import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import pandas as pd

# Load the Universal Sentence Encoder model
module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
model = hub.load(module_url)

# Function to calculate the similarity scores
def calculate_similarity(sentence1, sentence2):
    if pd.isnull(sentence1) or pd.isnull(sentence2):
        return 0.0
    embeddings = model([sentence1, sentence2])
    similarity = tf.tensordot(embeddings, tf.transpose(embeddings), 1).numpy()
    return similarity[0][1]  # Return the similarity score between the two sentences

def calculate_similarity_scores(df):
    # Prepare data for comparison
    data = []
    for country, law in zip(df['Country'], df['Legislation']):
        sentences = law.split('.')  # Split law into sentences (assuming '.' separates sentences)
        for sentence in sentences:
            data.append((country, sentence))

    # Calculate the similarity scores
    similarity_scores = []
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            country1, sentence1 = data[i]
            country2, sentence2 = data[j]
            if country1 != country2:  # Compare only if the countries are different
                similarity_score = calculate_similarity(sentence1, sentence2)
                similarity_scores.append([country1, sentence1, country2, sentence2, similarity_score])

    return similarity_scores

# Load all laws from the CSV file into a DataFrame
all_laws_df = pd.read_csv("hate_laws_processed.csv")

# Calculate similarity scores for the provided DataFrame
similarity_scores = calculate_similarity_scores(all_laws_df)

# Create a DataFrame from the similarity scores
similarity_df = pd.DataFrame(similarity_scores, columns=['Country1', 'Sentence1', 'Country2', 'Sentence2', 'SimilarityScore'])

# Save the resulting DataFrame
similarity_df.to_csv("similarity_scores.csv", index=False)
