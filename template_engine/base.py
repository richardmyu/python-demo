# -*- coding: utf-8 -*-

from template import Template
from collections import namedtuple

template_text = """
<p>Welcome, {{user_name}}</p>
<p>Products:</p>
<ul>
{% for product in product_list %}
    <li>{{ product.name }}: {{ product.price|format_price }}</li>
{% endfor %}
</ul>
"""

Product = namedtuple("Product", ["name", "price"])
product_list = [Product("Apple", 1), Product("Fig", 1.5), Product("Pomegranate", 3.25)]


def format_price(price):
    return "$%.2f" % price


t = Template(template_text, {"user_name": "Charlie", "product_list": product_list}, {"format_price": format_price})

print('--- start render ---')
print(t.render())
print('--- end render ---')
