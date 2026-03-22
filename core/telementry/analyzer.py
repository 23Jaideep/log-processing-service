# ---- Time Between Runs ----
def compute_time_between_runs(events):
    times = [
        e["timestamp"]
        for e in events
        if e["event_type"] == "test_run"
    ]

    if len(times) < 2:
        return None

    intervals = [
        times[i] - times[i-1]
        for i in range(1, len(times))
    ]

    return {
        "avg": sum(intervals) / len(intervals),
        "min": min(intervals),
        "max": max(intervals)
    }


# ---- Recovery ----
def compute_recovery(events):
    recoveries = []
    last_pass_time = None
    in_regression = False

    for e in events:
        if e["event_type"] != "test_run":
            continue

        if e["passed"]:
            if in_regression:
                recoveries.append(e["timestamp"] - last_pass_time)
                in_regression = False
            last_pass_time = e["timestamp"]

        else:
            if last_pass_time is not None:
                in_regression = True

    return recoveries


# ---- Progress ----
def compute_progress(events):
    progress = [
        e["tests_passed"]
        for e in events
        if e["event_type"] == "test_run"
    ]

    if len(progress) < 2:
        return None

    improvements = sum(
        1 for i in range(1, len(progress))
        if progress[i] > progress[i-1]
    )

    return {
        "improvements": improvements,
        "final": progress[-1],
        "max": max(progress)
    }


# ---- Scope Discipline ----
ALLOWED_FILES = {"parser.py", "aggregator.py"}

def compute_scope_violations(events):
    violations = []

    for e in events:
        if e["event_type"] != "test_run":
            continue

        for f in e["diff"]["files_changed"]:
            if f not in ALLOWED_FILES:
                violations.append(f)

    return {
        "count": len(violations),
        "files": list(set(violations))
    }