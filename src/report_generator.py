"""
Markdown report generator for RAG Security Scanner v1.

This module converts scanner results into a clean Markdown report that is easy
to read, save, and include in a GitHub portfolio project.
"""

from typing import Any


def generate_markdown_report(
    results: list[dict[str, Any]],
    summary: dict[str, Any],
) -> str:
    """
    Generate a Markdown report from evaluated RAG security test results.
    """

    lines = [
        "# RAG Security Scanner Report",
        "",
        "## Summary",
        "",
        f"- Total Tests: {summary['total_tests']}",
        f"- Passed: {summary['passed']}",
        f"- Failed: {summary['failed']}",
        "",
        "## Risk Summary",
        "",
        f"- Low: {summary['risk_counts']['low']}",
        f"- Medium: {summary['risk_counts']['medium']}",
        f"- High: {summary['risk_counts']['high']}",
        f"- Critical: {summary['risk_counts']['critical']}",
        "",
        "## Findings",
        "",
    ]

    for result in results:
        status = "PASS" if result["passed"] else "FAIL"

        lines.extend(
            [
                f"### {result['test_id']} — {result['category']}",
                "",
                f"- Status: **{status}**",
                f"- Risk Level: **{result['risk_level'].upper()}**",
                "",
                "**User Query**",
                "",
                "```text",
                result["user_query"],
                "```",
                "",
                "**Retrieved Context**",
                "",
                "```text",
                result["retrieved_context"],
                "```",
                "",
                "**Mock RAG Response**",
                "",
                "```text",
                result["response"],
                "```",
                "",
                "**Reason**",
                "",
                result["reason"],
                "",
                "**Recommended Mitigation**",
                "",
                result["recommended_mitigation"],
                "",
                "---",
                "",
            ]
        )

    lines.extend(
        [
            "## Notes",
            "",
            "This report uses safe simulated test cases only.",
            "",
            "Retrieved context should be treated as untrusted input. A secure RAG system should use retrieved documents as evidence, not as instructions.",
            "",
        ]
    )

    return "\n".join(lines)


def save_markdown_report(report_text: str, output_path: str) -> None:
    """
    Save a Markdown report to disk.
    """

    with open(output_path, "w", encoding="utf-8") as report_file:
        report_file.write(report_text)