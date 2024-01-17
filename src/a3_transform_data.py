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
        for i in range(len(ocr_text_list)):
            line = ocr_text_list[i]
            if 'Description' in line:
                description_index = i
            if 'TOTAL' in line:
                total_index = i
            if 'Date:' in line:
                date_index = i
    elif 'SHENG SIONG' in merchant_name:
        for i in range(len(ocr_text_list)):
            line = ocr_text_list[i]
            if 'Description' in line:
                description_index = i
            if 'Sub Total' in line:
                total_index = i
            if 'Receipt:' in line:
                date_index = i-1
            if 'Sales Discount' in line:
                discount_index = i
            if 'Rounding Adjustment' in line:
                rounding_index = i

    # convert date
    date_line = ocr_text_list[date_index]
    receipt_date = convert_datetime_format(date_line,merchant_name)
    print(receipt_date)

    # extract description and price
    for i in range(description_index+1,total_index,2):
        description_line = ocr_text_list[i]
        description = ' '.join(clean_description(description_line.split(' '),merchant_name)).strip()
        
        price_line = ocr_text_list[i+1]
        price = price_line.split(' ')[-1].strip()

        print(merchant_name, receipt_date, description, price)
        with open('items.csv','a') as f:
            f.write(f'{merchant_name},{receipt_date},{description},{price}\n')
    
    # shengsiong discount and adjustment
    if 'SHENG SIONG' in merchant_name:
        discount_line = ocr_text_list[discount_index]
        discount = discount_line.split(' ')[-1].strip()[2:-1]
        print(merchant_name, receipt_date, 'Discount', discount)
        with open('items.csv','a') as f:
            f.write(f'{merchant_name},{receipt_date},Discount,-{discount}\n')

        rounding_line = ocr_text_list[rounding_index]
        rounding = rounding_line.split(' ')[-1].strip()[2:-1]
        print(merchant_name, receipt_date, 'Rounding', rounding)
        with open('items.csv','a') as f:
            f.write(f'{merchant_name},{receipt_date},Rounding,-{rounding}\n')
    

def clean_description(my_list,merchant_name):
    if 'Ang Mo' in merchant_name:
        # remove qty in front of description
        pattern = r'\d{1}x'
    elif 'SHENG SIONG' in merchant_name:
        # remove index in front of description
        pattern = r'\d{1}\.'
    filtered_list = []

    for text in my_list:
        if not re.search(pattern, text):
            # If the pattern is not found in the text, add it to the filtered list
            filtered_list.append(text)

    return filtered_list


def convert_datetime_format(date_line,merchant_name):
    # Convert the input string to a datetime object using the original format
    if 'Ang Mo' in merchant_name:
        date_line_split = date_line.strip().split(' ')
        input_datetime_str = f'{date_line_split[1]} {date_line_split[2]}'
        original_format = "%d/%m/%Y %H:%M:%S"
    elif 'SHENG SIONG' in merchant_name:
        input_datetime_str = date_line.strip()
        original_format = "%d/%m/%Y %H:%M"
    original_datetime = datetime.strptime(input_datetime_str, original_format)

    # Convert the datetime object to a string with the desired format
    new_format = "%Y-%m-%d %H:%M:%S"
    new_datetime_str = original_datetime.strftime(new_format)

    return new_datetime_str


if __name__ == "__main__":
    transform_data()