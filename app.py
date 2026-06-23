#Importing necessary libraries
import os
import time
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain.messages import HumanMessage,SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
load_dotenv()


#getting our api key for our llm model
api_key=os.getenv('GROQ_API')

#We are Using GROQ LLM (model='llama-3.1-8b-instant)
llm=ChatGroq(model="llama-3.1-8b-instant",temperature=0.7,groq_api_key=api_key)

#Creating Prompt
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a conversational AI assistant.

Instructions:
- Answer questions based on the conversation context.
- Be friendly, natural, and engaging.
- Keep answers short for simple questions and detailed for complex ones.
- Ask clarifying questions when the user's query is ambiguous.
- Do not provide false information.
- If you don't know the answer, say:
  "I don't have enough information to answer that accurately."
- Maintain context across the conversation.
- Format responses using markdown when useful.
        """
    ),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

#Creating Our Output Parser for (To Extract text content from model outputs as a string.)
parser=StrOutputParser()

#Get the session id for the chat
if "store" not in st.session_state:
    st.session_state.store = {}
    
def get_session_history(session_id: str):
    if session_id not in st.session_state.store:
        st.session_state.store[session_id] = InMemoryChatMessageHistory()
    return st.session_state.store[session_id]

#Set the configuration
config={"configurable": {"session_id": "user1"}}

#Making Our Chain using LECL
chain=prompt|llm|parser

#Chain with history
chain_with_history=RunnableWithMessageHistory(chain,get_session_history=get_session_history,input_messages_key="input",history_messages_key='history')

#Now Our Streamlit App
st.set_page_config(page_title="Groq Chatbot",page_icon="🤖",layout="wide",initial_sidebar_state="expanded")

with st.sidebar:
    st.header("CHATBOT🤖")
    st.write(f"**Model**: llama-3.1-8b-instant")
    st.write("Temperature: 0.7")
    st.info("Built by Aayush Acharya")
    
st.markdown(
    "<h1 style='text-align:center;color:#4F8BF9;'>🤖 Groq Chatbot</h1>",
    unsafe_allow_html=True
)
st.header("Hey! Whats Your Query.😊")

question=st.text_input("Enter Your Question:",placeholder="Hi,Your Question Here.")

if st.button("Answer This"):
    with st.spinner("🤖 Thinking..."):
        time.sleep(2)
        if question=="":
            st.warning("Please Enter Your Question⚠️")
        else:
            response = chain_with_history.invoke({"input": question},config=config)
            st.write(response)
st.divider()
st.write(" History")

if "user1" in st.session_state.store:
    for msg in st.session_state.store["user1"].messages:

        if msg.type == "human":
            st.markdown(f"**You:** {msg.content}")

        else:
            st.markdown(f"**AI:** {msg.content}")

st.divider()