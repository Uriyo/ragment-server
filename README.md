# Ragment - Backend API

A powerful Python backend service for the Notebook LLM Clone application, featuring document processing, AI-powered retrieval, and real-time chat capabilities.

<img width="843" height="587" alt="Screenshot 2026-01-02 at 10 05 43 PM" src="https://github.com/user-attachments/assets/5a536c48-5ba3-477c-9cc7-7be6523cbff6" />



## Features

- 📄 **Advanced Document Processing** - Support for PDFs, images, and various document formats
- 🔍 **Hybrid Search** - Combines vector similarity and keyword search for optimal retrieval
- 🤖 **AI-Powered RAG Pipeline** - Retrieval-Augmented Generation for accurate responses
- ⚡ **Async Processing** - Background task processing with Celery
- 🗄️ **Vector Database** - Efficient embedding storage and retrieval with Supabase
- 🔄 **Redis Caching** - Fast data access and task queue management
- 🎯 **Multi-Agent System** - Specialized agents for different tasks

## Tech Stack

- **Framework**: FastAPI (Python)
- **Task Queue**: Celery
- **Cache/Broker**: Redis
- **Database**: Supabase (PostgreSQL + pgvector)
- **Document Processing**: Poppler, Tesseract OCR, libmagic
- **Dependency Management**: Poetry
- **Testing**: pytest

## Project Structure

```
backend/
├── redis/                    # Redis data directory
├── src/
│   ├── __pycache__/         # Python cache files
│   ├── agents/              # AI agent implementations
│   ├── config/              # Configuration management
│   ├── models/              # Data models and schemas
│   ├── rag/                 # RAG pipeline implementation
│   ├── routes/              # API route handlers
│   ├── services/            # Business logic services
│   ├── utils/               # Utility functions
│   └── server.py            # Main FastAPI application
├── supabase/                # Supabase migrations and functions
├── tests/                   # Test suite
├── .env                     # Environment variables (create from .env.sample)
├── .env.sample             # Environment variables template
├── .gitignore              # Git ignore rules
├── poetry.lock             # Poetry lock file
├── pyproject.toml          # Poetry configuration
├── README.md               # This file
├── start_redis.sh          # Redis startup script
├── start_server.sh         # API server startup script
├── start_worker.sh         # Celery worker startup script
└── stopAll.sh              # Stop all services script
```

## Prerequisites

- Python 3.9+
- Poetry (Python dependency manager)
- Redis
- Supabase account and local setup
- System dependencies: Poppler, Tesseract OCR, libmagic

## Setup

### 1. Install System Dependencies

These are required for document processing (PDFs, images, etc.)

**macOS:**

```bash
brew install poppler tesseract libmagic
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt-get update
sudo apt-get install poppler-utils tesseract-ocr libmagic1
```

**Windows:**

