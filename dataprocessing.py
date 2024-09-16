from datetime import datetime, timedelta
import csv

def is_within_30_days(date_str):
    # 将字符串转换为datetime对象
    given_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

    # 获取当前时间并设置时分秒为00:00:00
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # 计算30天前的日期
    thirty_days_ago = today - timedelta(days=30)

    # 判断给定日期是否在30天内
    return thirty_days_ago <= given_date <= today

send_num_dict = {}
with open('cust_records.txt', 'r', encoding='utf-8') as file:
    for line in file:
        data = line.strip().split(',')
        date_str = data[2]
        if is_within_30_days(date_str):
            if data[1] in send_num_dict.keys():
                send_num_dict[data[1]] += 1
            else:
                send_num_dict[data[1]] = 1

push_radio_dict = {}
with open('push_1.csv', mode='r', encoding='utf-8') as file:
    # 创建一个CSV阅读器
    csv_reader = csv.reader(file)

    # 逐行读取CSV文件
    for row in csv_reader:
        if row[0] == 'cust_id': continue
        push_radio_dict[row[0]] = row[1]

risk_radio_dict = {}
with open('risk_1.csv', mode='r', encoding='utf-8') as file:
    # 创建一个CSV阅读器
    csv_reader = csv.reader(file)

    # 逐行读取CSV文件
    for row in csv_reader:
        if row[0] == 'cust_id': continue
        risk_radio_dict[row[0]] = row[1]

data_list = []
with open('cust_info.txt', 'r', encoding='utf-8') as file:
    # 一行一行读取文件
    for line in file:
        data = line.strip().split(',')
        s = ''
        for i in range(1, 11):
            s += data[i]
            s += ','
        if data[1] in push_radio_dict.keys():
            s += push_radio_dict[data[1]]
            s += ','
        else:
            s += '1,'
        if data[1] in send_num_dict.keys():
            s += str(send_num_dict[data[1]])
            s += ','
        else:
            s += '0,'
        if data[1] in risk_radio_dict.keys():
            s += risk_radio_dict[data[1]]
        else:
            s += '0'
        data_list.append(s)

with open('customers.txt', 'a', encoding='utf-8') as file:  # 使用 'a' 模式追加内容
    for line in data_list:
        file.write(line + '\n')  # 每行末尾加上换行符