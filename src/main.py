from flask import Flask, jsonify
import threading
import time
import random
import pandas as pd
from summary import summarizer  # Import your summarizer

app = Flask(__name__)

# Shared global variables
global_data = []
summary_text = ""
data_copy = []

# Lock for synchronizing access to the global variables
lock = threading.Lock()

# Dummy function to simulate emitting data from a CSV data stream
def csv_data_stream(dataframe, interval=1):
    for _, row in dataframe.iterrows():
        yield row.to_dict()
        sleep_duration = random.uniform(0.1, interval)
        time.sleep(sleep_duration)

# Load your CSV data
df = pd.read_csv('./data/topical_chat.csv')

def emit_data():
    global global_data
    for data in csv_data_stream(df):
        print(f"{data['message']}")
        with lock:
            global_data.append(data)

def sum_data():
    global global_data, summary_text, data_copy
    
    start_time = time.time()
    while True:
        time.sleep(1)  # Check every second to avoid busy-waiting
        with lock:
            if time.time() - start_time >= 5 and global_data:
                data_copy = global_data.copy()
                global_data = []
        if data_copy:
            text = " ".join([d['message'] for d in data_copy])
            summary = summarizer.invoke(text)
            with lock:
                summary_text = summary  # Update the global summary_text
            print(f"\n[Summary]\n{summary}\n")
            data_copy = []
            start_time = time.time()

@app.route('/summary', methods=['GET'])
def get_summary():
    with lock:
        return jsonify({"summary": summary_text})

def start_background_tasks():
    thread_one = threading.Thread(target=emit_data)
    thread_two = threading.Thread(target=sum_data)
    thread_one.start()
    thread_two.start()

if __name__ == '__main__':
    start_background_tasks()
    app.run(host='0.0.0.0', port=5000)