import json
import requests
import os

URL = "https://ocr.asprise.com/api/v1/receipt"


def get_ocr_response():
    receipt_jpg_file_list = os.listdir('receipts')
    receipt_jpg_file_list.sort()
    receipt_jpg_file_name = receipt_jpg_file_list[-1]

    image = f'receipts/{receipt_jpg_file_name}'

    res = requests.post(url=URL,
                        data={
                            'api_key': 'TEST',
                            'recognizer': 'auto',
                            'ref_no': 'oct_python_123'
                        },
                        files={
                            'file' : open(image,'rb')
                        })

    with open(f'ocr_response/{receipt_jpg_file_name.split(".")[0]}.json','w') as f:
        json.dump(json.loads(res.text),f)

if __name__ == "__main__":
    get_ocr_response()