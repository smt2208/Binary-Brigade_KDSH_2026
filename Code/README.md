# Character Backstory Verification System

**Team:** Binary Brigade  
**Event:** Kharagpur Data Science Hackathon 2026

## Overview
This system verifies the consistency of character backstories against literary texts using a multi-step Retrieval-Augmented Generation (RAG) approach. It leverages LangGraph for orchestration, Pathway for vector storage, and GPT-5 for reasoning.

## Requirements

1. **System**:
   - OS: Windows, Linux, or MacOS
   - Python: 3.10 or higher
   - Docker: Desktop installed and running

2. **API Keys**:
   - OpenAI API Key (Access to GPT-5 required)

## Setup & Installation

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_sk_key_here
   ```

## How to Run

A single script handles the entire workflow (starting Docker containers, waiting for readiness, and running the pipeline).

**Command**:
```bash
python run.py
```

**What happens**:
1. Checks if `docker-compose` is available.
2. Starts the vector store servers (Ports 8765, 8766).
3. Polls the servers until they are ready to accept requests.
4. Executes the verification pipeline on `data/test.csv`.
5. Outputs predictions to `data/results.csv`.

## Output Format

The results are saved in `data/results.csv`:
- `story_id`: The ID of the input backstory.
- `prediction`: `1` (Consistent) or `0` (Contradict).
- `rationale`: A brief textual explanation of the decision.
