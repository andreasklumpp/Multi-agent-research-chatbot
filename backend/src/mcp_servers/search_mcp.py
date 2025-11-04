import os
from agents.mcp import MCPServerStdio, MCPServerStdioParams

def get_search_mcp_server() -> MCPServerStdio:
    return MCPServerStdio(
        params=MCPServerStdioParams(
            command="uvx",
            args=["serper-mcp-server"],
            env={
                "SERPER_API_KEY": os.getenv("SERPER_API_KEY"),
            },
        )
    )