# Character Backstory Verification System

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-required-blue.svg)](https://www.docker.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3+-green.svg)](https://langchain.com/)

> **Team:** Binary Brigade  
> **Event:** Kharagpur Data Science Hackathon 2026  
> **Challenge:** Verify character backstory consistency against classic literature

## 📖 Overview

This project implements an intelligent **Retrieval-Augmented Generation (RAG)** system that verifies whether character backstories are consistent with or contradict their source novels. The system uses a sophisticated multi-agent workflow powered by **LangGraph**, dual **vector stores**, and **GPT-5** reasoning to provide accurate verdicts with detailed rationales.

### Key Features

- 🎯 **Corrective RAG Architecture**: Multi-step query generation and retrieval for comprehensive context gathering
- 📚 **Dual Vector Stores**: Separate vector databases for each novel to prevent character detail mixing
- 🤖 **LLM-Powered Reasoning**: GPT-5 for query generation and final verdict synthesis
- 🐳 **Dockerized Deployment**: Fully containerized vector stores for easy setup and reproducibility
- 🔄 **Automated Pipeline**: One-command execution from start to finish
- ✅ **Structured Output**: Clean CSV format with verdicts and rationales

## 🏗️ Architecture

The system uses a **LangGraph state machine** with three main stages:

1. **Query Generation**: LLM generates 3-4 targeted search queries based on character and backstory
2. **Multi-Query Retrieval**: Queries are executed against book-specific vector stores to gather relevant passages
3. **Verdict Synthesis**: LLM analyzes retrieved context and generates structured verdict (consistent/contradict) with rationale

```
Backstory Input → Query Generation → Vector Retrieval → Verdict Synthesis → Output
                      (GPT-5)        (Dual Stores)         (GPT-5)
```

### Technology Stack

- **LangChain & LangGraph**: Orchestration and agent workflow
- **OpenAI GPT-5**: Language model for reasoning
- **OpenAI Embeddings**: text-embedding-3-small for vector representations
- **Pathway Vector Client**: Custom vector store interface
- **Docker**: Containerized vector stores (ports 8765, 8766)
- **Flask**: Vector store REST API servers
- **Pandas**: Data processing and CSV handling

## 📋 Requirements

### System Requirements
- **OS**: Windows 10/11, Linux, or MacOS
- **RAM**: Minimum 8GB (16GB recommended)
- **Disk Space**: ~10GB free
- **Python**: 3.10 or higher
- **Docker Desktop**: Installed and running

### API Keys
- **OpenAI API Key** with access to:
  - GPT-5 (or GPT-4 as fallback)
  - text-embedding-3-small

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/smt2208/Binary-Brigade_KDSH_2026.git
cd Binary-Brigade_KDSH_2026/Code
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Create a `.env` file in the `Code` directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Run the System
```bash
python run.py
```

That's it! The script will:
- ✅ Start Docker containers for both vector stores
- ✅ Wait for servers to become ready
- ✅ Process all test cases from `data/test.csv`
- ✅ Generate predictions in `data/results.csv`

## 📂 Project Structure

```
Code/
├── main.py                      # Main execution pipeline
├── run.py                       # Automated runner (Docker + pipeline)
├── docker-compose.yml           # Docker services configuration
├── requirements.txt             # Python dependencies
├── .env                         # API keys (create this)
│
├── config/
│   └── config.py                # Central configuration
│
├── src/
│   ├── graph_agent.py           # LangGraph workflow implementation
│   └── prompts.py               # System and user prompts
│
├── servers/
│   ├── server_castaways.py      # Vector store server (port 8765)
│   └── server_monte_cristo.py   # Vector store server (port 8766)
│
├── data/
│   ├── train.csv                # Training dataset
│   ├── test.csv                 # Test dataset (input)
│   ├── results.csv              # Predictions (output)
│   └── Books/
│       ├── In search of the castaways.txt
│       └── The Count of Monte Cristo.txt
│
├── Dockerfile.castaways         # Dockerfile for Castaways vector store
└── Dockerfile.monte_cristo      # Dockerfile for Monte Cristo vector store
```

## 🔧 Configuration

Key settings in [config/config.py](config/config.py):

```python
LLM_MODEL = "gpt-4o"                    # Language model
LLM_TEMPERATURE = 0.0                   # Deterministic output
RETRIEVAL_K = 5                         # Top-K documents per query
PATHWAY_PORT_CASTAWAYS = 8765           # Vector store port 1
PATHWAY_PORT_MONTE_CRISTO = 8766        # Vector store port 2
```

## 📊 Input & Output Format

### Input (`data/test.csv`)
| Story ID | Character | Book Name                      | Backstory                           |
|----------|-----------|--------------------------------|-------------------------------------|
| 1        | Mary Grant| In Search of the Castaways     | Mary is Captain Grant's daughter... |

### Output (`data/results.csv`)
| Story ID | Prediction | Rationale                                                    |
|----------|------------|--------------------------------------------------------------|
| 1        | consistent | Mary Grant is confirmed as Captain Grant's daughter in...   |

## 🐳 Docker Services

The system runs two separate vector store containers:

- **novel-rag-castaways** (port 8765): Serves "In Search of the Castaways"
- **novel-rag-monte-cristo** (port 8766): Serves "The Count of Monte Cristo"

### Manual Docker Commands
```bash
# Start services
docker-compose up --build -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🧪 Testing

Run the system on test data:
```bash
python main.py
```

For custom testing, modify [data/test.csv](data/test.csv) with your own backstories.

## 🛠️ Troubleshooting

### Docker Issues
- Ensure Docker Desktop is running
- Check ports 8765 and 8766 are not in use
- Try: `docker-compose down && docker-compose up --build`

### API Errors
- Verify your OpenAI API key in `.env`
- Check API quota and model access
- Ensure internet connectivity

### Import Errors
- Run: `pip install -r requirements.txt --upgrade`
- Check Python version: `python --version` (must be 3.10+)

For detailed setup instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md).

## 📝 License

This project was developed for the Kharagpur Data Science Hackathon 2026.

## 👥 Team Binary Brigade

*Innovative solutions through collaborative intelligence.*

---

**Questions or Issues?** Check the [SETUP_GUIDE.md](SETUP_GUIDE.md) for comprehensive installation instructions.
- `story_id`: The ID of the input backstory.
- `prediction`: `1` (Consistent) or `0` (Contradict).
- `rationale`: A brief textual explanation of the decision.
