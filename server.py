from fastmcp import MCPServer
import httpx

## Create MCP server
server = MCPServer()


## ChEMBL Method
@server.method()
async def get_chembl_info(chembl_id: str) -> dict:
    """Fetch basic compound metadata using a ChEMBL ID."""
    base_url = "https://www.ebi.ac.uk/chembl/api/data"

    async with httpx.AsyncClient() as client:
        # Get compound info
        compound_resp = await client.get(f"{base_url}/molecule/{chembl_id}")
        if compound_resp.status_code != 200:
            return {"error": f"Compound {chembl_id} not found."}
        compound = compound_resp.json()

        # Optionally get mechanism of action
        moa_resp = await client.get(f"{base_url}/mechanism?molecule_chembl_id={chembl_id}")
        moa = moa_resp.json().get("mechanisms", [])

    return {
        "pref_name": compound.get("pref_name"),
        "molecular_weight": compound.get("molecule_properties", {}).get("full_molweight"),
        "structure": compound.get("molecule_structures", {}).get("canonical_smiles"),
        "mechanism_of_action": moa[0].get("mechanism_of_action") if moa else None,
        "target_name": moa[0].get("target_chembl_id") if moa else None
    }

## PDB Method
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
