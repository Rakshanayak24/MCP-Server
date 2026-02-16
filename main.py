import os
import asyncpg
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Enterprise Financial MCP Server", version="0.1.0")

# -------------------------
# Database pool
# -------------------------
DB_PASSWORD = "YOUR PASSWORD"
DB_PASSWORD_ENCODED = DB_PASSWORD.replace("&", "%26")
SUPABASE_DB_URL = f"postgresql://postgres:{DB_PASSWORD_ENCODED}@XYZ"

_pool = None
async def get_pool():
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(SUPABASE_DB_URL)
    return _pool

# -------------------------
# CORS
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# -------------------------
# Health
# -------------------------
@app.get("/health")
async def health():
    return {"status": "ok"}

# -------------------------
# Endpoints
# -------------------------
@app.get("/tools/get_company_profile")
async def get_company_profile(identifier: str):
    pool = await get_pool()
    async with pool.acquire() as con:
        row = None
        # Try numeric ID first
        if identifier.isdigit():
            row = await con.fetchrow(
                "SELECT id AS company_id, name, ticker, industry, valuation FROM companies WHERE id=$1",
                int(identifier)
            )
        # Fallback to ticker or name
        if not row:
            row = await con.fetchrow(
                "SELECT id AS company_id, name, ticker, industry, valuation FROM companies "
                "WHERE ticker ILIKE $1 OR name ILIKE $1 LIMIT 1",
                f"%{identifier}%"
            )
        if not row:
            return {"error": "Company not found"}
        return dict(row)

@app.get("/tools/get_financial_report")
async def get_financial_report(ticker: str):
    pool = await get_pool()
    async with pool.acquire() as con:
        rows = await con.fetch(
            "SELECT fr.* FROM financial_reports fr "
            "JOIN companies c ON c.id = fr.company_id "
            "WHERE c.ticker=$1 ORDER BY fiscal_year DESC",
            ticker
        )
        return [dict(r) for r in rows]

# -------------------------
# Run server
# -------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
