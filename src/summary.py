import threading
import time
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from llm import llm

template = """
Summarize the chat based on the following chat input: {context}

Keep the summary point to 3, the template in the example below. Do not add in other comment.

Do not need to include "Summary:" in the header

Example:

1. Point 1
2. Point 2
3. Point 3
"""

prompt = ChatPromptTemplate.from_template(template)

summarizer = (
    {"context": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

lock = threading.Lock()

def sum_data(summarizer=summarizer):
    global global_data, summary_text
    global data_copy
    global message_queue
    
    start_time = time.time()
    while True:
        time.sleep(1)  # Check every second to avoid busy-waiting
        with lock:
            if time.time() - start_time >= 5 and global_data:
                data_copy = global_data.copy()  # Make a copy of the data
                global_data = []  # Clear the global data
        if data_copy:
            text = " ".join([d['message'] for d in data_copy])
            summary = summarizer.invoke(text)
            
            summary_text = summary
            data_copy = []  # Clear the data copy after processing
            start_time = time.time()
            