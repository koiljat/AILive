from flask import Flask, jsonify
import threading
import time
import random
import pandas as pd
import spacy
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from summary import summarizer
import torch
from auto_reply import auto_reply
import signal
import sys

app = Flask(__name__)

# Shared global variables
global_data = []
summary_text = ""
data_copy = []
aspect_sentiment_summary = ""

# Lock for synchronizing access to the global variables
lock = threading.Lock()

# Event to signal threads to stop
stop_event = threading.Event()

# Load NLP models
nlp = spacy.load("en_core_web_sm")

sa_model_name = "distilbert-base-uncased-finetuned-sst-2-english"
sa_tokenizer = AutoTokenizer.from_pretrained(sa_model_name)
sa_model = AutoModelForSequenceClassification.from_pretrained(sa_model_name)
device = "cuda" if torch.cuda.is_available() else "cpu"
sa = pipeline("sentiment-analysis", model=sa_model, tokenizer=sa_tokenizer, device=device)

# Dummy function to simulate emitting data from a CSV data stream
def csv_data_stream(dataframe, interval=1):
    for _, row in dataframe.iterrows():
        if stop_event.is_set():
            break
        yield row.to_dict()
        sleep_duration = random.uniform(0.1, interval)
        time.sleep(sleep_duration)

# Load your CSV data
df = pd.read_csv('./data/topical_chat.csv')

def emit_data():
    global global_data
    for data in csv_data_stream(df):
        if stop_event.is_set():
            break
        print(f"{data['message']}")
        with lock:
            global_data.append(data)

def extract_aspects_and_adjectives(text):
    doc = nlp(text)
    aspects = []
    adjectives = []
    for chunk in doc.noun_chunks:
        if chunk.root.pos_ == "PRON":
            continue
        aspect = chunk.root.text
        adjective = [child.text for child in chunk.root.children if child.dep_ == "amod"]
        aspects.append(aspect)
        adjectives.append(adjective[0] if adjective else "")
    return aspects, adjectives

def analyze_sentiment(aspects):
    results = [sa(aspect)[0] for aspect in aspects]
    return results

def format_aspects_sentiments(aspects, sentiments, adjectives):
    formatted_results = []
    for aspect, sentiment, adjective in zip(aspects, sentiments, adjectives):
        formatted_results.append(f"Aspect: {aspect}, Sentiment: {sentiment['label']}, Adjective: {adjective}")
    return "\n".join(formatted_results)

def sum_data():
    global global_data, summary_text, data_copy, aspect_sentiment_summary
    
    start_time = time.time()
    while not stop_event.is_set():
        time.sleep(1)  # Check every second to avoid busy-waiting
        with lock:
            if time.time() - start_time >= 5 and global_data:
                data_copy = global_data.copy()
                global_data = []
        if data_copy:
            text = " ".join([d['message'] for d in data_copy])
            summary = summarizer.invoke(text)
            aspects, adjectives = extract_aspects_and_adjectives(summary)
            sentiments = analyze_sentiment(aspects)

            aspect_sentiment_summary = format_aspects_sentiments(aspects, sentiments, adjectives)
            with lock:
                summary_text = summary  # Update the global summary_text
            data_copy = []
            start_time = time.time()

def reply():
    global global_data
    last_processed_index = -1
    while not stop_event.is_set():
        time.sleep(0.1)  # Check every 0.1 seconds to avoid busy-waiting
        with lock:
            if global_data and last_processed_index < len(global_data) - 1:
                for i in range(last_processed_index + 1, len(global_data)):
                    data = global_data[i]
                    message = data['message']
                    reply = auto_reply.get_auto_response(message)
                    if reply:
                        print(f"Bot: {reply}")
                        global_data.append({"message": reply, "is_bot": True})
                last_processed_index = len(global_data) - 1

@app.route('/summary', methods=['GET'])
def get_summary():
    with lock:
        return jsonify({
            "summary": summary_text,
            "aspect_sentiment_summary": aspect_sentiment_summary
        })
        
@app.route('/getChat', methods=['GET'])
def get_chat():
    with lock:
        return jsonify(global_data)

def signal_handler(signum, frame):
    print("Received shutdown signal. Stopping threads...")
    stop_event.set()

def start_background_tasks():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    thread_one = threading.Thread(target=emit_data)
    thread_two = threading.Thread(target=sum_data)
    thread_three = threading.Thread(target=reply)
    
    thread_one.start()
    thread_two.start()
    thread_three.start()

    return [thread_one, thread_two, thread_three]

if __name__ == '__main__':
    threads = start_background_tasks()
    try:
        app.run(host='0.0.0.0', port=5001)
    finally:
        print("Shutting down...")
        stop_event.set()
        for thread in threads:
            thread.join()
        print("All threads stopped. Exiting.")