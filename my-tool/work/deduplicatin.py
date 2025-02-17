import csv

# TODO:Completed

def check_repeat(file):
    repeat_str = ''

    file_data = csv.reader(file)

    data = [data for data in file_data]

    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if data[i][1] == data[j][1]:
                print(data[i][1], data[j][1])
                repeat_str += str(data[i])

    return repeat_str


def write_repeat(diff):
    with open('./repeat_result_registered.txt', 'w', encoding='utf-8') as file:
        file.write(diff)


def main():
    file = open('./all_registered.csv', 'r', encoding='utf-8')
    str = check_repeat(file)
    write_repeat(str)


if __name__ == '__main__':
    main()
