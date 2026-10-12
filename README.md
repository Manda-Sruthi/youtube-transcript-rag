# YouTube Transcript Q&A using RAG

A Retrieval-Augmented Generation application that answers questions about YouTube videos using their available transcripts.

## Features

- YouTube transcript extraction
- Recursive text splitting with overlap
- Gemini text embeddings
- FAISS similarity search
- Gemini-powered question answering
- Streamlit web interface
- Transcript evidence and timestamp links
- Basic automated tests

## Architecture

YouTube URL → Transcript Extraction → Chunking → Gemini Embeddings → FAISS → Retrieval → Gemini Answer → Streamlit UI

## Technology Stack

Python, LangChain, Google Gemini, FAISS, Streamlit, YouTube Transcript API, pytest.

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

   `pip install -r requirements.txt`

3. Copy `.env.example` to `.env`.
4. Add your Google API key to `.env`.
5. Run the tests:

   `pytest -q`

6. Start the app:

   `streamlit run app.py`

## How it works

The application extracts the available transcript, splits it into chunks, embeds those chunks, and stores them in a FAISS index. When a user asks a question, the app retrieves relevant chunks and passes them to Gemini as evidence for answering.

## Limitations

- Some videos do not have accessible transcripts.
- The starter version requests English captions.
- API quotas and rate limits may affect usage.
- The FAISS index is held in Streamlit session state and is not durable storage.
- Retrieved evidence and model answers can still be incomplete or incorrect.

## Future Improvements

- Multiple-video collections
- Persistent vector indexes
- Chat history
- More language options
- Retrieval evaluation and relevance thresholds
- Docker and cloud deployment

## Security

Never commit your `.env` file or API keys. Keep secrets in environment variables or your deployment platform's secret manager.

## Learning Objectives

Understand transcript processing, embeddings, vector similarity search, RAG, prompt grounding, Python modularity, and Streamlit application development.