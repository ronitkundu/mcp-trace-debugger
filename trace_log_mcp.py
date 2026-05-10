from mcp.server.fastmcp import FastMCP

mcp = FastMCP("trace-debugger")




def parse_logs(request_id):

    results = []

    with open("logs/microservices.log", "r") as file:
        for line in file:

            if f"requestId={request_id}" in line:

                parts = line.split()

                service = parts[2].split("=")[1]
                duration = int(parts[3].split("=")[1])

                results.append({
                    "service": service,
                    "duration": duration
                })

    return results

@mcp.tool('trace_request')
def trace_request(request_id: str):

    spans = parse_logs(request_id)

    flow = []
    slowest = {"service": "", "duration": 0}

    for span in spans:

        flow.append(f"{span['service']} ({span['duration']} ms)")

        if span["duration"] > slowest["duration"]:
            slowest = span

    return {
        "flow": flow,
        "root_cause": f"{slowest['service']} is slow ({slowest['duration']} ms)"
    }
    
    
if __name__ == "__main__":
    mcp.run()