import spacy
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments, pipeline
from datasets import load_dataset, Dataset
import torch
import pandas as pd

# Set device to CPU explicitly
device = torch.device("cpu")

# Load Spacy model for aspect extraction
nlp = spacy.load("en_core_web_sm")

# Load pre-trained BERT model and tokenizer for sentiment analysis
model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=5)  # Ensure num_labels matches your task

# Move model to CPU
model.to(device)

# Load your domain-specific dataset
dataset = load_dataset('csv', data_files={'train': '../data/train.csv', 'test': '../data/test.csv'})

# Filter out rows with None values
def filter_none_values(data):
    # Convert to pandas DataFrame for easy filtering
    df = pd.DataFrame(data)
    df = df.dropna(subset=['message', 'rating'])  # Drop rows with any None values in specific columns
    return Dataset.from_pandas(df)

dataset['train'] = filter_none_values(dataset['train'])
dataset['test'] = filter_none_values(dataset['test'])

# Preprocess the dataset
def preprocess_function(examples):
    inputs = tokenizer(examples['message'], padding="max_length", truncation=True)
    inputs['labels'] = [(rating - 1) for rating in examples['rating']]  # Ensure labels are zero-indexed
    return inputs

encoded_dataset = dataset.map(preprocess_function, batched=True)

# Ensure data is moved to CPU
def move_to_device(batch):
    # Only move tensor-compatible items to the device
    return {
        k: torch.tensor(v).to(device) if isinstance(v, list) and len(v) > 0 and isinstance(v[0], (int, float)) else v
        for k, v in batch.items()
    }

encoded_dataset = encoded_dataset.map(move_to_device, batched=True)

# Make sure the inputs are correctly formatted and moved to the CPU
def collate_fn(batch):
    input_ids = torch.stack([torch.tensor(item['input_ids']).to(device) for item in batch])
    attention_mask = torch.stack([torch.tensor(item['attention_mask']).to(device) for item in batch])
    labels = torch.tensor([item['labels'] for item in batch]).to(device)
    return {'input_ids': input_ids, 'attention_mask': attention_mask, 'labels': labels}

# Training arguments
training_args = TrainingArguments(
    output_dir="./results",
    eval_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
    use_cpu=True  # Ensure CPU is used
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=encoded_dataset["train"],
    eval_dataset=encoded_dataset["test"],
    data_collator=collate_fn,  # Use the custom collate function
)

# Fine-tune the model
trainer.train()

# Create a pipeline for sentiment analysis with the fine-tuned model
sentiment_analyzer = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, device=-1)  # Set device to CPU

def extract_aspects(text):
    doc = nlp(text)
    aspects = [chunk.text for chunk in doc.noun_chunks]
    return aspects

def analyze_aspects(text):
    aspects = extract_aspects(text)
    aspect_sentiments = {}
    for aspect in aspects:
        aspect_text = f"{aspect}: {text}"
        result = sentiment_analyzer(aspect_text)
        sentiment = result[0]['label']  # The sentiment in star rating
        confidence = result[0]['score']  # The confidence of the prediction
        aspect_sentiments[aspect] = {'sentiment': sentiment, 'confidence': confidence}
    return aspect_sentiments

# Sample text
text = "The battery life of this phone is amazing, but the camera quality is poor."

# Analyze aspects and their sentiments
aspect_sentiments = analyze_aspects(text)

for aspect, sentiment_info in aspect_sentiments.items():
    print(f"Aspect: {aspect}, Sentiment: {sentiment_info['sentiment']}, Confidence: {sentiment_info['confidence']:.2f}")
