import os
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI

# load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def get_pdf_text(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    return "".join(page.extract_text() for page in pdf_reader.pages)

def get_text_chunks(text, chunk_size=1000, chunk_overlap=200):
    text_chunks = []
    position = 0
    while position < len(text):
        start_index = max(0, position - chunk_overlap)
        end_index = position + chunk_size
        chunk = text[start_index:end_index]
        text_chunks.append(chunk)
        position = end_index - chunk_overlap
    return text_chunks

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    return vector_store

def get_conversation_chain(vectorstore):
    model_prams = {"temperature": 0.23, "max_length": 4096}
    llm = OpenAI(openai_api_key=openai_api_key, model="text-davinci-003", **model_prams)
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    return ConversationalRetrievalChain.from_llm(llm=llm, retriever=vectorstore.as_retriever(), memory=memory)

def handle_userinput(user_question):
    if st.session_state.conversation is not None:
        response = st.session_state.conversation.predict(input=user_question)
        st.write(response['answer'])

def main():
    st.set_page_config(page_title="PDF Chatbot", page_icon=":robot_face:", layout="wide")
    st.title("PDF Chatbot")
    st.subheader("Ask me anything about your PDF file")

    pdf_file = st.file_uploader("Upload a PDF file", type="pdf")
    if pdf_file:
        text = get_pdf_text(pdf_file)
        text_chunks = get_text_chunks(text)
        vectorstore = get_vectorstore(text_chunks)
        st.session_state.conversation = get_conversation_chain(vectorstore)
        user_question = st.text_input("Your question:")
        if user_question:
            handle_userinput(user_question)

if __name__ == '__main__':
    main()