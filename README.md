
# Enterprise MCP Financial Server

## Features
- 8 fully validated MCP tools
- stdio + SSE transport
- Connection pooling
- Structured error responses
- Rate limiting (SSE)
- Input validation (Pydantic)
- Parameterized queries
- Production-ready architecture

## Run
```bash
pip install -r requirements.txt
python main.py
```
- open in browser: http://127.0.0.1:8001/docs
  
Fill .env File with Your API 
```BASH
SUPABASE_DB_URL=postgresql://postgres:XXXXXXX
SUPABASE_SERVICE_ROLE_KEY=sb_secret_XXXXXXX
SUPABASE_API_KEY=sb_publishable_XXXXXXXX
JWT_SECRET=6vXXXXXXXXXXXXXXXX
TRANSPORT=stdio
RATE_LIMIT_PER_MIN=60
```
