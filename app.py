import streamlit as st
from streamlit_extras.stylable_container import stylable_container

from govchat.chat_pipeline import Pipeline

chat_bot = Pipeline('current_chatbot')


def file_uploader(cont, label):
    with cont:
        uploaded_file = st.file_uploader(label)
        if uploaded_file is not None:
            with open(uploaded_file.name, mode='wb') as w:
                w.write(uploaded_file.getvalue())
            return chat_bot._load(uploaded_file.name)


st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center; color: black; top: -10'>Bill Challenger</h1>", unsafe_allow_html=True)
st.markdown("""
            #### This app enables:

                1. Checking consistency between bills and their explanatory notes.
                2. Finding past bills relevant to a given legislation, and find possible aspects missed in the given legislation as discussed in each of the relevant ones.
                3. Finding the past bills that may contradict with the proposals of the given legislation.  
            """)

with st.container(height=190, border=True):
    st.markdown("#### Uploads")
    col1, col2 = st.columns(2)
    bill = file_uploader(col1, "Bill")
    xnote = file_uploader(col2, "Explanatory Notes")

with st.container(height=310, border=True):
    st.markdown("#### Analysis")
    tab1, tab2, tab3 = st.tabs(["Consistency Checker", "Relevance+Coverage Checker", "Contradiction Checker"])
    # task 1
    with tab1:
        st.markdown("##### Found inconsistencies:")
        with stylable_container(key="output", css_styles="""{background-color: lightyellow}"""):
            answer = chat_bot.ask(question="Check for inconsistencies between the provided bill and its explanatory note.", bills=bill, xnotes=xnote)
            st.write(answer)

    # task 2
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            col1.markdown("##### Relevant previous bills:")
            with stylable_container(key="output", css_styles="""{background-color: lightyellow}"""):
                st.write("LLM output as a list")
                for i in ["bill 1", "bill 2", "bill 3"]:
                    st.markdown("- " + i)

        with col2:
            col2.markdown("##### Missed aspects from the highlighted bill:")
            with stylable_container(key="output", css_styles="""{background-color: lightyellow}"""):
                st.write("LLM output as a list")
                for i in ["aspect 1", "aspect 2", "aspect 3"]:
                    st.markdown("- " + i)
