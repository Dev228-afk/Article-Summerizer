# Core Pkgs
import streamlit as st
from function import *
# EDA Pkgs
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
# Utils
from datetime import datetime
warnings.filterwarnings("ignore")

# page info setup
menu_items = {
	'Get help':'https://www.linkedin.com/in/dev-ansodariya-b616941b9/' ,
	'Report a bug': 'https://www.linkedin.com/in/dev-ansodariya-b616941b9/',
	'About': '''
	## My Custom App
	Some markdown to show in the About dialog.
	'''
}
#page configuration
st.set_page_config(page_title="Article Summerizer", page_icon="./favicon/favicon.ico",menu_items=menu_items)
st.set_option('deprecation.showPyplotGlobalUse', False)

def main():
        # This is used to hide the made with streamlit watermark
        hide_streamlit_style = """
                <style>
                footer {visibility: hidden;}
                </style>
                """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)

        # Article Summerizer heading
        st.markdown("<h1 style = 'color:gold; align:center; font-size: 40px;'> Article Summerizer</h1>", unsafe_allow_html=True)
        
        # control for Model Settings
        st.sidebar.markdown("<h4 style = 'color:gold; align:center; font-size: 20px;'> Model Settings</h1>", unsafe_allow_html=True)
        max_length= st.sidebar.slider("Maximum length of the generated text is  500 tokens",min_value=100,max_value=500)
        min_length= st.sidebar.slider("Minimum length of the generated text",min_value=30)
        model_type = st.sidebar.selectbox("Model type", options=["Bart","T5"])
        
        # This function is used to upload a .txt, .pdf, .docx file for summarization
        upload_doc = st.file_uploader("Upload a .txt, .pdf, .docx file for summarization")
        
        st.markdown("<h3 style='text-align: center; color: gold;'>OR</h3>",unsafe_allow_html=True)

        #This function is used to Type your Message... (text area)
        plain_text = st.text_area("Type your Message...",height=200)

        # this is used to control the logic of the code
        if upload_doc:
            clean_text = preprocess_plain_text(extract_text_from_file(upload_doc))
        else:
            clean_text = preprocess_plain_text(plain_text)
            
        summarize = st.button("Summarize...")        
        
        # called on toggle button [summarize]
        if summarize:
            if model_type == "Bart":
                text_to_summarize = clean_text

                with st.spinner(
                    text="Loading Bart Model and Extracting summary. This might take a few seconds depending on the length of your text..."):
                    summarizer_model = bart()
                    summarized_text = summarizer_model(text_to_summarize, max_length=max_length ,min_length=min_length)
                    summarized_text = ' '.join([summ['summary_text'] for summ in summarized_text])
            
            elif model_type == "T5":
                text_to_summarize = clean_text

                with st.spinner(
                    text="Loading T5 Model and Extracting summary. This might take a few seconds depending on the length of your text..."):
                    summarizer_model = t5()
                    summarized_text = summarizer_model(text_to_summarize, max_length=max_length, min_length=min_length)
                    summarized_text = ' '.join([summ['summary_text'] for summ in summarized_text]) 

            res_col1 ,res_col2 = st.columns(2)
            with res_col1:
                st.subheader("Generated Text Visualization")
                # Create and generate a word cloud image:
                wordcloud = WordCloud().generate(summarized_text)
                # Display the generated image:
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis("off")
                plt.show()
                st.pyplot()
                summary_downloader(summarized_text)   
                
            with res_col2:
                st.subheader("Summarized Text Output")
                st.success("Summarized Text")
                st.write(summarized_text)

if __name__ == '__main__':
	main()