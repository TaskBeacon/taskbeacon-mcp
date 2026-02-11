# Codex MCP failure notes (taskbeacon)

## Symptom
You see something like:

- MCP client for taskbeacon failed to start: ... handshaking ... connection closed: initialize response

That message means: the MCP client spawned the server process, but the server exited (or the stdio streams closed) before it replied to the MCP initialize request.

## What I verified on this machine
- Running D:\Python310\python.exe -u E:\xhmhc\TaskBeacon\taskbeacon-mcp\taskbeacon_mcp\main.py --stdio from a normal shell exits quickly with no output.
  - This is expected when the process has no MCP client connected: MCP stdio servers read JSON-RPC lines from stdin. If stdin is closed/empty, the server can exit.
- When launched via an MCP stdio client (keeps stdin open and sends initialize), the server works.
  - initialize.protocolVersion = 2025-06-18
  - tools: Build_task, download_task, localize, list_voices, list_tasks
  - prompts: 	ransform_prompt, localize_prompt, choose_template_prompt, choose_repo_prompt

So: this is typically a client launch/config issue or an environment/import issue, not a protocol mismatch in 	askbeacon_mcp.

## Most common root causes
1. **Missing Python dependencies in the exact interpreter you configured**
   - If D:\Python310\python.exe doesn’t have the deps, the process can crash on import and the client reports a handshake failure.

2. **Client is not actually running stdio transport correctly**
   - If the client closes stdin immediately (or never sends JSON-RPC), the server can exit and you’ll see the same handshake error.

3. **Wrong config / wrong entrypoint path**
   - Wrong file path, wrong python, or a config format mismatch can all lead to a process that exits instantly.

## The smoke test (recommended)
This reproduces the client/server handshake locally and prints the tool list.

Run in PowerShell:

`powershell
@'
import anyio
from mcp import StdioServerParameters, stdio_client, ClientSession

SERVER = StdioServerParameters(
    command=r"D:\\Python310\\python.exe",
    args=[
        "-u",
        r"E:\\xhmhc\\TaskBeacon\\taskbeacon-mcp\\taskbeacon_mcp\\main.py",
        # optional; this server ignores --stdio, but keeping it doesn't hurt
        "--stdio",
    ],
)

async def main():
    async with stdio_client(SERVER) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            tools = await s.list_tools()
            print([t.name for t in tools.tools])

anyio.run(main)
'@ | D:\Python310\python.exe -
`

Expected output includes:

- ['build_task', 'download_task', 'localize', 'list_voices', 'list_tasks']

If this fails, the printed traceback is your real root cause.

## Fix: install deps into that interpreter
From repo root:

`powershell
D:\Python310\python.exe -m pip install -e E:\xhmhc\TaskBeacon\taskbeacon-mcp
`

## Recommended Codex config
In C:\Users\Zhipeng\.codex\config.toml, prefer the module entrypoint instead of a direct .py path:

`	oml
[mcp_servers.taskbeacon]
command = "D:\\Python310\\python.exe"
args = ["-u", "-m", "taskbeacon_mcp.server"]
`

Notes:
- --stdio is not required for this server (it always runs stdio).
- If you keep the .py entrypoint, it should still work.

## Where to look for details (Codex)
Codex log:
- C:\Users\Zhipeng\.codex\log\codex-tui.log

Search for:
- MCP client for + Failed to start
- MCP server stderr

Those lines usually contain the actual exception (import error, path error, etc.).
