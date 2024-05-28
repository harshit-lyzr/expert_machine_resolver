from gptvision import GPTVISION
import streamlit as st
from PIL import Image
import utils
import base64
import os

st.set_page_config(
    page_title="Expert Machine Resolver",
    layout="centered",  # or "wide"
    initial_sidebar_state="auto",
    page_icon="lyzr-logo-cut.png",
)

st.markdown(
    """
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

image = Image.open("lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Expert Machine Resolver👷‍")
st.sidebar.markdown("## Welcome to the Expert Machine Resolver!")
st.sidebar.markdown("In this App you need to Upload Your machine image and ask question. This app will gives you repairing tips and troubleshooting tips.")

api = st.sidebar.text_input("Enter Your OPENAI API KEY HERE",type="password")

if api:
        openai_4o_model = GPTVISION(api_key=api,parameters={})
else:
        st.sidebar.error("Please Enter Your OPENAI API KEY")

data_directory = "data"
os.makedirs(data_directory, exist_ok=True)

def encode_image(image_path):
        with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')


uploaded_files = st.file_uploader("Upload Your Machine image", type=['png', 'jpg'])
prompt = st.text_area("Enter Question: ")
example = f"""
You are an Expert Electrical Engineer.Your Task is to Give answer related to electrical machines repairing.
Follow Below steps:
1/ ANALYZE image and get insights about it.
2/ Understand Question entered by user.
3/ BASED ON analyzing image and understanding question you need to give answer in simple language.
    Give instruction about how to repair given electric machines by themselves
4/ IF IMAGE IS NOT RELATED TO Electrical machines THEN REPLY "Please Upload image Related to electric machine"

user question: {prompt}
"""
if uploaded_files is not None:
        st.success(f"File uploaded: {uploaded_files.name}")
        file_path = utils.save_uploaded_file(uploaded_files)
        if file_path is not None:
            st.sidebar.image(file_path)
            if st.button("Generate"):
                encoded_image = encode_image(file_path)
                planning = openai_4o_model.generate_text(prompt=prompt, image_url=encoded_image)
                st.markdown(planning)



