# Recommendation_ChatBot

# MoviesBot Chatbot

MoviesBot is a responsive chatbot application built using Flask, HTML, CSS, and JavaScript. It allows users to ask questions related to movies and provides relevant answers based on a pre-defined database. The chatbot also offers suggestions based on the conversation history to enhance user interaction.

## Features

- **Question-Answering:** Users can ask questions about movies, and the chatbot provides accurate answers based on the available data.
- **Conversation History:** MoviesBot maintains conversation history and suggests relevant topics based on previous interactions.
- **Responsive Design:** The chatbot's interface is designed to work seamlessly on desktop, tablet, and mobile devices.
- **Suggestion System:** Users receive suggestions during the conversation to help them ask relevant questions.

## Technologies Used

- **Flask:** Web framework for building the backend server.
- **HTML/CSS:** Frontend technologies for structuring and styling the user interface.
- **JavaScript:** Used for dynamic interactions, fetching data from the server, and displaying suggestions.
- **OpenAI API:** Utilized for natural language processing and question-answering capabilities.
- **Pinecone API:** Used for similarity search and conversation history analysis.

## Getting Started

To run the MoviesBot chatbot locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/moviesbot-chatbot.git
   cd moviesbot-chatbot

pip install -r requirements.txt

OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key

python app.py or flask run
