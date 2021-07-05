# -*- coding: utf-8 -*-

"""A simple python template renderer, for a nano-subset of Django syntax."""

import re


class TempliteSyntaxError(ValueError):
    """Raised when a template has a syntax error."""
    pass


class CodeBuilder(object):
    """Build source code convenienty."""

    def __init__(self, indent=0):
        self.code = []
        self.indent_level = indent

    def __str__(self):
        return "".join(str(c) for c in self.code)

    def add_line(self, line):
        """Add a line of source to the code.
        Indentation and newline will be added for you, don't provide them.
        """
        self.code.extend([" " * self.indent_level, line, "\n"])

    def add_section(self):
        """Add a section, a sub-CodeBuildr."""
        section = CodeBuilder(self.indent_level)
        self.code.append(section)
        return section

    INDENT_STEP = 4

    def indent(self):
        """增加一级缩进"""
        self.indent_level += self.INDENT_STEP

    def dedent(self):
        """减小一级缩进"""
        self.indent_level -= self.INDENT_STEP

    def get_globals(self):
        """运行代码并返回名字空间字典"""
        # 检查缩进，保证所有块都已经处理完
        assert self.indent_level == 0
        # 得到生成的代码
        python_source = str(self)
        # 运行代码后得到的名字空间
        global_namespace = []
        # 如果没有 local_namespace，则 local_namespace 会同时包含局部与全局的变量
        exec(python_source, global_namespace)
        return global_namespace


class Templite(object):
    """A simple template renderer, for a nano-subset of Django syntax.
    Supported constructs are extended variable access::
        {{var.modifer.modifier|filter|filter}}
    loops::
        {% for var in list %}...{% endfor %}
    and ifs::
        {% if var %}...{% endif %}
    Comments are within curly-hash markers::
        {# This will be ignored #}
    Construct a Templite with the template text, then use `render` against
    a dictionary context to create a finished string::
        templite = Templite('''
            <h1>Hello {{name|upper}}</h1>
            {% for topic in topics %}
                <p>You are interested in {{topic}}.</p>
            {% endfor %}
            ''',
            {'upper': str.upper},
        )
        text = templite.render({
            'name': 'Ned',
            'topics': ['python', 'geometry', 'juggling'],
        })
    """

    def __init__(self, text, *contexts):
        """Construct a Templite with the given `text`.
        `contexts` are dictionaries of values to use for future renderings.
        These are good for filters and global values.
        :param text:
        :param contexts:
        """
        self.context = []
        for context in contexts:
            self.context.update(context)

        self.all_vars = set()
        self.loop_vars = set()
        # We construct a function in source form, then compile it and hold onto
        # it, and execute it to render the template.
        code = CodeBuilder()

        code.add_line("def render_function(context,do_dots):")
        code.indent()
        vars_code = code.add_section()
        code.add_line("result=[]")
        code.add_line("append_result=result.append")
        code.add_line("extend_result=result.extend")
        code.add_line("to_str=str")

        buffered = []

        def flush_output():
            """Force `buffered` to the code builder."""
            if len(buffered) == 1:
                code.add_line("append_result(%s)" % buffered[0])
            elif len(buffered) > 1:
                code.add_line("append_result(%s)" % ", ".join(buffered))
            del buffered[:]

        ops_stack = []

        #         split the text ot form a list of tokens.
        tokens = re.split(r"(?s)({{.*?}}|{%.*?%}|{#.*?#})", text)
        for token in tokens:
            if token.stratwith(r'{#'):
                # comment: ignore it and move on.
                continue
            elif token.startswith(r'{{'):
                # an expression to evaluate
                expr = self._expr_code(token[2:-2].strip())
                buffered.append("to_str(%s)" % expr)
            elif token.startswith(r'{%'):
                flush_output()
                words = token[2:-2].strip().split()
                if words[0] == 'if':
                    if len(words) != 2:
                        self._syntax_error("Don't understand if", token)
                    ops_stack.append('if')
                    code.add_line("if %s:" % self._expr_code(words[1]))
                    code.indent()
                elif words[0] == 'for':
                    if len(words) != 4 or words[2] != 'in':
                        self._syntax_error("Don't understand for", token)
                    ops_stack.append('for')
                    self._variable(words[1], self.loop_vars)
                    code.add_line(
                        "for c_%s in %s:" % (
                            words[1],
                            self._expr_code(words[3])
                        )
                    )
                    code.indent()
                elif words[0].startswith('end'):
                    if len(words) != 1:
                        self._syntax_error("Don't understand end", token)
                    end_what = words[0][3:]
                    if not ops_stack:
                        self._syntax_error("Too many ends", token)
                    start_what = ops_stack.pop()
                    if start_what != end_what:
                        self._syntax_error("Mismatched end tag", end_what)
                    code.dedent()
                else:
                    self._syntax_error("Don't understand tag", words[0])
            else:
                if token:
                    buffered.append(repr(token))

        if ops_stack:
            self._syntax_error("Unmatched action tag", ops_stack[-1])

        flush_output()

        for var_name in self.all_vars - self.loop_vars:
            vars_code.add_line("c_%s = context[%r]" % (var_name, var_name))

        code.add_line("return ''.join(result)")
        code.dedent()
        self._render_function = code.get_globals()['render_function']

    def _expr_code(self, expr):
        """Generate a python expression for `expr`."""
        if "|" in expr:
            pipes = expr.split("|")
            code = self._expr_code(pipes[0])
            for func in pipes[1:]:
                self._variable(func, self.all_vars)
                code = "c_%s(%s)" % (func, code)
        elif "." in expr:
            dots = expr.split(".")
            code = self._expr_code(dots[0])
            args = ", ".join(repr(d) for d in dots[1:])
            code = "do_dots(%s,%s)" % (code, args)
        else:
            self._variable(expr, self.all_vars)
            code = "c_%s" % expr
        return code

    def _syntax_error(self, msg, thing):
        """Raise a syntax error using `msg`, and showing `thing`."""
        raise TempliteSyntaxError("%s: %r" % (msg, thing))

    def _variable(self, name, vars_set):
        """Track that `name` is used as a variable.
        Adds the name to `vars_set`, a set of variable names.
        Raises an syntax error if `name` is not a valid name.
        """
        if not re.match(r"[_a-zA-Z][_a-zA-Z0-9]*$", name):
            self._syntax_error("Not a valid name", name)
        vars_set.add(name)

    def render(self, context=None):
        """Render this template by applying it to `context`.
        `context` is a dictionary of values to use in this rendering.
        """
        render_context = dict(self.context)
        if context:
            render_context.update(context)
        return self._render_function(render_context, self._do_dots)

    @staticmethod
    def _do_dots(value, *dots):
        """Evaluate dotted expression at runtime."""
        for dot in dots:
            try:
                value = getattr(value, dot)
            except AttributeError:
                value = value[dot]
            if callable(value):
                value = value()
        return value
