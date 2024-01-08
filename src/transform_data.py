import os
import re
from datetime import datetime


def transform_data():
    ocr_text_file_list = os.listdir('ocr_text')
    ocr_text_file_list.sort()
    ocr_text_file = ocr_text_file_list[-1]

    with open(f'ocr_text/{ocr_text_file}') as f:
        ocr_text_list = f.readlines()
    
    # detect relevant parameters
    for i in range(len(ocr_text_list)):
        line = ocr_text_list[i]
        if i == 0:
            merchant_name = line.strip()
        if 'Description' in line:
            description_index = i
        if 'TOTAL' in line:
            total_index = i
        if 'Date:' in line:
            date_index = i

    # convert date
    date_line_split = ocr_text_list[date_index].strip().split(' ')
    receipt_date = f'{date_line_split[1]} {date_line_split[2]}'

    # extract description and price
    for i in range(description_index+1,total_index,2):
        description_line = ocr_text_list[i]
        description = ' '.join(remove_qty_from_description(description_line.split(' '))).strip()
        
        price_line = ocr_text_list[i+1]
        price = price_line.split(' ')[-1].strip()

        print(merchant_name, receipt_date, description, price)
        with open('items.csv','a') as f:
            f.write(f'{merchant_name},{receipt_date},{description},{price}\n')
    

def remove_qty_from_description(my_list):
    pattern = r'\d{1}x'
    filtered_list = []

    for text in my_list:
        if not re.search(pattern, text):
            # If the pattern is not found in the text, add it to the filtered list
            filtered_list.append(text)

    return filtered_list


# def convert_datetime_format(input_datetime_str):
#     # Convert the input string to a datetime object using the original format
#     original_format = "%d/%m/%Y %H:%M:%S"
#     original_datetime = datetime.strptime(input_datetime_str, original_format)

#     # Convert the datetime object to a string with the desired format
#     new_format = "%y/%m/%d %H:%M:%S"
#     new_datetime_str = original_datetime.strftime(new_format)

#     return new_datetime_str


if __name__ == "__main__":
    transform_data()