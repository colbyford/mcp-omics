import asyncio
from fastmcp import Client

client = Client("server.py")

## Test PDB Method
async def call_pdb(pdb_id: str):
    async with client:
        result = await client.call_tool("get_pdb_info", {"pdb_id": pdb_id})
        print(result)

asyncio.run(call_pdb("5JXE"))

## Test ChEMBL Method
async def call_chembl(chembl_id: str):
    async with client:
        result = await client.call_tool("get_chembl_info", {"chembl_id": chembl_id})
        print(result)

asyncio.run(call_chembl("CHEMBL25"))
