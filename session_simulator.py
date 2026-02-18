import subprocess
import time


def run_tests(file):
    result = subprocess.run(
        ["pytest", file, "-q"],
        capture_output=True,
        text=True
    )
    print(result.stdout)   # <-- add this line
    print(result.stderr)
    return result.returncode


def simulate_session():
    start = time.time()
    runs = 0

    # Phase 1 — Core
    while True:
        input("Press Enter to run core tests...")
        runs += 1

        code = run_tests("test_core.py")

        if code == 0:
            break

    core_end = time.time()

    print("\nCore tests passed!")
    print("Core runs:", runs)
    print("Core time:", core_end - start)

    # Phase 2 — Mutation
    print("\nRunning mutation tests...")
    mutation_runs = 0

    while True:
        input("Press Enter to run mutation tests...")
        mutation_runs += 1

        mutation_code = run_tests("test_mutation.py")

        if mutation_code == 0:
            print("Mutation tests PASSED.")
            break
        else:
            print("Mutation tests FAILED\n")
    print("Mutation runs:", mutation_runs)

    end = time.time()

    print("\nTotal session time:", end - start)


simulate_session()
