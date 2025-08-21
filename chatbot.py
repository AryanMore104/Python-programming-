# Import necessary libraries
import nltk
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module='sklearn')
corpus = """
Natural Language Processing (NLP) is a subfield of artificial intelligence.
It is concerned with the interactions between computers and human language.
NLP enables computers to understand, interpret, and generate human text.
Key tasks in NLP include tokenization, parsing, and named entity recognition.
Tokenization is the process of breaking text into smaller pieces called tokens.
Libraries like NLTK and spaCy are popular for NLP tasks in Python.
NLTK, the Natural Language Toolkit, is great for learning and research.
spaCy is known for its speed and is often used in production environments.
A chatbot is a common application of NLP.
Chatbots can answer user queries, provide information, or even complete tasks.
This simple chatbot uses a technique called TF-IDF to find the best response.
"""


try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Downloading 'punkt' package...")
    nltk.download('punkt')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    print("Downloading 'wordnet' package...")
    nltk.download('wordnet')
try:
    nltk.data.find('tokenizers/punkt_tab') # <-- ADD THIS CHECK
except LookupError:
    print("Downloading 'punkt_tab' package...")
    nltk.download('punkt_tab') # <-- AND THIS DOWNLOADER
# Tokenize the corpus into a list of sentences
sentence_tokens = nltk.sent_tokenize(corpus)
lemmatizer = nltk.stem.WordNetLemmatizer()

# Function to lemmatize tokens (reduce words to their base form)
def lemmatize_tokens(tokens):
    return [lemmatizer.lemmatize(token) for token in tokens]

# Function to normalize the text (lowercase, remove punctuation)
def normalize(text):
    return lemmatize_tokens(nltk.word_tokenize(text.lower()))

# --- 3. The Response Generation Function ---
def get_response(user_query):
    # Add the user's query to the sentence list to include it in the TF-IDF calculation
    sentence_tokens.append(user_query)
    
    # Create a TF-IDF Vectorizer with our normalization function
    tfidf_vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')
    
    # Create the TF-IDF vectors
    tfidf_matrix = tfidf_vectorizer.fit_transform(sentence_tokens)
    
    # Calculate the cosine similarity between the user's query (last element) and all other sentences
    similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix)
    
    # Get the index of the most similar sentence (ignoring the similarity to itself)
    # The second-to-last score will be the highest similarity to a sentence in the original corpus
    most_similar_index = similarity_scores.argsort()[0][-2]
    
    # Get the similarity score of the best match
    best_score = similarity_scores[0][most_similar_index]
    
    # Remove the user's query from the sentence list
    sentence_tokens.pop()
    
    # If the best score is 0, it means there was no match
    if best_score == 0:
        return "I'm sorry, I don't understand that. Could you rephrase?"
    else:
        # Return the most similar sentence
        return sentence_tokens[most_similar_index]

# --- 4. The Chat Loop ---
def run_chatbot():
    print("ChatBot: Hello! I am an NLP-powered chatbot. Ask me a question about NLP, NLTK, or spaCy. Type 'bye' to exit.")
    
    # Pre-defined greetings and responses
    greetings = ("hello", "hi", "hey", "greetings")
    greeting_responses = ["Hello!", "Hi there!", "Hey! How can I help?"]

       # "How are you?"
    how_are_you_in = ("how are you", "how are you doing", "how's it going")
    how_are_you_out = ["I'm doing great, thanks for asking!", "I am a bot, so I am always ready to help!", "Feeling fantastic! What can I do for you?"]

    # "What is your name?"
    name_in = ("what is your name", "who are you")
    name_out = ["You can call me ChatBot.", "I'm ChatBot, your friendly NLP assistant."]
    
    # "Thanks"
    thanks_in = ("thanks", "thank you", "thx")
    thanks_out = ["You're welcome!", "No problem!", "Happy to help!"]
    while True:
        user_input = input("You: ").lower()
        
        if user_input in ('bye', 'quit', 'exit'):
            print("ChatBot: Goodbye! Have a great day.")
            break
        
        # Handle simple greetings
        if user_input in greetings:
            print(f"ChatBot: {random.choice(greeting_responses)}")

        elif user_input in how_are_you_in:
            print(f"ChatBot: {random.choice(how_are_you_out)}")

        # Check for "what is your name?"
        elif user_input in name_in:
            print(f"ChatBot: {random.choice(name_out)}")

        # Check for "thanks"
        elif user_input in thanks_in:
            print(f"ChatBot: {random.choice(thanks_out)}")    
        else:
            # Generate and print the response
            response = get_response(user_input)
            print(f"ChatBot: {response}")

# --- 5. Start the Chatbot ---
if __name__ == "__main__":
    run_chatbot()