import spacy
from transformers import pipeline

# Load Spacy model for aspect extraction
nlp = spacy.load("en_core_web_sm")

# Specify the model explicitly
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
sentiment_analyzer = pipeline("sentiment-analysis", model=model_name)

def extract_aspects(text):
    doc = nlp(text)
    aspects = [chunk.text for chunk in doc.noun_chunks]
    return aspects

def extract_adjectives(doc, aspect):
    adjectives = []
    for token in doc:
        if token.dep_ in ['amod', 'acomp'] and (token.head.text in aspect or aspect in [child.text for child in token.head.children]):
            adjectives.append(token.text)
    return list(set(adjectives)) if adjectives else ["NIL"]

def analyze_aspects(text):
    doc = nlp(text)
    aspects = extract_aspects(text)
    aspect_sentiments = {}
    for aspect in aspects:
        aspect_sentences = [sent for sent in doc.sents if aspect in sent.text]
        for sent in aspect_sentences:
            clauses = [clause.text for clause in sent.as_doc().sents if aspect in clause.text]
            for clause in clauses:
                result = sentiment_analyzer(clause)[0]
                sentiment = result['label']  # The sentiment label
                confidence = result['score']  # The confidence of the prediction
                clause_doc = nlp(clause)
                adjectives = extract_adjectives(clause_doc, aspect)
                if aspect not in aspect_sentiments:
                    aspect_sentiments[aspect] = {'sentiment': sentiment, 'confidence': confidence, 'adjectives': adjectives}
                else:
                    if confidence > aspect_sentiments[aspect]['confidence']:
                        aspect_sentiments[aspect]['sentiment'] = sentiment
                        aspect_sentiments[aspect]['confidence'] = confidence
                        aspect_sentiments[aspect]['adjectives'] = adjectives
    return aspect_sentiments

# Sample text
text = "Wah, I want this shirt. The battery life of this phone is amazing, but the camera quality is poor. The display is bright and clear."

# Analyze aspects and their sentiments
aspect_sentiments = analyze_aspects(text)

# Print results
for aspect, sentiment_info in aspect_sentiments.items():
    print(f"Aspect: {aspect}, Sentiment: {sentiment_info['sentiment']}, Confidence: {sentiment_info['confidence']:.2f}, Adjectives: {', '.join(sentiment_info['adjectives'])}")

print("Extraction complete.")
