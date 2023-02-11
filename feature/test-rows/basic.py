"""
Rows 快速操作 csv 文件

https://pythondict.com/python-data-analyze/rows/
"""

import rows

# TODO: OverflowError: Python int too large to convert to C long

cities = rows.import_from_csv("data/brazilian-cities.csv")
rio_biggest_cities = [
    city for city in cities if city.state == "RJ" and city.inhabitants > 500000
]

for city in rio_biggest_cities:
    density = city.inhabitants / city.area
    print(f"{city.city} ({density:5.2f} ppl/km²)")
