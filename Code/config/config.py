"""Configuration file for Novel RAG System"""

import os
from dotenv import load_dotenv

load_dotenv()

PATHWAY_HOST = "127.0.0.1"
PATHWAY_PORT_CASTAWAYS = 8765
PATHWAY_PORT_MONTE_CRISTO = 8766

BOOK_NAMES = {
    "castaways": "In Search of the Castaways",
    "monte_cristo": "The Count of Monte Cristo"
}

LLM_MODEL = "gpt-5-2025-08-07"
LLM_TEMPERATURE = 0.3
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 1536

CHUNK_SIZE = 2000
CHUNK_OVERLAP = 500
RETRIEVAL_K = 5

DATA_DIR = "./data"
BOOKS_DIR = "./data/Books"
TRAIN_DATA = "./data/train.csv"
TEST_DATA = "./data/test.csv"
RESULTS_FILE = "../Results/results.csv"

EVALUATION_SAMPLE_SIZE = 10
REQUEST_DELAY = 5
RETRY_ATTEMPTS = 3
RETRY_DELAY = 2

SERVER_HOST = "0.0.0.0"
RESERVED_SPACE = 1000
