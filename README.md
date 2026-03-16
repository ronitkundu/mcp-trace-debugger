# Trace Debugger MCP

A Model Context Protocol (MCP) server for analyzing and debugging slow requests in distributed microservices architectures by tracing request flows through service logs.

## Overview

Trace Debugger helps you identify performance bottlenecks in your microservices by:
- Parsing structured service logs
- Tracking request flows across services
- Identifying the slowest service in each request chain
- Providing root cause analysis for slow API responses

## Features

- **Request Tracing**: Follow a request through all microservices
- **Performance Analysis**: Identify which service is causing delays
- **Root Cause Detection**: Pinpoint the bottleneck service automatically
- **MCP Integration**: Works with any MCP-compatible client

## Installation

1. Clone or download this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - **Windows**: `.\venv\Scripts\Activate.ps1`
   - **macOS/Linux**: `source venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install mcp fastmcp
   ```

## Configuration

Configure the MCP server in your `.vscode/mcp.json`:

```json
{
  "servers": {
    "trace-debugger": {
      "type": "stdio",
      "command": "./venv/Scripts/python",
      "args": ["trace_log_mcp.py"],
      "cwd": "c:/Users/ronit/ai/mcp-trace-debugger"
    }
  }
}
```

## Log Format

Logs should be in `microservices.log` with the following format:

```
<timestamp> requestId=<id> service=<service_name> duration=<milliseconds>
```

Example:
```
2026-03-14 requestId=123 service=Gateway duration=20
2026-03-14 requestId=123 service=OrderService duration=120
2026-03-14 requestId=123 service=PaymentService duration=900
2026-03-14 requestId=123 service=InventoryService duration=50
```

## Usage

### Using the `trace_request` Tool

Call the `trace_request` tool with a request ID to analyze its performance:

**Input:**
```
trace_request(request_id="123")
```

**Output:**
```json
{
  "flow": [
    "Gateway (20 ms)",
    "OrderService (120 ms)",
    "PaymentService (900 ms)",
    "InventoryService (50 ms)"
  ],
  "root_cause": "PaymentService is slow (900 ms)"
}
```

## Interpreting Results

- **flow**: The complete trace of services called during the request, with execution time for each
- **root_cause**: The service that took the longest to respond, indicating where to focus optimization efforts

## Example Scenario

For request ID `123`:
- Total services: 4
- Total time: 1,090 ms
- Bottleneck: PaymentService (900 ms) accounts for ~83% of the time

**Action**: Investigate and optimize PaymentService to improve overall API response time.

## Development

To extend this debugger:

1. Modify `parse_logs()` to handle different log formats
2. Add new analysis tools by creating new functions with `@mcp.tool()` decorator
3. Examples:
   - Average response times per service
   - Service dependency graphs
   - Performance trends over time

## Running the Server

```bash
python trace_log_mcp.py
```

The server will start and listen for MCP client connections.

## Requirements

- Python 3.7+
- mcp
- fastmcp

## License

MIT
