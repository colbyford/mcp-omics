# mcp-omics
A Model Context Protocol server for retrieving -omics data from various online sources.


## Run the MCP server
To run the MCP server, you need to have FastMCP installed. You can install it using pip:

```bash
pip install -r requirements.txt
```

Then, you can run the server using the following command:

```bash
fastmcp run server.py
```

```bash
curl http://localhost:5000/.well-known/mcp/tools.json
```


## Example: Communicate with the MCP server locally in Ollama using MCPHost

1. Pull the desired model from Ollama:

```bash
ollama run qwen2.5:0.5b
```

Note that you can use any of the models that support "[tools](https://ollama.com/search?c=tools)". Avoid the "thinking" models, as their outputs are overly verbose for this use case.

2. Install the MCPHost package:

```bash
go install github.com/mark3labs/mcphost@latest
## Make sure mcphost is in your PATH 
# export PATH="$HOME/go/bin:$PATH"
```

3. Run MCPHost with the model you pulled from Ollama:

```bash
# mcphost -m ollama:qwen3:0.6b --config .mcphost.json
mcphost -m ollama:qwen2.5:0.5b --config .mcphost.json
```

4. Run some examples:

- **PDB** - "Tell me about PDB 5JXE."
- **ChEMBL** - "In the ChEMBL database, what is CHEMBL112?"