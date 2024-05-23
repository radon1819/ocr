# app.py
import streamlit as st
from PIL import Image, ImageDraw
import pytesseract
from pytesseract import TesseractNotFoundError

def main():
    st.title("Text Recognition from Image")
    st.write("Upload an image and select an area to extract the text from it.")

    uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Add option to select an area
        st.write("Select an area on the image to recognize text:")
        drawing_mode = st.checkbox("Enable Drawing", False)
        selected_area = st.empty()

        if drawing_mode:
            with selected_area:
                draw = ImageDraw.Draw(image)
                selected_area.image(image)

                # Allow user to draw bounding box
                cropped_image = st.image(image, caption="Selected Area", use_column_width=True, clamp=True, channels="RGB")

                # Hide the cropped image if the user hasn't drawn anything yet
                if st.button("Extract Text"):
                    if st._is_running_with_streamlit:
                        cropped_image.empty()
                        selected_area.empty()
                        cropped_image = None
                        selected_area = None
            st.image(image, caption='Uploaded Image', use_column_width=True)

        if st.button('Recognize Text'):
            try:
                text = extract_text(image)
                st.write("Extracted Text:")
                st.write(text)
            except TesseractNotFoundError:
                st.error("Tesseract OCR is not installed. Please make sure it's installed and configured correctly.")

def extract_text(image):
    # Convert image to text using Tesseract OCR
    text = pytesseract.image_to_string(image)
    return text

if __name__ == "__main__":
    main()
