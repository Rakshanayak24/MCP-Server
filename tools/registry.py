from tools.company import register_company_tools
from tools.finance import register_finance_tools

def register_all(server):
    register_company_tools(server)
    register_finance_tools(server)
