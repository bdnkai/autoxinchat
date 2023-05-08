import cv2
import difflib
import numpy as np
import pytesseract
import requests
import concurrent.futures
from filtered_case import names as name_cases


def clean_list(lst):
    cleaned_list = []
    case_name = set(name.lower() for name in name_cases)
    cleaned_list = [difflib.get_close_matches(item.lower(), case_name, n=1, cutoff=0.5)[0]
                    for item in lst if difflib.get_close_matches(item.lower(), case_name, n=1, cutoff=0.5)]
    return cleaned_list


def process_image(link):
    response = requests.get(link)
    img_array = np.array(bytearray(response.content), dtype=np.uint8)
    img = cv2.imdecode(img_array, -1)

    orig_height, orig_width = img.shape[:2]
    fixed_width = 400
    ratio = fixed_width / float(orig_width)
    fixed_height = int(orig_height * ratio)
    img = cv2.resize(img, (fixed_width, fixed_height))

    sigma_x = 14 * ratio
    sigma_y = 5 * ratio
    alpha = 14 * ratio
    beta = 14 * ratio
    min_conf = 150
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sharpen = cv2.GaussianBlur(gray, (0, 0), sigmaX=sigma_x, sigmaY=sigma_y)
    sharpen = cv2.addWeighted(gray, alpha, sharpen, -alpha, beta)
    thresh = cv2.threshold(sharpen, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]


    config = '-c char_whitelist=你爸爸野爹我命天破聪明绝顶的贪生恶杀abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ --oem 3 --psm 12'

    usernames = []
    text = pytesseract.image_to_string(sharpen, lang='chi_sim+eng', config=config)
    lines = text.split('\n')
    for line in lines:
        if ':X' in line:
            username = line.split(':')[0].strip()
            usernames.append(username)

    usernames = [result.split(":")[0].replace(" ", "") for result in text.split("\n") if ":" in result]
    clean_names = list(set(clean_list(usernames)))

    return clean_names




