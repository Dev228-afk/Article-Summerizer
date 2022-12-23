# Core Pkgs
import streamlit as st
from transformers import pipeline
from PyPDF2 import PdfFileReader
import docx2txt
import base64
import  re
import sqlite3
import time
from io import StringIO
import warnings
warnings.filterwarnings("ignore")

time_str = time.strftime("%Y%m%d-%H%M%S")
# Loading function the model pipeline from huggingface model
@st.cache(allow_output_mutation=True)
def bart():
    ''' Loading bart model using pipeline api '''
    summarizer = pipeline('summarization',model='facebook/bart-large-cnn')
    return summarizer
    
def t5():
    ''' Loading t5 model using pipeline api '''
    summarizer = pipeline("summarization", model="t5-base", tokenizer="t5-base")
    return summarizer

# def pegasus():
#     ''' Loading pegasus model using pipeline api '''
#     summarizer = pipeline('summarization',model='google/pegasus-xsum')
#     return summarizer

def preprocess_plain_text(x):

    x = x.encode("ascii", "ignore").decode()  # unicode
    x = re.sub(r"https*\S+", " ", x)  # url
    x = re.sub(r"@\S+", " ", x)  # mentions
    x = re.sub(r"#\S+", " ", x)  # hastags
    x = re.sub(r"\s{2,}", " ", x)  # over spaces
    x = re.sub("[^.,!?A-Za-z0-9]+", " ", x)  # special charachters except .,!?

    return x

def extract_pdf(file):
    
    '''Extract text from PDF file'''
    
    pdfReader = PdfFileReader(file)
    count = pdfReader.numPages
    all_text = ""
    for i in range(count):
        page = pdfReader.getPage(i)
        all_text += page.extractText()

    return all_text


def extract_text_from_file(file):

    '''Extract text from uploaded file'''

    # read text file
    if file.type == "text/plain":
        # To convert to a string based IO:
        stringio = StringIO(file.getvalue().decode("utf-8"))

        # To read file as string:
        file_text = stringio.read()

    # read pdf file
    elif file.type == "application/pdf":
        file_text = extract_pdf(file)

    # read docx file
    elif (
        file.type
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ):
        file_text = docx2txt.process(file)

    return file_text

def summary_downloader(raw_text):
    
	b64 = base64.b64encode(raw_text.encode()).decode()
	new_filename = "new_text_file_{}_.txt".format(time_str)
	st.markdown("#### Download Summary as a File ###")
	href = f'<a href="data:file/txt;base64,{b64}" download="{new_filename}">Click to Download!!</a>'
	st.markdown(href,unsafe_allow_html=True)


# Storage in A Database
conn = sqlite3.connect('summarizer_database.db',check_same_thread=False)
c = conn.cursor() 
    # Create Fxn From SQL
def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS TextTable(text_to_summarize TEXT,summarized_text TEXT,postdate DATE)')


def add_data(text_to_summarize,summarized_text,postdate):
    c.execute('INSERT INTO TextTable(text_to_summarize,summarized_text,postdate) VALUES (?,?,?)',(text_to_summarize,summarized_text,postdate))
    conn.commit()

def view_all_data():
	c.execute("SELECT * FROM TextTable")
	data = c.fetchall()
	return data