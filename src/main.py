"""
Command-line entry point for RAG Security Scanner v1.

Run from the project root:

    python src/main.py

Optional custom output paths:

    python src/main.py --json-output examples/sample_results.json --report-output examples/sample_report.md

Optional mock modes:

    python src/main.py --mock-mode demo
    python src/main.py --mock-mode secure
    python src/main.py --mock-mode vulnerable
"""

import argparse

from mock_rag import SUPPORTED_MOCK_MODES
from test_runner import print_summary, run_scanner


DEFAULT_JSON_OUTPUT = "examples/sample_results.json"
DEFAULT_REPORT_OUTPUT = "examples/sample_report.md"


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.
    """

    parser = argparse.ArgumentParser(
        description=(
            "Run safe simulated RAG security tests and generate JSON plus "
            "Markdown results."
        )
    )

    parser.add_argument(
        "--json-output",
        default=DEFAULT_JSON_OUTPUT,
        help=f"Path for JSON results output. Default: {DEFAULT_JSON_OUTPUT}",
    )

    parser.add_argument(
        "--report-output",
        default=DEFAULT_REPORT_OUTPUT,
        help=f"Path for Markdown report output. Default: {DEFAULT_REPORT_OUTPUT}",
    )

    parser.add_argument(
        "--mock-mode",
        default="demo",
        choices=sorted(SUPPORTED_MOCK_MODES),
        help="Mock response mode. Choices: demo, secure, vulnerable. Default: demo",
    )

    return parser.parse_args()


def main() -> None:
    """
    Run the scanner from the command line.
    """

    args = parse_arguments()

    scanner_output = run_scanner(
        json_output_path=args.json_output,
        report_output_path=args.report_output,
        mock_mode=args.mock_mode,
    )

    print_summary(scanner_output)

    print(f"JSON results saved to: {args.json_output}")
    print(f"Markdown report saved to: {args.report_output}")
    print()


if __name__ == "__main__":
    main()