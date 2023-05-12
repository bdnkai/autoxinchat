# custom data structure to hold the state of an HSV filter
class HsvFilter:
    def __init__(hMin=None, sMin=None, vMin=None, hMax=None, sMax=None, vMax=None,
                 sAdd=None, sSub=None, vAdd=None, vSub=None):
        hMin = hMin
        sMin = sMin
        vMin = vMin
        hMax = hMax
        sMax = sMax
        vMax = vMax
        sAdd = sAdd
        sSub = sSub
        vAdd = vAdd
        vSub = vSub
        
        
        TRACKBAR_WINDOW = 'Trackbars'
def init_control_gui():
    cv.namedWindow(TRACKBAR_WINDOW, cv.WINDOW_NORMAL)
    cv.resizeWindow(TRACKBAR_WINDOW, 350, 700)

    # required callback. we'll be using getTrackbarPos() to do lookups
    # instead of using the callback.
    def nothing(position):
        pass

    # create trackbars for bracketing.
    # OpenCV scale for HSV is H: 0-179, S: 0-255, V: 0-255
    cv.createTrackbar('HMin', TRACKBAR_WINDOW, 0, 179, nothing)
    cv.createTrackbar('SMin', TRACKBAR_WINDOW, 0, 255, nothing)
    cv.createTrackbar('VMin', TRACKBAR_WINDOW, 0, 255, nothing)
    cv.createTrackbar('HMax', TRACKBAR_WINDOW, 0, 179, nothing)
    cv.createTrackbar('SMax', TRACKBAR_WINDOW, 0, 255, nothing)
    cv.createTrackbar('VMax', TRACKBAR_WINDOW, 0, 255, nothing)
    # Set default value for Max HSV trackbars
    cv.setTrackbarPos('HMax', TRACKBAR_WINDOW, 179)
    cv.setTrackbarPos('SMax', TRACKBAR_WINDOW, 255)
    cv.setTrackbarPos('VMax', TRACKBAR_WINDOW, 255)

    # trackbars for increasing/decreasing saturation and value
    cv.createTrackbar('SAdd', TRACKBAR_WINDOW, 0, 255, nothing)
    cv.createTrackbar('SSub', TRACKBAR_WINDOW, 0, 255, nothing)
    cv.createTrackbar('VAdd', TRACKBAR_WINDOW, 0, 255, nothing)
    cv.createTrackbar('VSub', TRACKBAR_WINDOW, 0, 255, nothing)


# returns an HSV filter object based on the control GUI values
def get_hsv_filter_from_controls():
    # Get current positions of all trackbars
    hsv_filter = HsvFilter()
    # hsv_filter.hMin = cv.getTrackbarPos('HMin', TRACKBAR_WINDOW)
    # hsv_filter.sMin = cv.getTrackbarPos('SMin', TRACKBAR_WINDOW)
    # hsv_filter.vMin = cv.getTrackbarPos('VMin', TRACKBAR_WINDOW)
    # hsv_filter.hMax = cv.getTrackbarPos('HMax', TRACKBAR_WINDOW)
    # hsv_filter.sMax = cv.getTrackbarPos('SMax', TRACKBAR_WINDOW)
    # hsv_filter.vMax = cv.getTrackbarPos('VMax', TRACKBAR_WINDOW)
    # hsv_filter.sAdd = cv.getTrackbarPos('SAdd', TRACKBAR_WINDOW)
    # hsv_filter.sSub = cv.getTrackbarPos('SSub', TRACKBAR_WINDOW)
    # hsv_filter.vAdd = cv.getTrackbarPos('VAdd', TRACKBAR_WINDOW)
    # hsv_filter.vSub = cv.getTrackbarPos('VSub', TRACKBAR_WINDOW)

    # green text filter
    # hsv_filter.hMin = 27
    # hsv_filter.sMin = 0
    # hsv_filter.vMin = 0
    # hsv_filter.hMax = 73
    # hsv_filter.sMax = 255
    # hsv_filter.vMax = 251
    # hsv_filter.sAdd = 0
    # hsv_filter.sSub = 207
    # hsv_filter.vAdd = 53
    # hsv_filter.vSub = 0

    # hMin = 27
    # sMin = 0
    # vMin = 0
    # hMax = 73
    # sMax = 255
    # vMax = 251
    # sAdd = 0
    # sSub = 207
    # vAdd = 53
    # vSub = 0

    # yellow text
    # hsv_filter.hMin = 0
    # hsv_filter.sMin = 0
    # hsv_filter.vMin = 99
    # hsv_filter.hMax = 35
    # hsv_filter.sMax = 255
    # hsv_filter.vMax = 255
    # hsv_filter.sAdd = 0
    # hsv_filter.sSub = 102
    # hsv_filter.vAdd = 0
    # hsv_filter.vSub = 0
    # hMin = 0
    # sMin = 54
    # vMin = 102
    # hMax = 179
    # sMax = 65
    # vMax = 255
    # sAdd = 0
    # sSub = 33
    # vAdd = 63
    # vSub = 58

    # White text filter
    hsv_filter.hMin = 0
    hsv_filter.sMin = 0
    hsv_filter.vMin = 178
    hsv_filter.hMax = 180
    hsv_filter.sMax = 33
    hsv_filter.vMax = 255
    hsv_filter.sAdd = 25
    hsv_filter.sSub = 41
    hsv_filter.vAdd = 103
    hsv_filter.vSub = 0

    # hMin = 0
    # sMin = 0
    # vMin = 178
    # hMax = 180
    # sMax = 33
    # vMax = 255
    # sAdd = 25
    # sSub = 41
    # vAdd = 103
    # vSub = 0
    return hsv_filter


