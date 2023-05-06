import cv2
import pytesseract
import requests
import numpy as np

# Download the image using requests
img_url = "https://cdn.discordapp.com/attachments/1069726036041945098/1103442611852820490/Screenshot_139.png"
response = requests.get(img_url)
img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

# Preprocess the image
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0.185)
sharpen_kernel = np.array([[-1, -1, -1], [-1, 9.3, -1], [-1, -1, -1]])
sharpen = cv2.filter2D(blur, -1, sharpen_kernel)
thresh = cv2.threshold(sharpen, 20, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
resized_img = cv2.resize(thresh, (350, 500))



# Apply Tesseract OCR
config = '-c char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ驳  --oem 3 --psm 11'
# Apply Tesseract OCR and draw boxes
boxes = pytesseract.image_to_boxes(img, lang='chi_sim', config=config)
for box in boxes.splitlines():
    box = box.split(' ')
    x,y,w,h = int(box[1]), int(box[2]), int(box[3]), int(box[4])
    cv2.rectangle(img, (x, img.shape[0]-y), (w, img.shape[0]-h), (0, 0, 255), 2)

cv2.imshow('Resized Image', blur)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Extract the usernames before the colon
usernames = []
text = pytesseract.image_to_string(blur, lang='chi_sim+eng', config=config)
lines = text.split('\n')
for line in lines:
    if ':' in line:
        username = line.split(':')[0].strip()
        usernames.append(username)

usernames = [result.split(":")[0].replace(" ", "") for result in text.split("\n") if ":" in result]
usernames = list(set(usernames))
print(usernames)
