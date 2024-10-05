#Application that can take the image 
# we write a prompt and then LLm should connect 
#the prompt with the image 
#and generate output

import streamlit as st
import google.generativeai as genai
import os 
from dotenv import load_dotenv
load_dotenv() #Enable the local environment variables
from PIL import Image #this will store the image
from io import StringIO
import pandas as pd
import numpy as np
from fpdf import  FPDF


#configure genai 

genai.configure(api_key=os.getenv('GOOGLE-API-KEY'))

#configuring the webpage 
st.markdown("""
    <h1 style='text-align: left; color: #2196F3;'>
    <span style="background-color: #E3F2FD; padding: 10px; border-radius: 5px;"><b>MICA</b></span> 
    <span style='color: #2196F3;'>AI</span> 
    <span style='color: #2196F3;'>Caption</span> 
    <span style='color: #2196F3;'>Maker</span>
    </h1>
""", unsafe_allow_html=True)
st.caption('AI powered tool to process your images and give output anything you need')

st.markdown("""<hr style="height:3px;border:none;color:#a5d6ff;background-color:#a5d6ff;" /> """, unsafe_allow_html=True)

user_input = st.text_input('''This is a simple application that uses Google's LLM to generate captions for images''')

with st.sidebar:
    uploaded_image = st.file_uploader("Choose an image", type=["jpg", "png", 'jpeg'])
if uploaded_image is not None:
    st.image(uploaded_image, caption = 'image uploaded', use_column_width= True)

enable = st.checkbox("Enable camera")
picture = st.camera_input("Take a picture", disabled=not enable)

if picture:
    st.image(picture, caption = 'image uploaded',  use_column_width= True)


if uploaded_image is None:
    uploaded_image = picture
else:
    uploaded_image = uploaded_image


if uploaded_image is not None:
    # To read image file buffer as a PIL Image:
    img = Image.open(uploaded_image)



demo_template = f'''Describe the components with clear divisions in each section in the  give a feedback about how the image can be improved 
                        next time, also provide 5 lines of description about  the image in line  with this request as well {user_input} 
                        at the end thank the user for using MICA and end with a  positive note of a poetry'''


#create a function for response
def gemini_response(user_input, img):
    model = genai.GenerativeModel(model_name= 'gemini-1.5-flash')
    if user_input!="":
        response = model.generate_content([demo_template, img])
    else:
        response = model.generate_content([img])
    return response.text

#Create a button

submit = st.button("Caption dedo", type="primary")

if submit:
    response = gemini_response(user_input=demo_template, img = img)
    st.subheader('The Response is:', divider = True)
    st.write(response)
    
    def save_to_pdf(text):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, text)
            
            # Save the file
            pdf_output = "generated_caption.pdf"
            pdf.output(pdf_output)
            return pdf_output

        # Provide a download button for the PDF
    if response is not None:
        pdf_file = save_to_pdf(response)
        with open(pdf_file, "rb") as pdf:
            st.download_button(
                label="Download Caption as PDF",
                data=pdf,
                file_name="MICA_caption.pdf",
                mime="application/pdf"
                )