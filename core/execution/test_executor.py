import subprocess
import time
from core.telementry.tracker import SessionTracker
import re

def run_tests(file):
    result = subprocess.run(
        ["pytest", file, "-q"],
        capture_output=True,
        text=True
    )
    output = result.stdout
    print(output)   # <-- add this line
    print(result.stderr)
    return result.returncode, output

import re

def extract_passed_tests(output):
    match = re.search(r"(\\d+) passed", output)
    if match:
        return int(match.group(1))
    return 0


def run_session(task_path: str):
    tracker = SessionTracker()
    start = time.time()

    # -------- Phase 1: Core --------
    while True:
        input("Press Enter to run core tests...")

        code, output = run_tests(f"{task_path}/tests/test_core.py")

        passed_tests = extract_passed_tests(output)
        tracker.record_progress(passed_tests)

        passed = (code == 0)
        tracker.record_core_run(passed)

        if passed:
            print("Core tests PASSED\n")
            break
        else:
            print("Core tests FAILED\n")

    # -------- Phase 2: Mutation --------
    print("Running mutation tests...")

    while True:
        input("Press Enter to run mutation tests...")

        mutation_code, mutation_output = run_tests(f"{task_path}/tests/test_mutation.py")
        passed_mutation_tests = extract_passed_tests(mutation_output)
        tracker.record_progress(passed_mutation_tests)
        passed = (mutation_code == 0)
        tracker.record_mutation_run(passed)

        if passed:
            print("Mutation tests PASSED\n")
            break
        else:
            print("Mutation tests FAILED\n")

    end = time.time()

    print("\nTotal session time:", end - start)
    print(tracker.summary())



if __name__ == "__main__":
    run_session("tasks/log_parser_v1")
