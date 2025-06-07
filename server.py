from fastmcp import MCPServer
import httpx

## Create MCP server
server = MCPServer()

@server.method()
async def get_protein_info(pdb_id: str) -> dict:
    """Fetch basic metadata for a protein using its PDB ID."""
    async with httpx.AsyncClient() as client:
        url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
        response = await client.get(url)

    if response.status_code != 200:
        return {"error": f"PDB ID '{pdb_id}' not found."}

    data = response.json()
    return {
        "title": data.get("struct", {}).get("title", "Unknown"),
        "method": data.get("exptl", [{}])[0].get("method", "Unknown"),
        "resolution": data.get("rcsb_entry_info", {}).get("resolution_combined", ["N/A"])[0],
        "release_date": data.get("rcsb_accession_info", {}).get("initial_release_date", "Unknown")
    }

## Run the MCP server
if __name__ == "__main__":
    server.run()
