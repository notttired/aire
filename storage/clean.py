import json

def parse_flight_data(raw_data):
    """
    Parses a dictionary where values are lists of JSON-encoded strings.
    Returns a clean dictionary of Python objects.
    """
    return {
        timestamp: [json.loads(flight_str) for flight_str in flights]
        for timestamp, flights in raw_data.items()
    }

# Execution
clean_data = parse_flight_data(raw_payload)

# Example: Accessing a specific price after parsing
if clean_data["2026-01-16T13:30:02.130086"]:
    print(clean_data["2026-01-16T13:30:02.130086"][0]['price']) # Output: 861.0