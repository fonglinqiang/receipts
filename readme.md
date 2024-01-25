# Receipts Project

This projects aims to automate tracking of household petty cash by extracting data from receipts.

We currently support receipt from Supermarket in Singapore
- Ang Mo Supermarket
- Sheng Siong Supermarket

OCR API used is the free version and have a limited number of use per day.

## Usage
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=$PWD
```
Save a new receipt image in the `receipts` folder. It is recommended to name your receipts by date in yyyy-mm-dd.ext format as the scripts will sort the files by filenames and process the latest file.

Script 1: call OCR API and get response in JSON file, saved in `ocr_response` folder
```
python src/a1_ocr_api.py
```

Script 2: extract receipt text from JSON file, saved in `ocr_text` folder
```
python src/a2_extract_response_text.py
```

Script 3: detect items description and price from receipt text and update `items.csv`
```
python src/a3_transform_data.py 
```

Script 4: update balance in pretty cash -> `balance.csv`
```
python src/a4_update_balance.py
```

Script 5: topup money in pretty cash -> `balance.csv`, change the topup amount accordingly
```
python src/a5_topup.py
```

Script `p1_4_run_wo_topup.py` will run script 1 to 4 in that order.
