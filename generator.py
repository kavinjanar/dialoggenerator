import os
import dotenv
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# Load environment variables from .env file FIRST
dotenv.load_dotenv()

# Set the API key - you should put this in your .env file instead of hardcoding
os.environ['GOOGLE_API_KEY'] = "AIzaSyDUE5Ppp7dueqlFUyaaWCqmiDcy51HNuPY"

# Initialize Google's Gemini model AFTER setting the API key
gemini_model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest")

dialog_template_instruction = """Give me {turns} dialog turns between these two character regarding the rise of AI: {first} and {second}.

Please follow these instructions:
1. Limit each character's response to a maximum of 50 words.
2. If the character is a known fictional character, answer in their tone, style, and personality.
3. Ensure the dialog is engaging and coherent.
4. Do not include any personal information or real-life references.
5. Make sure the dialog is fun and entertaining.

"""

dialog_prompt = PromptTemplate(
    input_variables=["first", "second", "turns"],
    template=dialog_template_instruction
)

# Create the chain
dialog_chain = dialog_prompt | gemini_model

# Streamlit UI
st.header("Dialog Generator")

st.subheader("Generate a dialog between two fictional characters")

first_character = st.text_input("First Character Name", "Alice")
second_character = st.text_input("Second Character Name", "Bob")

number_of_turns = st.slider("Number of Dialog Turns", 1, 10, 5)

# Fix: Only one button, not two
if st.button("Generate Dialog"):
    if first_character and second_character:
        with st.spinner("Generating dialog..."):
            try:
                dialog = dialog_chain.invoke({
                    "first": first_character,
                    "second": second_character,
                    "turns": number_of_turns
                })
                st.write(dialog.content)
            except Exception as e:
                st.error(f"Error generating dialog: {str(e)}")
    else:
        st.error("Please enter both character names.")