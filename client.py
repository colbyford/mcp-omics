import asyncio
from fastmcp import Client

client = Client("server.py")

async def call_pdb(pdb_id: str):
    async with client:
        result = await client.call_tool("get_protein_info", {"pdb_id": pdb_id})
        print(result)

asyncio.run(call_pdb("5JXE"))
