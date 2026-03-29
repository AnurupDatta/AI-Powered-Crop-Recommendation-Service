AI-Powered Crop Recommendation Service
![WhatsApp Image 2026-03-25 at 04 05 08](https://github.com/user-attachments/assets/70d26148-6ad1-4b69-b927-724c1e03ed34)
This Project is a full-stack AI service that recommends optimal crops to farmers based on environmental conditions. It features a scalable vector search backend, a hybrid search capability, and an LLM-powered engine to provide clear explanations for its recommendations.

Table of Contents
Project Overview
Features
System Architecture
Technologies Used
Setup and Installation
Usage
Running the API Server
API Endpoint
Interactive Notebook
Future Improvements
Project Overview
The goal of this project is to provide an intelligent, data-driven tool for farmers. By inputting environmental data (temperature, humidity, moisture) and an optional keyword, users receive a list of the most suitable crops. What makes this service powerful is its ability to not only recommend but also explain why each crop is a good choice, leveraging a Large Language Model (LLM).

The system is built as a RESTful API using FastAPI, making it easy to integrate with any front-end application (web or mobile).

Features
RESTful API: A robust backend built with FastAPI to serve crop recommendations.
Hybrid Search: Combines keyword-based search with semantic (vector) search for more accurate and relevant results.
Scalable Vector Database: Uses Astra DB (Cassandra) to store and efficiently query millions of crop data vectors.
Explainable AI (XAI): Integrates with the Groq API to leverage the llama-3.3-70b-versatile model, providing users with human-readable explanations for each recommendation.
Modular and Production-Ready: The logic is decoupled into a recommender module, and the API is ready for deployment.
System Architecture
The project follows a simple, yet powerful, architecture:

API Layer (FastAPI): The app.py file defines the API endpoints. It receives user requests containing environmental data.
Recommender Service (recommender.py): This module contains the core logic.
It takes the input data and constructs a query.
It performs a hybrid similarity search against the Astra DB vector store to retrieve the most relevant crops.
The search results are then passed to the Groq LLM.
LLM for Explanation: The LLM generates a detailed explanation based on the input conditions and the recommended crops.
Response: The API returns a JSON object containing the list of recommended crops and the AI-generated explanation.
Technologies Used
Backend: FastAPI
AI / ML:
LangChain
HuggingFace Transformers (sentence-transformers/all-MiniLM-L6-v2 for embeddings)
Semantic & Hybrid Search
Database: Astra DB (serverless Cassandra)
LLM Provider: Groq API (llama-3.3-70b-versatile)
Libraries: Pandas, NumPy, python-dotenv, cassio
Language: Python
Setup and Installation
Follow these steps to set up and run the project locally.
![WhatsApp Image 2026-03-25 at 04 04 17 (1)](https://github.com/user-attachments/assets/b57c38de-31b9-4b22-9582-084f0eb4d148)

![WhatsApp Image 2026-03-25 at 04 04 17](https://github.com/user-attachments/assets/519e9142-e8c3-49c0-8682-2be280301b60)


1. Clone the Repository
2. Create a Virtual Environment
It's recommended to use a virtual environment to manage dependencies.

3. Install Dependencies
Create a requirements.txt file with the following content:

Then, install the packages:

4. Set Up Environment Variables
You will need API keys for Astra DB and Groq. Create a file named .env in the root directory of the project and add your credentials:

5. Populate the Vector Database
The first time you run the application, it will populate the Astra DB vector store with data from Crop_recommendation.csv. This is handled by the recommender.py script. After the first successful run, you can comment out the line astra_vector_store.add_texts(crop_strings) in recommender.py to prevent re-indexing.

Usage
Running the API Server
To start the FastAPI server, run the following command in your terminal:

The server will be available at http://127.0.0.1:8000. You can access the interactive API documentation at http://127.0.0.1:8000/docs.

API Endpoint
POST /recommend_crops
This endpoint accepts environmental data and an optional keyword to return crop recommendations.

Request Body:

keyword (optional): A specific crop or term to refine the search.
Example curl Request:

Success Response (200 OK):

<img width="1081" height="417" alt="image" src="https://github.com/user-attachments/assets/796e5905-7fea-4cd2-865e-b3167bc19c7b" />

Interactive Notebook
For experimentation and testing, you can use the crop_recommend.ipynb Jupyter notebook. It provides a step-by-step guide to testing the recommendation logic interactively.
