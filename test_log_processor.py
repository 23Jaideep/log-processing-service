import pytest
from log_processor import (
    parse_log_line,
    compute_error_rate,
    compute_avg_response_time,
    count_unique_users,
)

# -------- parse_log_line --------

def test_parse_valid_line():
    line = "2026-02-15T12:00:00 | user_1 | 200 | 100"
    result = parse_log_line(line)

    assert result["timestamp"] == "2026-02-15T12:00:00"
    assert result["user_id"] == "user_1"
    assert result["status_code"] == 200
    assert result["response_time"] == 100.0


def test_parse_invalid_format():
    with pytest.raises(ValueError):
        parse_log_line("invalid line")


def test_parse_non_string():
    with pytest.raises(TypeError):
        parse_log_line(123)


def test_parse_negative_response_time():
    with pytest.raises(ValueError):
        parse_log_line("2026-02-15T12:00:00 | user_1 | 200 | -10")


# -------- compute_error_rate --------

def test_error_rate():
    logs = [
        {"status_code": 200},
        {"status_code": 500},
    ]
    assert compute_error_rate(logs) == 0.5


def test_error_rate_empty():
    assert compute_error_rate([]) == 0.0


# -------- compute_avg_response_time --------

def test_avg_response_time():
    logs = [
        {"response_time": 100},
        {"response_time": 300},
    ]
    assert compute_avg_response_time(logs) == 200.0


def test_avg_response_time_empty():
    assert compute_avg_response_time([]) == 0.0


# -------- count_unique_users --------

def test_unique_users():
    logs = [
        {"user_id": "u1"},
        {"user_id": "u2"},
        {"user_id": "u1"},
    ]
    assert count_unique_users(logs) == 2


def test_unique_users_empty():
    assert count_unique_users([]) == 0
