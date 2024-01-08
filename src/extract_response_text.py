import json
import os


def extract_response_text():
    ocr_response_json_list = os.listdir('ocr_response')
    ocr_response_json_list.sort()
    ocr_response_json_file = ocr_response_json_list[-1]

    with open(f'ocr_response/{ocr_response_json_file}') as f:
        ocr_response_dict = json.load(f)

    ocr_response_text = ocr_response_dict['receipts'][0]['ocr_text']

    with open(f'ocr_text/{ocr_response_json_file.split(".")[0]}.txt','w') as f:
        f.write(ocr_response_text)


if __name__ == "__main__":
    extract_response_text()