- Download Poppler from [https://github.com/oschwartz10612/poppler-windows/releases](https://github.com/oschwartz10612/poppler-windows/releases)
- Download Tesseract from [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)
- Add both to your system PATH

### 2. Install Poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 3. Install Python Dependencies

```bash
poetry install
```

### 4. Set Up Supabase

Start Supabase locally:

```bash
npx supabase start
```

Get your credentials:

```bash
npx supabase status
```

### 5. Configure Environment Variables

Create a `.env` file:

```bash
cp .env.sample .env
```

Update the values in `.env` file:

```env
# Supabase Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_role_key  # Previously called "Secret Key"

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# AI Model Configuration
OPENAI_API_KEY=your_openai_api_key
# Add other LLM provider keys as needed

# Application Settings
ENVIRONMENT=development
DEBUG=true
```

> 💡 **Tip:** Get your Supabase credentials by running `npx supabase status` after starting Supabase locally.
>
> ⚠️ **Note:** Supabase has updated their naming. The old variable `service_role key` is now simply called `Secret Key`.  
> 📸 [Reference screenshot](https://ik.imagekit.io/5wegcvcxp/HarishNeel/supabase-credentials.png)

## Running the Application

You need to run **3 services** in separate terminal windows:

### Terminal 1: Start Redis 🟥

```bash
sh start_redis.sh
```

This starts the Redis server for caching and task queue management.

### Terminal 2: Start API Server 🟦

```bash
sh start_server.sh
```

The API server will run on `http://localhost:8000`

**API Documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Terminal 3: Start Celery Worker 🟩

```bash
sh start_worker.sh
```

This processes background tasks including:
- Document ingestion
- Embedding generation
- Vector indexing
- Long-running operations

### Stop All Services

To stop everything at once:

```bash
sh stopAll.sh
```

This stops: Celery Worker, Redis Server, and API Server

## Development Tasks

### Complete the Basic Retrieval Pipeline

Every step is well documented inside the code. Follow the inline comments and TODOs.

### Database Schema Updates

1. **Update the initial schema:**
   - Insert your changes in the schema file before `(embedding vector_ip_ops);`
   - Insert additional changes after `(embedding vector_cosine_ops);`

2. **Create migration files:**
   - Create a new migration file for the Postgres function `vector_search_document_chunks`
   - Create a new migration file for the Postgres function `keyword_search_document_chunks`

### Complete the Advanced Retrieval Pipeline

Implement advanced retrieval techniques as outlined in the codebase documentation.

## API Endpoints

### Health Check
```
GET /health
```

### Document Management
```
POST   /api/documents/upload
GET    /api/documents
GET    /api/documents/{document_id}
DELETE /api/documents/{document_id}
```

### Chat & Query
```
POST   /api/chat
POST   /api/query
GET    /api/chat/history/{session_id}
```

### Projects
```
POST   /api/projects
GET    /api/projects
GET    /api/projects/{project_id}
PATCH  /api/projects/{project_id}
DELETE /api/projects/{project_id}
```

## Architecture

### RAG Pipeline

The Retrieval-Augmented Generation pipeline consists of:

1. **Document Ingestion** - Process and chunk documents
2. **Embedding Generation** - Create vector embeddings
3. **Vector Storage** - Store in Supabase with pgvector
4. **Hybrid Retrieval** - Combine vector and keyword search
5. **Context Ranking** - Rerank results for relevance
6. **Response Generation** - Generate answers using LLM

### Agent System

Specialized agents handle different tasks:
- **Query Agent** - Processes user queries
- **Document Agent** - Manages document operations
- **Synthesis Agent** - Combines information from multiple sources

## Testing

Run tests with pytest:

```bash
poetry run pytest
```

Run tests with coverage:

```bash
poetry run pytest --cov=src --cov-report=html
```

## Deployment

### Docker (Recommended)

```bash
docker build -t notebook-llm-backend .
docker run -p 8000:8000 notebook-llm-backend
```

### Production Considerations

- Use a production-ready ASGI server (Gunicorn + Uvicorn)
- Set up proper logging and monitoring
- Configure CORS settings appropriately
- Use environment-specific configuration
- Set up SSL/TLS certificates
- Configure rate limiting
- Implement proper authentication/authorization

## Troubleshooting

### Redis Connection Issues
```bash
# Check if Redis is running
redis-cli ping

# Should return: PONG
```

### Celery Worker Not Processing Tasks
```bash
# Check Celery logs
celery -A src.celery inspect active

# Restart the worker
sh stopAll.sh
sh start_worker.sh
```

### Document Processing Errors

Ensure system dependencies are installed:
```bash
# Test Poppler
pdftoppm -v

# Test Tesseract
tesseract --version
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for functions and classes
- Add unit tests for new features

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with FastAPI and Celery
- Powered by Supabase and pgvector
- Document processing with Poppler and Tesseract
- AI capabilities through OpenAI and other LLM providers

## Support

For support, please open an issue in the GitHub repository or contact the development team.

---

Built with 🐍 using Python and FastAPI
