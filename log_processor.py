def parse_log_line(line: str) -> dict:
    if not isinstance(line, str):
        raise TypeError("Log line must be a string")
    
    parts = line.split("|")

    if len(parts) != 4:
        raise ValueError("Invalid log format")
    
    timestamp = parts[0].strip()
    user_id = parts[1].strip()
    status_str = parts[2].strip()   
    response_str = parts[3].strip()

    return{
        "timestamp": timestamp,
        "user_id": user_id,
        "status": status_str,
        "response": response_str    
    }