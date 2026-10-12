# YouTube Transcript Q&A — RAG Project

A question-answering application that lets users ask questions about a YouTube video's transcript. It uses Retrieval-Augmented Generation (RAG) to retrieve relevant transcript sections and generate answers grounded in the available content.

## Features

- Extracts available transcripts from YouTube videos.
- Splits transcripts into smaller text chunks.
- Creates embeddings and stores them in a FAISS vector index.
- Retrieves relevant transcript sections for user questions.
- Uses Google's Gemini model to generate answers.
- Provides a Streamlit web interface.
- Includes automated tests for core pipeline functions.

## Tech Stack

- Python
- Streamlit
- LangChain
- Google Gemini API
- FAISS
- YouTube Transcript API
- Pytest

## How It Works

1. Enter a YouTube video URL.
2. The app retrieves the available transcript.
3. The transcript is split into chunks and converted into embeddings.
4. FAISS retrieves relevant chunks for a question.
5. Gemini generates an answer using the retrieved context.
6. The app displays the answer and relevant sources when evidence is available.

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Manda-Sruthi/youtube-transcript-rag.git
cd youtube-transcript-rag
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure your API key

Create a local `.env` file based on `.env.example`.

Add your own Google Gemini API key and the model settings required by your code. Never upload your real `.env` file or API key to GitHub.

### 5. Run the application

```powershell
streamlit run app.py
```

## Run Tests

```powershell
python -m pytest
```

## Notes

- A valid Google Gemini API key is required.
- API availability and quotas depend on your account and selected model.
- Not every YouTube video has an accessible transcript.
- Answer quality depends on the available transcript and retrieved context.

## License

No license has been added yet.
