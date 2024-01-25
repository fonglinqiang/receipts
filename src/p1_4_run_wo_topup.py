from src.a1_ocr_api import get_ocr_response
from src.a2_extract_response_text import extract_response_text
from src.a3_transform_data import transform_data
from src.a4_update_balance import update_balance

if __name__ == "__main__":
    get_ocr_response()
    extract_response_text()
    transform_data()
    update_balance()