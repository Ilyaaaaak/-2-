import os
import platform
import sys
import unittest


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)


def get_status_mark(result):
    if result.wasSuccessful():
        return "PASS"
    return "FAIL"


def write_report(result):
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return

    runner_os = os.environ.get("RUNNER_OS", platform.system())
    commit_sha = os.environ.get("GITHUB_SHA", "")
    short_sha = commit_sha[:7] if commit_sha else "local"
    status = get_status_mark(result)
    passed = result.testsRun - len(result.failures) - len(result.errors)

    lines = [
        "# Report Card",
        "",
        "## Overview",
        "",
        f"- Test status: **{status}**",
        f"- Tests passed: **{passed}/{result.testsRun}**",
        f"- Operating system: **{runner_os}**",
        f"- Python version: **{platform.python_version()}**",
        "",
        "## Test matrix",
        "",
        "| Check | Result |",
        "| --- | --- |",
        f"| Built? | {status} |",
        f"| Unit tests | {passed}/{result.testsRun} |",
        f"| Failures | {len(result.failures)} |",
        f"| Errors | {len(result.errors)} |",
        "",
        f"Report generated for commit `{short_sha}`.",
        "",
    ]

    with open(summary_path, "a", encoding="utf-8") as report:
        report.write("\n".join(lines))


def main():
    loader = unittest.TestLoader()
    suite = loader.discover("tests")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    write_report(result)

    if not result.wasSuccessful():
        sys.exit(1)


if __name__ == "__main__":
    main()
