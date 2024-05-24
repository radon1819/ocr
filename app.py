import streamlit as st
from PIL import Image
import pytesseract
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
                text = extract_text(image)
                st.write("Extracted Text:")
                st.write(text)
            except TesseractNotFoundError:
                st.error("Tesseract OCR is not installed. Please make sure it's installed and configured correctly.")

def extract_text(image):
    # Convert image to text using Tesseract OCR with custom configuration
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(image, config=custom_config)
    return text

if __name__ == "__main__":
    main()
