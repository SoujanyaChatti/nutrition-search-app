# nutrition_web_app/nutrition_search.py
import pandas as pd
import re
from collections import namedtuple

# Define a structure to hold the information of each item including NDB_No
Item = namedtuple('Item', ['description', 'similarity_score', 'length', 'NDB_No'])

# Preprocess input to handle compound words and tokenization
def preprocess_input(description):
    tokens = re.findall(r'\w+', description.lower().strip())
    return set(tokens)

def contains_input_as_substrings(input_tokens, dataset_description):
    dataset_description = dataset_description.lower()
    return all(token in dataset_description for token in input_tokens)

# Calculate Levenshtein distance-based similarity
def levenshtein_similarity(s1, s2):
    from difflib import SequenceMatcher
    return SequenceMatcher(None, s1, s2).ratio()

# Token match similarity to prioritize exact token presence
def token_match_similarity(input_tokens, dataset_tokens):
    if input_tokens.issubset(dataset_tokens):
        return 1.0  # Exact match of input tokens in dataset item
    return 0.0

# Combined similarity scoring mechanism considering both token presence and Levenshtein distance
def combined_similarity(input_description, dataset_description):
    input_tokens = preprocess_input(input_description)
    dataset_tokens = preprocess_input(dataset_description)

    # Check for exact token match presence
    token_match_score = token_match_similarity(input_tokens, dataset_tokens)
    if token_match_score == 1.0:
        return token_match_score

    # Continue with Levenshtein similarity scoring
    input_string = ' '.join(input_tokens)
    dataset_string = ' '.join(dataset_tokens)
    levenshtein_score = levenshtein_similarity(input_string, dataset_string)

    combined_score = 0.6 * token_match_score + 0.4 * levenshtein_score
    return combined_score

# Function to prioritize matches in dataset
def prioritize_matches(input_description, df, top_n=10):
    input_tokens = preprocess_input(input_description)
    prioritized_matches = []
    other_matches = []

    # Step 1: Prioritize matches with exact token presence
    for index, row in df.iterrows():
        dataset_description = row['Shrt_Desc'].lower()
        if contains_input_as_substrings(input_tokens, dataset_description):
            item_length = len(dataset_description)
            item = Item(description=dataset_description, similarity_score=1.0, length=item_length, NDB_No=row['NDB_No'])
            prioritized_matches.append(item)

    # Step 2: Handle other matches with combined similarity scoring mechanism
    for index, row in df.iterrows():
        dataset_description = row['Shrt_Desc'].lower()
        similarity_score = combined_similarity(input_description, dataset_description)

        if similarity_score > 0:
            item_length = len(dataset_description)
            item = Item(description=dataset_description, similarity_score=similarity_score, length=item_length, NDB_No=row['NDB_No'])
            other_matches.append(item)

    # Sort prioritized matches by similarity score descending, and then by length ascending
    prioritized_matches.sort(key=lambda x: (-x.similarity_score, x.length))
    # Sort other matches by similarity score descending, and then by length ascending
    other_matches.sort(key=lambda x: (-x.similarity_score, x.length))

    # Collect the top matches
    top_matches = prioritized_matches[:top_n] + other_matches[:max(top_n - len(prioritized_matches), 0)]

    return [(match.description, match.NDB_No) for match in top_matches]

# Load the dataset from a CSV file
file_path = '/users/soujanyachatti/Desktop/ABBREV.csv'  # Update with the correct path to your dataset
df = pd.read_csv(file_path)
