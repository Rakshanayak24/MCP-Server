from pydantic import BaseModel
from db.pool import get_pool

class TickerInput(BaseModel):
    ticker: str

def register_finance_tools(server):
    @server.tool(name="get_financial_report",
                 description="Get financial reports")
    async def get_financial_report(input: TickerInput):
        pool = await get_pool()
        async with pool.acquire() as con:
            rows = await con.fetch(
                "SELECT fr.* FROM financial_reports fr "
                "JOIN companies c ON c.id = fr.company_id "
                "WHERE c.ticker=$1 ORDER BY fiscal_year DESC",
                input.ticker
            )
            return [dict(r) for r in rows]
