import cv2
import pytesseract
import numpy
import pyautogui
import win32gui
import time
import difflib
import json
import keyboard
from PIL import Image, ImageDraw

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

tower_window = None

# Find the Tower Unite window
def findTowerWindow(hwnd, ctx):
    global tower_window

    if win32gui.GetWindowText(hwnd).strip() == "Tower Unite":
        tower_window = hwnd


# Read some text from an image
def readImageText(image, replace_newline=False, psm=False):
    config = ""
    if psm:
        config = "--psm 6"

    read_text = pytesseract.image_to_string(image, lang="eng", config=config)
    read_text.replace("|", "I")
    if replace_newline:
        read_text.replace("\n", " ")

    return read_text


def processCVImage(screenshot, output=None):
    image = numpy.array(screenshot)
    image = image[:, :, ::-1].copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.threshold(image, 80, 255, cv2.THRESH_BINARY_INV)[1]

    if output:
        cv2.imwrite(output + ".jpg", image)
    return image


def _load_csv2(img, grayscale=False):
    img_array = numpy.array(img.convert("RGB"))
    img_cv = img_array[:, :, ::-1].copy()
    if grayscale:
        img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

    return img_cv


def locateSubImage(haystack, needle, w, h):
    # Load image in CV2 form
    haystack = _load_csv2(haystack)
    needle = _load_csv2(needle)
    height, width = haystack.shape[:2]

    # Find position
    result = cv2.matchTemplate(haystack, needle, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    return min_loc


def word_distance(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()


def load_questionbank():
    with open("questions.json") as f:
        return json.load(f)


def getWindowScreenshot(start_time):
    # Bring Tower Unite window to the front
    win32gui.EnumWindows(findTowerWindow, None)
    win32gui.SetForegroundWindow(tower_window)
    start_time = time.time()

    # Screenshot the Tower Unite window
    pos = win32gui.GetWindowRect(tower_window)
    screenshot = pyautogui.screenshot(
        region=(pos[0], pos[1], pos[2] - pos[0], pos[3] - pos[1]),
    ).resize((1600, 900))
    screenshot.save(str(start_time) + "_ss.png")

    return screenshot


def findMarkerPosition(start_time, screenshot):
    # Locate the marker
    template = Image.open("marker.jpg")
    screenshot_cropped = screenshot.crop((0, 0, 1600, 1000))
    marker_pos = locateSubImage(
        screenshot_cropped, template, template.width, template.height
    )
    return marker_pos


def readQuestion(start_time, screenshot, marker_pos):
    # Screenshot the question title
    question_screenshot = screenshot.crop(
        (
            marker_pos[0] - 100,
            marker_pos[1] - 75,
            marker_pos[0] - 100 + 1100,
            marker_pos[1] - 75 + 135,
        )
    )

    left = 0
    right = 400
    top = question_screenshot.height - 45
    bottom = question_screenshot.height

    draw = ImageDraw.Draw(question_screenshot)
    draw.rectangle((left, top, right, bottom), fill=(255, 255, 255))

    left = int(question_screenshot.width / 2) - 40
    right = question_screenshot.width
    top = 0
    bottom = 55
    draw.rectangle((left, top, right, bottom), fill=(255, 255, 255))

    question_image = processCVImage(
        question_screenshot, output=str(start_time) + "_question",
    )
    return readImageText(question_image, psm=True)


def readAnswers(start_time, screenshot, marker_pos):
    # Screenshot the answers block
    answers_screenshot = screenshot.crop(
        (
            marker_pos[0] + 40,
            marker_pos[1],
            marker_pos[0] + 40 + 450,
            marker_pos[1] + 0 + 220,
        )
    )

    # Block out the top left corner since the question title ends up there
    left = answers_screenshot.width - 150
    right = answers_screenshot.width
    top = 0
    bottom = 50

    draw = ImageDraw.Draw(answers_screenshot)
    draw.rectangle((left, top, right, bottom), fill=(255, 255, 255))

    answers_image = processCVImage(
        answers_screenshot, output=str(start_time) + "_answers"
    )
    answers_text = readImageText(answers_image)
    return answers_text.split("\n")


if __name__ == "__main__":
    while True:
        # Wait until F1 is pressed
        while True:
            if keyboard.is_pressed("f1"):
                break

        start_time = time.time()
        screenshot = getWindowScreenshot(start_time)
        # screenshot = Image.open("screenshot.png")
        marker_pos = findMarkerPosition(start_time, screenshot)
        question_bank = load_questionbank()

        question_text = readQuestion(start_time, screenshot, marker_pos).strip()
        answers = readAnswers(start_time, screenshot, marker_pos)

        # Run through the questions data bank and get the closest question
        best_difference1 = 0
        best_question = ""
        for question in question_bank:
            difference = word_distance(question_text, question)
            if difference > best_difference1:
                best_question = question
                best_difference1 = difference

                # Break immediately if we're 65% confident
                if difference > 0.65:
                    break

        # Find out which answer text is closest to the correct answer
        correct_answer = question_bank[best_question]
        best_difference2 = 0
        best_answer = -1
        for k, my_answer in enumerate(answers):
            difference = word_distance(my_answer, correct_answer)
            if difference > best_difference2:
                best_answer = k
                best_difference2 = difference

        print(answers)
        print(best_question, best_difference1)
        print(best_answer, answers[best_answer])
        print("Time: ", time.time() - start_time)

        buttons = ["1", "2", "3", "4"]
        pyautogui.press(buttons[best_answer])
