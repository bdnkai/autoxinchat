import cv2
import pytesseract
import requests
import numpy as np
import difflib
from filtered_case import names as name_cases



# Load image from URL
url = "https://cdn.discordapp.com/attachments/1101022979963490324/1104425148523757658/image.png"
response = requests.get(url)
img_array = np.array(bytearray(response.content), dtype=np.uint8)
img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

# Get the original height and width of the image
orig_height, orig_width = img.shape[:2]

fixed_width = 500
ratio = fixed_width / float(orig_width)
fixed_height = int(orig_height * ratio)

img = cv2.resize(img, (fixed_width, fixed_height))


def clean_list(lst):
    cleaned_list = []
    case_name = [name.lower() for name in name_cases]
    for item in lst:
        matches = difflib.get_close_matches(item.lower(), case_name, n=1, cutoff=0.55)
        if len(matches) > 0:
            cleaned_list.append(matches[0])
    return cleaned_list



while True:
    sigmaX = 14 * ratio
    sigmaY = 6 * ratio
    alpha = 14 * ratio
    beta = 14 * ratio
    min_conf = 150

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sharpen = cv2.GaussianBlur(gray, (0, 0), sigmaX=sigmaX, sigmaY=sigmaY)
    sharpen = cv2.addWeighted(gray, alpha, sharpen, -alpha, beta)
    thresh = cv2.threshold(sharpen, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    config = '-c char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --oem 3 --psm 12'

    boxes = pytesseract.image_to_boxes(thresh, lang='chi_sim', config=config)
    for box in boxes.splitlines():
        box = box.split(' ')
        x, y, w, h = int(box[1]), int(box[2]), int(box[3]), int(box[4])
        cv2.rectangle(sharpen, (x, img.shape[0] - y), (w, img.shape[0] - h), (0, 0, 255), 1)

    usernames = []
    text = pytesseract.image_to_string(thresh, lang='chi_sim', config=config)
    lines = text.split('\n')
    for line in lines:
        if ': x' in line:
            username = line.split(':')[0].strip()
            usernames.append(username)

    usernames = [result.split(":")[0].replace(" ", "") for result in text.split("\n") if ":" in result]
    usernames= list(set(clean_list(usernames)))

    print(usernames)


    cv2.imshow("image", thresh)
    key = cv2.waitKey(0) & 0xFF

    # If the 'q' key is pressed, break from the loop
    if key == ord("q"):
        break

cv2.destroyAllWindows()


