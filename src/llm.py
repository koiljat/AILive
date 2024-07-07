from langchain_huggingface import HuggingFaceEndpoint
import ollama
from langchain_community.chat_models import ChatOllama

import os

huggingfacehub_api_token = os.getenv('HUGGINGFACEHUB_API_TOKEN')

llm = ChatOllama(model='llama3', temperature=0)


