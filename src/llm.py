from langchain_huggingface import HuggingFaceEndpoint

import os

huggingfacehub_api_token = os.getenv('HUGGINGFACEHUB_API_TOKEN')

llm = HuggingFaceEndpoint(repo_id='meta-llama/Meta-Llama-3-8B-Instruct', huggingfacehub_api_token=huggingfacehub_api_token)


