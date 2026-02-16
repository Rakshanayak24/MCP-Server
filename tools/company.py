from pydantic import BaseModel, Field
from db.pool import get_pool

class CompanyQuery(BaseModel):
    identifier: str = Field(..., min_length=1)

def register_company_tools(server):
    @server.tool(name="get_company_profile",
                 description="Fetch company profile by ticker or name")
    async def get_company_profile(input: CompanyQuery):
        pool = await get_pool()
        async with pool.acquire() as con:
            row = await con.fetchrow(
                "SELECT id, name, industry, valuation FROM companies WHERE ticker ILIKE $1 OR name ILIKE $1 LIMIT 1",
                f"%{input.identifier}%"
            )
            if not row:
                return {"error": "Company not found"}
            return dict(row)
