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

    try:
        status_code = int(status_str)
    except ValueError:
        raise ValueError("Status code must be numeric")
    
    try:
        response_time = int(response_str)
    except ValueError:
        raise ValueError("Response time must be numeric")
    
    if response_time < 0:
        raise ValueError("Response time cannot be negative")

    return{
        "timestamp": timestamp,
        "user_id": user_id,
        "status_code": status_code,
        "response_time": response_time    
    }

def compute_error_rate(logs: list) -> float:
    if not logs:
        return 0.0
    
    total = len(logs)
    errors = 0

    for log in logs:
        if log["status_code"] >= 400:
            errors+=1

    return errors / total

def compute_avg_response_time(logs: list) -> float:
    if not logs:
        return 0.0
    
    total_time = 0.0

    for log in logs:
        total_time += log["response_time"]

    return total_time / len(logs)

def count_unique_users(logs: list) -> int:
    unique_users = set()

    for log in logs:
        unique_users.add(log["user_id"])

    return len(unique_users)