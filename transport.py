import os
from fastapi import FastAPI

def run_transport(app: FastAPI):
    transport_mode = os.getenv("TRANSPORT", "stdio").lower()

    if transport_mode == "stdio":
        print("🚀 MCP Server running in STDIO mode")
        return app
    elif transport_mode == "sse":
        print("⚠ SSE transport requested but currently disabled. Falling back to STDIO.")
        return app
    else:
        print(f"⚠ Unknown transport '{transport_mode}', defaulting to STDIO.")
        return app
