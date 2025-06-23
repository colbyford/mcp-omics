from fastmcp import FastMCP
import httpx

server = FastMCP("mcp-omics")
headers = {"Accept": "application/json"}


## ChEMBL Method
@server.tool()
async def get_chembl_info(chembl_id: str) -> dict:
    """
    Fetch compound metadata using a ChEMBL ID.
    Example: 'CHEMBL25'
    This function retrieves the compound's preferred name, molecular weight,
    structure (SMILES), mechanism of action, and target information.
    """
    base_url = "https://www.ebi.ac.uk/chembl/api/data"

    async with httpx.AsyncClient() as client:
        # Get compound info
        compound_resp = await client.get(f"{base_url}/molecule/{chembl_id}", headers=headers)
        if compound_resp.status_code != 200:
            return {"error": f"Compound {chembl_id} not found."}

    return compound_resp.json()

## PDB Method
@server.tool()
async def get_pdb_info(pdb_id: str) -> dict:
    """
    Fetch information about a protein from the Protein Data Bank using its PDB ID.
    Example: '7WRL'.
    This function retrieves the protein's title, experimental method,
    resolution, and release date.
    """
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

## HUGO Gene Method
@server.tool()
async def get_gene_info(gene_symbol: str) -> dict:
    """
    Fetch gene information from HUGO.
    Example: 'BRCA1'.
    This function retrieves the gene's name, description, and other IDs.
    """
    base_url = "https://rest.genenames.org/fetch/symbol"

    async with httpx.AsyncClient() as client:
        response = client.get(f"{base_url}/{gene_symbol}", headers=headers)

    if response.status_code != 200:
        return {"error": f"HUGO Symbol '{gene_symbol}' not found."}

    gene_info = response.json()

    return gene_info

## PubChem Method
@server.tool()
async def get_pubchem_info(pubchem_id: str) -> dict:
    """
    Fetch basic compound information using a PubChem CID.
    Example: '2244' for caffeine.
    This function retrieves the compound's name, molecular weight, and SMILES representation.
    """
    base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid"

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/{pubchem_id}/JSON")

    if response.status_code != 200:
        return {"error": f"PubChem CID '{pubchem_id}' not found."}

    compound_info = response.json()

    return compound_info

@server.tool()
async def get_uniprot_info(uniprot_id: str) -> dict:
    """
    Fetch basic protein information using a UniProt ID.
    Example: 'P43220' for the GLP-1 Receptor.
    This function retrieves the protein name and function information.
    """
    base_url = "https://rest.uniprot.org/uniprotkb"

    params = {
        "fields": [
            "accession",
            "protein_name",
            "cc_function",
            "ft_binding"
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/{uniprot_id}", headers=headers, params=params)

    if response.status_code != 200:
        return {"error": f"UniProt ID '{uniprot_id}' not found."}

    uniprot_info = response.json()

    return uniprot_info


## Run the MCP server
if __name__ == "__main__":
    server.run()
