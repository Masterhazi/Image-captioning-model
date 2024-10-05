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

#configure genai 

genai.configure(api_key=os.getenv('GOOGLE-API-KEY'))

#configuring the webpage 
st.markdown(":blue-background[**MICA**] :blue[AI] :blue[C]aption :blue[M]aker")
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