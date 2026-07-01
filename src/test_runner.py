"""
Test runner for RAG Security Scanner v1.

This module connects the main parts of the scanner:

1. Load safe RAG security test cases.
2. Generate mock RAG responses.
3. Evaluate each response.
4. Build a summary.
5. Save JSON results.
6. Generate and save a Markdown report.
"""

import json
import os
from typing import Any

from evaluator import evaluate_response, evaluate_results
from mock_rag import DEFAULT_MOCK_MODE, generate_mock_response
from report_generator import generate_markdown_report, save_markdown_report
from test_cases import load_test_cases


def run_scanner(
    json_output_path: str,
    report_output_path: str,
    mock_mode: str = DEFAULT_MOCK_MODE,
) -> dict[str, Any]:
    """
    Run the full scanner workflow.

    Returns a dictionary containing:
    - summary
    - results
    """

    test_cases = load_test_cases()
    results = []

    for test_case in test_cases:
        response = generate_mock_response(test_case=test_case, mode=mock_mode)
        result = evaluate_response(test_case=test_case, response=response)
        results.append(result)

    summary = evaluate_results(results)

    scanner_output = {
        "project": "RAG Security Scanner v1",
        "mode": mock_mode,
        "summary": summary,
        "results": results,
    }

    save_json_results(scanner_output, json_output_path)

    report_text = generate_markdown_report(results=results, summary=summary)
    save_markdown_report(report_text=report_text, output_path=report_output_path)

    return scanner_output


def save_json_results(scanner_output: dict[str, Any], output_path: str) -> None:
    """
    Save scanner results to a JSON file.
    """

    output_dir = os.path.dirname(output_path)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(scanner_output, json_file, indent=2)


def print_summary(scanner_output: dict[str, Any]) -> None:
    """
    Print a clean command-line summary after the scanner runs.
    """

    summary = scanner_output["summary"]
    risk_counts = summary["risk_counts"]

    print()
    print("RAG Security Scanner v1")
    print("=======================")
    print(f"Mode: {scanner_output['mode']}")
    print()
    print(f"Total tests: {summary['total_tests']}")
    print(f"Passed:      {summary['passed']}")
    print(f"Failed:      {summary['failed']}")
    print()
    print("Risk levels:")
    print(f"  Low:       {risk_counts['low']}")
    print(f"  Medium:    {risk_counts['medium']}")
    print(f"  High:      {risk_counts['high']}")
    print(f"  Critical:  {risk_counts['critical']}")
    print()