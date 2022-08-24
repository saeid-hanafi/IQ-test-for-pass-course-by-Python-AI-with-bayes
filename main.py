# Libraries
# import library for read Excel files
import xlrd
# import library for math actions
import math
# import library for get random int
import random


# Functions
# function for read Excel files by location
def read_exel_files(file_loc):
    file = xlrd.open_workbook_xls(file_loc)
    return file.sheet_by_index(0)


# get average of class list
def get_avg(class_list):
    sum_items = 0
    for class_index in range(0, len(class_list)):
        sum_items += float(class_list[class_index])
    return sum_items / len(class_list)


# get std of class list
def get_std(class_list, avg):
    sum_item = 0
    for class_index in range(0, len(class_list)):
        sum_item += math.pow((float(class_list[class_index]) - float(avg)), 2)

    variance = sum_item / len(class_list)
    return math.sqrt(variance)


# get final bayes result
def p_x_w(x, class_list):
    avg_items = get_avg(class_list)
    sdt_items = get_std(class_list, avg_items)
    return (1/(math.sqrt(2*math.pi) * sdt_items)) * math.pow(math.e, (-1/2) * math.pow((float(x) - avg_items)/sdt_items, 2))


# get final result
def get_final_result(IQ_number, class1_list, c1_number, class2_list, c2_number):
    p_x_w1 = p_x_w(IQ_number, class1_list)
    p_w1_x = p_x_w1 * c1_number
    p_x_w2 = p_x_w(IQ_number, class2_list)
    p_w2_x = p_x_w2 * c2_number

    if p_w1_x > p_w2_x:
        return int(0)
    elif p_w1_x < p_w2_x:
        return int(1)
    else:
        return random.randint(0, 1)


# test code by Excel file
def test_code_list(excel_file_loc):
    test_info = read_exel_files(excel_file_loc)
    test_list = []
    for test_index in range(0, test_info.nrows):
        test_list_item = [test_info.cell_value(test_index, 0), test_info.cell_value(test_index, 1)]
        test_list.append(test_list_item)
    return test_list


# get Excel file info and sort list of IQ and pass course value(1 is pass, 0 is failed)
loc = "DataSet.xls"
file_info = read_exel_files(loc)
dateset = []
for i in range(0, file_info.nrows):
    file_item = [file_info.cell_value(i, 0), file_info.cell_value(i, 1)]
    dateset.append(file_item)

# create two class (class1 is IQs that failed in course and class2 is IQs that pass course)
class1 = []
class2 = []
for data_item in dateset:
    if data_item[1] == 0:
        class1.append(data_item[0])
    elif data_item[1] == 1:
        class2.append(data_item[0])

c1 = len(class1)/len(dateset)
c2 = len(class2)/len(dateset)

# get IQ and return final answer
# 0 => can pass course
# 1 => can not pass course
# TestSet.xls is a list for test code
test_loc = str(input("Enter IQ Test List Name With Format xls : "))
get_list = test_code_list(test_loc)
count_true_result = 0
for i in range(0, len(get_list)):
    IQ_item = get_list[i][0]
    test_result = get_list[i][1]
    result = get_final_result(IQ_item, class1, c1, class2, c2)
    if result == test_result:
        count_true_result += 1

print(int((count_true_result/len(get_list)) * 100), "% is true answer")

# Test code with enter number of IQ
# get IQ and return final answer
# 0 => can pass course
# 1 => can not pass course
x = float(input("Enter IQ : "))
print(get_final_result(x, class1, c1, class2, c2))
