import csv
import json

csv_file='all_clerks_to_json.csv'
json_file='all_clerks.json'

# my_json={}
my_json=[]

with open(csv_file,'r', encoding='utf-8') as fobj:
  reader=csv.DictReader(fobj)
  for row in reader:
    # key=row['num']
    # my_json[key]=row
    my_json.append(row)

with open(json_file,'w', encoding='utf-8') as fobj:
  fobj.write(json.dumps(my_json,indent=2,ensure_ascii=False))