# hsv_filter = ()
def process_screen(link):
    response = requests.get(link)
    img_array = np.array(bytearray(response.content), dtype=np.uint8)
    img = cv.imdecode(img_array, cv.IMREAD_COLOR)

    # Call init_control_gui to show the trackbars
    init_control_gui()

    orig_height, orig_width = img.shape[:2]
    fixed_width = 3000
    ratio = fixed_width / float(orig_width)
    fixed_height = int(orig_height * ratio)
    img = cv.resize(img, (fixed_width, fixed_height))

    config = '-c char_whitelist=你爸爸野爹我命天破聪明绝顶的贪生恶杀abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ --oem 3 --psm 12'

    while True:
        # Define the hsv_filter based on the trackbar values
        hsv_filter = get_hsv_filter_from_controls()

        filtered_img = apply_hsv_filter(img, hsv_filter=hsv_filter)

        gray = cv.cvtColor(filtered_img, cv.COLOR_BGR2GRAY)
        thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]

        # text = pytesseract.image_to_string(filtered_img, lang='chi_sim', config=config)
        usernames = [result.split(":")[0].replace(" ", "") for result in text.split("\n") if ":" in result]

        clean_names = list(set(clean_screen(usernames)))

        # print("Names:", clean_names)

        cv.imshow('img', filtered_img)

        # Break the loop if 'q' key is pressed
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cv.destroyAllWindows()
    
    
    def clean_screen(lst):
        cleaned_screen = []
    case_name = set(name.lower() for name in name_cases)
    cleaned_list = [difflib.get_close_matches(item.lower(), case_name, n=1, cutoff=0.7)[0]
                    for item in lst if difflib.get_close_matches(item.lower(), case_name, n=1, cutoff=0.7)]
    return cleaned_list

# create gui window with controls for adjusting arguments in real-time


# given an image and an HSV filter, apply the filter and return the resulting image.
# if a filter is not supplied, the control GUI trackbars will be used
def apply_hsv_filter(original_image, hsv_filter=None):

    # convert image to HSV
    hsv = cv.cvtColor(original_image, cv.COLOR_BGR2HSV)

    # if we haven't been given a defined filter, use the filter values from the GUI
    if not hsv_filter:
        hsv_filter = get_hsv_filter_from_controls()

    # add/subtract saturation and value
    h, s, v = cv.split(hsv)
    s = shift_channel(s, hsv_filter.sAdd)
    s = shift_channel(s, -hsv_filter.sSub)
    v = shift_channel(v, hsv_filter.vAdd)
    v = shift_channel(v, -hsv_filter.vSub)
    hsv = cv.merge([h, s, v])

    # Set minimum and maximum HSV values to display
    lower = np.array([hsv_filter.hMin, hsv_filter.sMin, hsv_filter.vMin])
    upper = np.array([hsv_filter.hMax, hsv_filter.sMax, hsv_filter.vMax])
    # Apply the thresholds
    mask = cv.inRange(hsv, lower, upper)
    result = cv.bitwise_and(hsv, hsv, mask=mask)

    # convert back to BGR for imshow() to display it properly
    img = cv.cvtColor(result, cv.COLOR_HSV2BGR)

    return img

# https://stackoverflow.com/questions/49697363/shifting-hsv-pixel-values-in-python-using-numpy
def shift_channel( c, amount):
    if amount > 0:
        lim = 255 - amount
        c[c >= lim] = 255
        c[c < lim] += amount
    elif amount < 0:
        amount = -amount
        lim = amount
        c[c <= lim] = 0
        c[c > lim] -= amount
    return c