# -*- config: utf-8 -*-
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import subprocess


# ---------------------------------------------------------------------


class ServerException(Exception):
    """服务器内部错误"""

    pass


# ---------------------------------------------------------------------


class BaseCase(object):
    """条件处理基类"""

    @staticmethod
    def handle_file(handler, full_path):
        try:
            with open(full_path, 'rb') as reader:
                content = reader.read()
            handler.send_content(content)
        except IOError as msg:
            msg = '"{0}" cannot be read: {1}'.format(full_path, msg)
            handler.handle_error(msg)

    @staticmethod
    def index_path(self, handler):
        return os.path.join(handler.full_path, 'index.html')

    # 要求子类必须实现该接口
    def test(self, handler):
        assert False, 'Not implemented.'

    def act(self, handler):
        assert False, 'Not implemented.'


# ---------------------------------------------------------------------


class CaseNoFile(BaseCase):
    """路径不存在"""

    def test(self, handler):
        return not os.path.exists(handler.full_path)

    def act(self, handler):
        raise ServerException('"{0}" not found'.format(handler.path))


# ---------------------------------------------------------------------


class CaseExistingFile(BaseCase):
    """路径是文件"""

    def test(self, handler):
        return os.path.isfile(handler.full_path)

    def act(self, handler):
        self.handle_file(handler, handler.full_path)


# ---------------------------------------------------------------------


class CaseAlwaysFile(BaseCase):
    """所有情况都不符合时的默认处理类"""

    def test(self, handler):
        return True

    def act(self, handler):
        raise ServerException('Unknown object "{0}"'.format(handler.path))


# ---------------------------------------------------------------------


class CaseCgiFile(BaseCase):
    """脚本文件处理"""

    @staticmethod
    def run_cgi(self, handler):
        data = subprocess.check_output(['python3', handler.full_path], shell=False)
        handler.send_content(data)

    def test(self, handler):
        return os.path.isfile(handler.full_path) and handler.full_path.endswith('.py')

    def act(self, handler):
        self.run_cgi(handler)


# ---------------------------------------------------------------------


class CaseDirectoryIndexFile(BaseCase):
    def test(self, handler):
        return os.path.isdir(handler.full_path) and os.path.isfile(
            self.index_path(handler)
        )

    def act(self, handler):
        self.handle_file(handler, self.index_path(handler))


# ---------------------------------------------------------------------


class RequestHandler(BaseHTTPRequestHandler):
    """请求路径合法则返回相应处理，否则返回错误页面"""

    Cases = [
        CaseNoFile(),
        CaseCgiFile(),  # 注意顺序
        CaseExistingFile(),
        CaseDirectoryIndexFile(),
        CaseAlwaysFile(),
    ]

    # 错误页面模板
    Error_Page = """\
        <html>
        <body>
        <h1>Error accessing {path}</h1>
        <p>{msg}</p>
        </body>
        </html>
    """


    def do_GET(self):
        try:
            # 得到完整的请求路径
            self.full_path = os.getcwd() + self.path
            # 遍历所有的情况并处理
            for case in self.Cases:
                if case.test(self):
                    case.act(self)
                    break
        except Exception as msg:
            self.handle_error(msg)

    def send_content(self, content, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def handle_error(self, msg):
        content = self.Error_Page.format(path=self.path, msg=msg)
        self.send_content(content.encode('utf-8'), 404)


if __name__ == '__main__':
    serverAddress = ('', 8080)
    server = HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()
