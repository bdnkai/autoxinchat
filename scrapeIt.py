import requests
import cv2
import numpy as np
import pytesseract
from Levenshtein import distance
from fuzzywuzzy import fuzz

# download the image from the URL and save it locally
url = "https://cdn.discordapp.com/attachments/1076623943760347136/1103504005725949952/image.png"
response = requests.get(url)
with open("image.png", "wb") as f:
    f.write(response.content)

# load the image using OpenCV and convert it to grayscale
image = cv2.imread("image.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# apply some pre-processing to the image
thresh_value = 150
thresh = cv2.threshold(gray, thresh_value, 255, cv2.THRESH_BINARY_INV)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

# show the processed image
cv2.imshow("Processed Image", morph)
cv2.waitKey(0)
cv2.destroyAllWindows()

# use Tesseract OCR to extract the text from the image
config = "--psm 6"
text = pytesseract.image_to_string(morph, config=config, lang='chi_sim+eng')

# get the bounding boxes of the characters in the image
boxes = pytesseract.image_to_boxes(morph, lang='chi_sim+eng')

# parse the text to extract the usernames before the colon and draw boxes around the characters
usernames = []
for line in text.split("\n"):
    if ":" in line:
        username = line.split(":")[0].strip()
        # correct common recognition errors
        username = username.replace("l", "i")
        username = username.replace("1", "i")
        username = username.replace("0", "o")
        username = username.replace("5", "s")
        username = username.replace("8", "b")
        # use Levenshtein distance and fuzzy string matching to correct errors
        for reference in ["john", "mary", "peter", "jane"]:
            if distance(username.lower(), reference) <= 1:
                username = reference.capitalize()
                break
            if fuzz.ratio(username.lower(), reference) >= 90:
                username = reference.capitalize()
                break
        # draw boxes around the characters
        for box in boxes.split("\n"):
            if box.startswith(username):
                box_coords = box.split()[1:-1]
                x, y, w, h = [int(coord) for coord in box_coords]
                cv2.rectangle(image, (x, image.shape[0]-y), (w, image.shape[0]-h), (0, 255, 0), 2)
        usernames.append(username)

# show the image with boxes drawn around the characters
cv2.imshow("OCR Result", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(usernames)
