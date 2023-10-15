import os
import sys
from flask import Flask, request, jsonify
# from dotenv import load_dotenv, find_dotenv
from dotenv import load_dotenv, find_dotenv
import openai
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import subprocess
from flask_cors import CORS
import json
import pinecone
from langchain.vectorstores import Pinecone

from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain


# app = Flask(__name__)
# CORS(app)

# # load_dotenv()

# load_dotenv(find_dotenv())
# # openai.api_key = os.environ["OPENAI_API_KEY"]

# OPENAI_API_KEY = "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"

# # api_requestor = openai.APIRequestor(key=OPENAI_API_KEY)
# print(OPENAI_API_KEY, "knkknkk")


# def read_json_file(filename):
#   with open(filename, "r") as f:
#     data = json.load(f)

#   return data

# # Example usage:

# data = read_json_file("movies.json")
# # print(data)

# def objects_to_paragraphs(objects):
#   paragraphs = []
#   for object in objects:
#     paragraph = ""
#     for key, value in object.items():
#       paragraph += f"{key}: {value}\n"

#     paragraphs.append(paragraph)

#   return paragraphs

# res = objects_to_paragraphs(data)
# # print(res)


# embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)



# PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
# PINECONE_API_ENV = os.getenv('PINECONE_API_ENV')
# print(PINECONE_API_KEY)
# print(PINECONE_API_ENV)

# pinecone.init(
#     api_key=PINECONE_API_KEY,  
#     environment=PINECONE_API_ENV 
# )

# index = "chatbot"

# docsearch = Pinecone.from_texts(res, embeddings, index_name=index)
# # print(docsearch)

# # query = "when The Godfather released?"
# # llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
# # chain = load_qa_chain(llm, chain_type="stuff")
# # docs = docsearch.similarity_search(query)
# # answer = chain.run(input_documents=docs, question=query)

# # print(answer)

# @app.route('/chat', methods=['POST'])
# def get_answer():
#     data = request.get_json()  # Extract JSON data from the request body
#     query = data.get('query', '')  # Assuming the query is provided in the 'query' field of the JSON request
    
#     llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
#     chain = load_qa_chain(llm, chain_type="stuff")
#     docs = docsearch.similarity_search(query)
#     answer = chain.run(input_documents=docs, question=query)
    
#     response = {
#         'query': query,
#         'answer': answer  # Assuming 'answer' is a string returned by the OpenAI API
#     }
    
#     return jsonify(response)



# if __name__ == "__main__":
#     app.run(debug=True)


# import os
# from flask import Flask, request, jsonify
# from dotenv import load_dotenv, find_dotenv
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.vectorstores import Pinecone
# from langchain.llms import OpenAI
# from langchain.chains.question_answering import load_qa_chain
from collections import Counter
import re

app = Flask(__name__)
CORS(app)

load_dotenv(find_dotenv())
  # Replace with your OpenAI API key
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_API_ENV = os.getenv('PINECONE_API_ENV')

# Initialize Pinecone vector store
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_API_ENV)
index_name = "chatbot"
docsearch = Pinecone.from_texts([], embeddings, index_name=index_name)

# Initialize conversation history list
conversation_history = []

@app.route('/chat', methods=['POST'])
def get_answer():
    data = request.get_json()
    query = data.get('query', '')

    # Store user query in conversation history
    conversation_history.append({'role': 'user', 'message': query})

    # Get answer from the database
    llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
    chain = load_qa_chain(llm, chain_type="stuff")
    docs = docsearch.similarity_search(query)
    answer = chain.run(input_documents=docs, question=query)

    # Generate suggestions based on conversation history
    suggestions = generate_suggestions(conversation_history)

    response = {
        'query': query,
        'answer': answer,
        'suggestions': suggestions
    }

    return jsonify(response)

# Function to generate suggestions based on conversation history
def generate_suggestions(conversation_history):
    # Extract user queries from conversation history
    user_queries = [entry['message'] for entry in conversation_history if entry['role'] == 'user']

    # Tokenize and count words in user queries
    words = re.findall(r'\b\w+\b', ' '.join(user_queries).lower())
    word_counts = Counter(words)

    # Generate suggestions based on frequently occurring words
    suggestions = []
    for word, count in word_counts.most_common():
        # Generate suggestions using frequently occurring words
        suggestion = f"Tell me more about {word.capitalize()}?"
        suggestions.append(suggestion)

    # Deduplicate suggestions and limit the number of suggestions
    unique_suggestions = list(set(suggestions))[:5]  # Limit to 5 unique suggestions

    return unique_suggestions

if __name__ == "__main__":
    app.run(debug=True)
