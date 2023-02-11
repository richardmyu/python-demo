import json
import time


def json_to_csv():
    try:
        with open('input.json', 'r', encoding='utf-8') as f:
            data = json.loads(f.read())

        output = ','.join([*data[0]])
        for obj in data:
            output += f'\n{obj["Name"]},{obj["age"]},{obj["birthyear"]}'

        t = time.localtime()
        output_suffix = (
            f'{t.tm_year}_{t.tm_mon}_{t.tm_mday}_{t.tm_hour}_{t.tm_min}_{t.tm_sec}'
        )

        with open(
            f'output_{output_suffix}.csv',
            'w',
            encoding='utf-8',
        ) as f:
            f.write(output)
    except Exception as ex:
        print(f'Error: {str(ex)}')


if __name__ == '__main__':
    json_to_csv()
