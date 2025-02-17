import csv
import time


def check_diff(file1, file2):
    diff = ''

    file1_data = csv.reader(file1)
    file2_data = csv.reader(file2)

    data1 = [data for data in file1_data]
    data2 = [data for data in file2_data]
    data2_list = [data[1] for data in data2]

    for i in range(len(data1)):
        if len(str(data1[i][1])) > 0 and not str(data1[i][1]) in data2_list:
            print(data1[i])
            diff += str(data1[i])

    return diff


def write_diff(diff, flag):
    with open(f'./result_{flag}_result.txt', 'w', encoding='utf-8') as file:
        file.write(diff)


def main():
    file1 = open('./all_preregister.csv', 'r', encoding='utf-8')
    file2 = open('./all_registered.csv', 'r', encoding='utf-8')
    # diff_1 = check_diff(file1, file2)
    # write_diff(diff_1, 'diff_1')

    diff_2 = check_diff(file2, file1)
    write_diff(diff_2, 'diff_2')


if __name__ == '__main__':
    main()
