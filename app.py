# app.py
import streamlit as st
from PIL import Image, ImageOps
import pytesseract
import cv2
import numpy as np
from pytesseract import TesseractNotFoundError

def main():
    st.title("Text Recognition from Image")
    st.write("Upload an image and the app will extract the text from it.")

    uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        if st.button('Recognize Text'):
            try:
                preprocessed_image = preprocess_image(image)
                text = extract_text(preprocessed_image)
                st.write("Extracted Text:")
                st.write(text)
            except TesseractNotFoundError:
                st.error("Tesseract OCR is not installed. Please make sure it's installed and configured correctly.")

def preprocess_image(image):
    # Convert image to grayscale
    gray = ImageOps.grayscale(image)

    # Convert image to numpy array
    img_array = np.array(gray)

    # Apply GaussianBlur to remove noise
    img_array = cv2.GaussianBlur(img_array, (5, 5), 0)

    # Apply thresholding to get a binary image
    _, img_array = cv2.threshold(img_array, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Convert back to PIL image
    preprocessed_image = Image.fromarray(img_array)

    return preprocessed_image

def extract_text(image):
    # Convert image to text using Tesseract OCR with custom configuration
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(image, config=custom_config)
    return text

if __name__ == "__main__":
    main()
