import streamlit as st
from streamlit_extras.stylable_container import stylable_container

from chat_pipeline_task1 import Pipeline as p1
from chat_pipeline_task2 import Pipeline as p2

chat_bot1 = p1("Chat_1")
chat_bot2 = p2("Chat_2")


def file_uploader(cont, label):
    with cont:
        uploaded_file = st.file_uploader(label)
        if uploaded_file is not None:
            with open(uploaded_file.name, mode='wb') as w:
                w.write(uploaded_file.getvalue())
            return chat_bot1._load(uploaded_file.name)
        

st.set_page_config(layout="wide")

# CSS to set font globally (replace with your font source)
st.markdown("""
<style>
body {
  font-family: 'Noto Sans Gurmukhi', sans-serif;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.write('')

with col2:
    st.write('')
    #st.markdown("<h1 style='text-align: center; top: -10'>Legal (AI)d</h1>", unsafe_allow_html=True)
with col3:
    st.write('')
    st.write('')
    st.write('')
    # Title wrapped in h1 with CSS class
    title_text = "Legal <span style='color:green'>AI</span>d"
    st.markdown(f"<h1 class='custom-title'>{title_text}</h1>", unsafe_allow_html=True)

    # CSS to style the title element (replace with your font source)
    st.markdown("""
    <style>
    .custom-title {
    font-family: 'Noto Sans Gurmukhi', sans-serif;
    font-size: 48px;
    }
    </style>
    """, unsafe_allow_html=True)
with col4:
    st.write('')

with col5:
    st.image("logo_hackathon.png", width=200)

#st.markdown("<h1 style='text-align: center; top: -10'>Legal (AI)d</h1>", unsafe_allow_html=True)
            # <span style="font-family: Lora; font-size: 1em;">
# st.markdown("""
#             ##### This app enables:
    
#                 1. Checking consistency between bills and their explanatory notes.
#                 2. Finding past bills relevant to a given legislation, and find possible aspects missed in the given legislation as discussed in each of the relevant ones.
#                 3. Finding the past bills that may contradict with the proposals of the given legislation.  
#             """, unsafe_allow_html=True)

with st.container(height=190, border=True):
    st.markdown("#### Uploads")
    col1, col2 = st.columns(2)
    bill = file_uploader(col1, "Bill")
    xnote = file_uploader(col2, "Explanatory Notes")

with st.container(height=310, border=True):
    st.markdown("#### Analysis")
    tab1, tab2 = st.tabs(["Consistency Check", "Possible Weaknesses"])#, "Contradiction Checker"])
    # task 1
    with tab1:
        #st.markdown("##### Found inconsistencies:")
        with stylable_container(key="output", css_styles="""{background-color: lightyellow}"""):
            answer = ""
            if bill is not None and xnote is not None:
                answer = chat_bot1.ask(question="Check for inconsistencies between the provided bill and its explanatory note overall and also section by section and part by part.", bills=bill, xnotes=xnote)
            st.write(answer)

    # task 2
    with tab2:
        #st.markdown("##### Potential Questions:")
        with stylable_container(key="output", css_styles="""{background-color: lightyellow}"""):
            answer = ""
            if bill is not None:
                answer = chat_bot2.ask(documents=bill)
                for qi, ques in enumerate(answer.split('?')):
                    if ques:
                        st.markdown(f"{ques}?")
