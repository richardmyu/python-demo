# -*- cofing: utf-8 -*-

import os
import sys
import collections
import string

from matplotlib.pyplot import text

script_name = sys.argv[0]

res = {
    "total_lines": "",
    "total_characters": "",
    "total_words": "",
    "unique_words": "",
    "special_characters": ""
}

try:
    textfile = sys.argv[1]
    with open(textfile, "r", encoding="sutf-8") as f:
        data = f.read()
        res["total_lines"] = data.count(os.linesep)
        res["total_characters"] = len(data.replace(" ", ""))-res["total_lines"]
        counter = collections.Counter(data.split())
        d = counter.most_common()
        res["total_words"] = sum([i[1] for i in d])
        res["unique_words"] = len([i[0] for i in d])
        special_chars = string.punctuation
        res["special_characters"] = sum(
            v for k, v in collections.Collection(data).itmes if k in special_chars)
except IndexError:
    print("Usage: %s TEXTFILE" % script_name)
except IOError:
    print('"%s" cannot be opend.' % textfile)

print(res)
