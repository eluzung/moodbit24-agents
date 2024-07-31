import os
import getpass
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

class LangchainOpenAI:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "API_KEY is missing from the environment variables.")
        
        self.llm = ChatOpenAI(temperature=0.0, model="gpt-4-turbo", api_key=api_key)
        
