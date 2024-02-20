import os
import re
from datetime import datetime


def transform_data():
    ocr_text_file_list = os.listdir('ocr_text')
    ocr_text_file_list.sort()
    ocr_text_file = ocr_text_file_list[-1]

    with open(f'ocr_text/{ocr_text_file}') as f:
        ocr_text_list = f.readlines()

    # detect merchant name
    merchant_name = ocr_text_list[0].strip()
    print(merchant_name)

    if 'Ang Mo' in merchant_name:
        extract_data_ang_mo(ocr_text_list)
    elif 'SHENG SIONG' in merchant_name:
        extract_data_sheng_siong(ocr_text_list)


def extract_data_ang_mo(ocr_text_list):
    merchant_name = 'Ang Mo Supermarket Pte Ltd'
    # get index of description, total and date
    for i in range(len(ocr_text_list)):
        line = ocr_text_list[i]
        if 'Description' in line:
            description_index = i
        if 'TOTAL' in line:
            total_index = i
        if 'Date:' in line:
            date_index = i

    # convert date
    date_line = ocr_text_list[date_index]
    original_format = "%d/%m/%Y %H:%M:%S"
    date_line_split = date_line.strip().split(' ')
    input_datetime_str = f'{date_line_split[1]} {date_line_split[2]}'
    receipt_date = convert_datetime_format(input_datetime_str,original_format)
    print(receipt_date)

    # extract description and price
    for i in range(description_index+1,total_index,2):
        description_line = ocr_text_list[i]
        pattern = r'\d{1}x'
        description = ' '.join(clean_description(description_line.split(' '),pattern)).strip()
        
        price_line = ocr_text_list[i+1]
        price = price_line.split(' ')[-1].strip()

        print(merchant_name, receipt_date, description, price)
        with open('items.csv','a') as f:
            f.write(f'{merchant_name},{receipt_date},{description},{price}\n')


def extract_data_sheng_siong(ocr_text_list):
    merchant_name = 'SHENG SIONG SUPERMARKET PTE LTD'
    # get index of description, total and date
    rounding_index = 0
    for i in range(len(ocr_text_list)):
        line = ocr_text_list[i]
        if 'Description' in line:
            description_index = i
        if 'Sub Total' in line:
            total_index = i
        if 'Terminal' in line:
            date_index = i
        if 'Sales Discount' in line:
            discount_index = i
        if 'Rounding Adjustment' in line:
            rounding_index = i

    # convert date
    date_line = ocr_text_list[date_index]
    date_line = ' '.join(date_line.split(' ')[-2:])
    original_format = "%d/%m/%Y %H:%M"
    receipt_date = convert_datetime_format(date_line.strip(),original_format)
    print(receipt_date)

    # extract item index
    item_index_list = []
    for i in range(description_index+1,total_index):
        pattern = r'\d+\.\s'
        match = re.search(pattern, ocr_text_list[i])
        if match:
            # print(match.group())
            item_index_list.append(i)
    item_index_list.append(total_index) # add total index to the end of the list

    for list_index, i in enumerate(item_index_list[:-1]):
        price_list = []
        start_index = i
        end_index = item_index_list[list_index+1]
        for j in range(start_index,end_index):
            # print(ocr_text_list[j].strip())
            pattern = r'-*\d{1,}\.\d{2}'
            matches = re.findall(pattern, ocr_text_list[j])
            if matches:
                price_list.append(matches[-1])
        description_line = ocr_text_list[i]
        pattern = r'\d+\.' # -*\d{1,}\.\d{2}
        description = ' '.join(clean_description(description_line.split(' '),pattern)).strip()
        # print(description,price_list)
        for price in price_list:
            print(merchant_name, receipt_date, description, price)
            with open('items.csv','a') as f:
                f.write(f'{merchant_name},{receipt_date},{description},{price}\n')
    
    # shengsiong discount and adjustment
    discount_line = ocr_text_list[discount_index]
    discount = discount_line.split(' ')[-1].strip()[2:-1]
    print(merchant_name, receipt_date, 'Discount', discount)
    with open('items.csv','a') as f:
        f.write(f'{merchant_name},{receipt_date},Discount,-{discount}\n')

    if rounding_index > 0:
        rounding_line = ocr_text_list[rounding_index]
        rounding = rounding_line.split(' ')[-1].strip()[2:-1]
        print(merchant_name, receipt_date, 'Rounding', rounding)
        with open('items.csv','a') as f:
            f.write(f'{merchant_name},{receipt_date},Rounding,-{rounding}\n')
    

def clean_description(my_list,pattern):
    filtered_list = []

    for text in my_list:
        if not re.search(pattern, text):
            # If the pattern is not found in the text, add it to the filtered list
            filtered_list.append(text)

    return filtered_list


def convert_datetime_format(input_datetime_str,original_format):
    # Convert the input string to a datetime object using the original format
    original_datetime = datetime.strptime(input_datetime_str, original_format)

    # Convert the datetime object to a string with the desired format
    new_format = "%Y-%m-%d %H:%M:%S"
    new_datetime_str = original_datetime.strftime(new_format)

    return new_datetime_str


if __name__ == "__main__":
    transform_data()