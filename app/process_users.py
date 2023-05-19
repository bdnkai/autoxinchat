import cv2 as cv
import difflib
import numpy as np
import pytesseract
import requests




def clean_list(lst, thresh_rate=0.54, player_names=[]):
    cleaned_list = []
    name_cases = player_names
    case_name = set(name.lower() for name in name_cases)
    cleaned_list = [difflib.get_close_matches(item.lower(), case_name, n=1, cutoff=thresh_rate)[0]
                    for item in lst if difflib.get_close_matches(item.lower(), case_name, n=1, cutoff=thresh_rate)]
    return cleaned_list



def debug_list(lst, thresh_rate=0.54, player_names=[]):
    clean_list = []
    debug_list = []
    name_cases = player_names
    case_name = set(name.lower() for name in name_cases)
    for item in lst:
        cleaned_list = [difflib.get_close_matches(item.lower(), case_name, n=1, cutoff=thresh_rate)][0]

        clean_results = [clean for clean in cleaned_list]

        if cleaned_list:
            clean_list.append(clean_results[0])
            clean_message = f'{thresh_rate}| {item} |>>| {clean_results}'
            debug_list.append(clean_message)
            clean_list.append(clean_results[0])



    debug_final = list(set(clean_list))
    finalize_list = debug_list, debug_final

    return finalize_list



def process_image(link, thresh_rate=0.54, player_names=[]):
    response = requests.get(link)
    img_array = np.array(bytearray(response.content), dtype=np.uint8)
    img = cv.imdecode(img_array, -1)

    orig_height, orig_width = img.shape[:2]
    fixed_width = 500
    ratio = fixed_width / float(orig_width)
    fixed_height = int(orig_height * ratio)
    img = cv.resize(img, (fixed_width, fixed_height))

    sigma_x = 14 * ratio
    sigma_y = 5 * ratio
    alpha = 14 * ratio
    beta = 14 * ratio
    min_conf = 150


    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    sharpen = cv.GaussianBlur(gray, (0, 0), sigmaX=sigma_x, sigmaY=sigma_y)
    sharpen = cv.addWeighted(gray, alpha, sharpen, -alpha, beta)
    thresh = cv.threshold(sharpen, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]
    config = '-c char_whitelist=你爸爸野爹我命天破聪明绝顶的贪生恶杀abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ --oem 3 --psm 12'


    usernames = []
    text = pytesseract.image_to_string(thresh, lang='chi_sim', config=config)
    lines = text.split('\n')
    for line in lines:
        if ':x' in line:
            username = line.split(':')[0].strip()
            usernames.append(username)



    usernames = [result.split(":")[0].replace(" ", "") for result in text.split("\n") if ":" in result]
    clean_names = list(set(clean_list(usernames, thresh_rate, player_names)))

    return clean_names




def process_debug(link, thresh_rate=0.54, player_names=[]):

    response = requests.get(link)
    img_array = np.array(bytearray(response.content), dtype=np.uint8)
    img = cv.imdecode(img_array, -1)

    orig_height, orig_width = img.shape[:2]
    fixed_width = 500
    ratio = fixed_width / float(orig_width)
    fixed_height = int(orig_height * ratio)
    img = cv.resize(img, (fixed_width, fixed_height))

    sigma_x = 14 * ratio
    sigma_y = 5 * ratio
    alpha = 14 * ratio
    beta = 14 * ratio
    min_conf = 150


    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    sharpen = cv.GaussianBlur(gray, (0, 0), sigmaX=sigma_x, sigmaY=sigma_y)
    sharpen = cv.addWeighted(gray, alpha, sharpen, -alpha, beta)
    thresh = cv.threshold(sharpen, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]
    config = '-c char_whitelist=你爸爸野爹我命天破聪明绝顶的贪生恶杀abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ --oem 3 --psm 12'


    usernames = []
    text = pytesseract.image_to_string(thresh, lang='chi_sim', config=config)
    lines = text.split('\n')
    for line in lines:
        if ':x' in line:
            username = line.split(':')[0].strip()
            usernames.append(username)



    usernames = [result.split(":")[0].replace(" ", "") for result in text.split("\n") if ":" in result]
    debug_names = debug_list(usernames, thresh_rate, player_names)
    print(debug_names)
    return debug_names
