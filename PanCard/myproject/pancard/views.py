import cv2
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

def extract_pan_details(text):
    pan_name_pattern = re.compile(r"Name\s+([A-Z\s]+)")
    father_name_pattern = re.compile(r"Father's Name\s+(\b[A-Z]+(?: [A-Z]+)+\b)")
    dob_pattern = re.compile(r'\b(?:0[1-9]|1[0-2])/(?:0[1-9]|[12][0-9]|3[01])/(?:19|20)\d{2}\b')
    pan_number_pattern = re.compile(r'\b[A-Z]{5}[0-9]{4}[A-Z]\b')

    pan_name = pan_name_pattern.search(text.replace('\n', ' '))
    father_name = father_name_pattern.search(text.replace('\n', ' '))
    dob = dob_pattern.search(text.replace('\n', ' '))
    pan_number = pan_number_pattern.search(text.replace('\n', ' '))

    pan_details = {
        'PAN Holder Name': pan_name.group(1) if pan_name else 'Not found',
        'Father\'s Name': father_name.group(1) if father_name else 'Not found',
        'Date of Birth': dob.group() if dob else 'Not found',
        'PAN Number': pan_number.group() if pan_number else 'Not found'
    }

    return pan_details

def process_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image'].file.read()

        # Use tempfile to create a temporary file to save the image
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_image:
            temp_image.write(image)
            image_path = temp_image.name

        extracted_text = extract_text_from_image(image_path)
        extracted_details = extract_pan_details(extracted_text)

        abc = extracted_details.get('PAN Holder Name', '')
        bcd = extracted_details.get('Father\'s Name', '')
        efg = extracted_details.get('Date of Birth', '')
        hij = extracted_details.get('PAN Number', '')

        return render(request, 'result1.html', {'pan_details': extracted_details, 'abc': abc, 'bcd': bcd, 'efg': efg, 'hij': hij})

    return render(request, 'pan_home.html')
