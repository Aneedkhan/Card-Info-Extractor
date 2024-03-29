
import cv2
import easyocr
import re
import tempfile
from django.shortcuts import render
import pytesseract


def extract_text_from_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th, threshed = cv2.threshold(gray, 127, 255, cv2.THRESH_TRUNC)
    extracted_text = pytesseract.image_to_string(threshed, lang="eng")
    return extracted_text

aadhar_number_pattern = r'\b\d{4}[\s.-]?\d{4}[\s.-]?\d{4}\b'
gender_pattern = r'\b(?:Male|Female|Other)\b'
dob_pattern = r'\b(\d{2}/\d{2}/\d{4}|\d{4})\b'
name_pattern = r'\b[A-Z][a-z]+(?: [A-Z][a-z]+)+\b'


def extract_aadhar_details(text):
    aadhar_number = re.search(aadhar_number_pattern, text)
    gender = re.search(gender_pattern, text)
    dob = re.search(dob_pattern, text)
    name = re.search(name_pattern, text)

    aadhar_details = {
        'Aadhar Number': aadhar_number.group() if aadhar_number else 'Not found',
        'Name': name.group() if name else 'Not found',
        'Gender': gender.group() if gender else 'Not found',
        'Date of Birth': dob.group() if dob else 'Not found'
    }

    return aadhar_details

def process_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image'].file.read()

        # Use tempfile to create a temporary file to save the image
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_image:
            temp_image.write(image)
            image_path = temp_image.name

        extracted_text = extract_text_from_image(image_path)
        extracted_details = extract_aadhar_details(extracted_text)

        one = extracted_details.get('Aadhar Number', '')
        two = extracted_details.get('Name', '') 
        three = extracted_details.get('Gender', '')
        four = extracted_details.get('Date of Birth', '')


        return render(request, 'result.html', {'aadhar_details': extracted_details, 'one': one, 'two': two, 'three': three,  'four': four})

    return render(request, 'index.html')