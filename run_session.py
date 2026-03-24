from core.execution.test_executor import run_session
from core.telementry import tracker
if __name__ == "__main__":
    candidate_id = input("Enter candidate ID: ")
    run_session("tasks/log_parser_v1", candidate_id)