#!/usr/bin/env python3
"""
Python client tool for the LunchAndLearn C# service.
Provides a simple CLI to interact with the API.
"""

import requests
import json
import sys
import argparse
from typing import Optional


class LunchAndLearnClient:
    """Client for interacting with the LunchAndLearn API."""
    
    def __init__(self, base_url: str = "http://localhost:5099"):
        """
        Initialize the client.
        
        Args:
            base_url: Base URL of the API service
        """
        self.base_url = base_url.rstrip('/')
    
    def get_issues(self, priority: Optional[str] = None) -> list:
        """
        Fetch all issues from the API.
        
        Args:
            priority: Optional filter - 'low', 'medium', 'high', or None for all
        
        Returns:
            List of issue dictionaries
            
        Raises:
            requests.RequestException: If the API request fails
        """
        try:
            params = {}
            if priority is not None:
                params["priority"] = priority.lower()
            
            response = requests.get(
                f"{self.base_url}/issues",
                params=params,
                headers={"Accept": "application/json"},
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"Could not connect to {self.base_url}. "
                "Make sure the C# service is running."
            )
        except requests.exceptions.RequestException as e:
            raise requests.RequestException(f"API request failed: {e}")
    
    def print_issues(self, issues: Optional[list] = None, format: str = "table", priority: Optional[str] = None):
        """
        Print issues in a formatted way.
        
        Args:
            issues: List of issues to print. If None, fetches from API.
            format: Output format - 'table', 'json', or 'simple'
            priority: Optional filter - 'low', 'medium', 'high', or None for all
        """
        if issues is None:
            issues = self.get_issues(priority=priority)
        
        if not issues:
            print("No issues found.")
            return
        
        # Priority level indicators
        priority_icons = {
            "low": "🟢",
            "medium": "🟡",
            "high": "🔴"
        }
        
        if format == "json":
            print(json.dumps(issues, indent=2))
        elif format == "simple":
            for issue in issues:
                priority_val = issue.get("priority", "medium").lower()
                icon = priority_icons.get(priority_val, "❓")
                print(f"{icon} {issue.get('code')}: {issue.get('shortDescription')}")
        else:  # table format
            print(f"\n{'Code':<12} {'Priority':<10} {'Description':<40}")
            print("-" * 70)
            for issue in issues:
                priority_val = issue.get("priority", "Medium")
                desc = issue.get("shortDescription", "")[:38]
                print(f"{issue.get('code'):<12} {priority_val:<10} {desc:<40}")
            print(f"\nTotal: {len(issues)} issue(s)\n")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="LunchAndLearn API client tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python client.py                    # List all issues in table format
  python client.py --priority high    # Show only high priority issues
  python client.py --priority medium  # Show only medium priority issues
  python client.py --priority low     # Show only low priority issues
  python client.py --format json      # Output as JSON
  python client.py --format simple    # Simple one-line format
  python client.py --url http://localhost:7181  # Use different URL
        """
    )
    parser.add_argument(
        "--url",
        default="http://localhost:5099",
        help="Base URL of the API service (default: http://localhost:5099)"
    )
    parser.add_argument(
        "--format",
        choices=["table", "json", "simple"],
        default="table",
        help="Output format (default: table)"
    )
    parser.add_argument(
        "--priority",
        choices=["low", "medium", "high"],
        help="Filter issues by priority (low, medium, high)"
    )
    
    args = parser.parse_args()
    
    client = LunchAndLearnClient(base_url=args.url)
    
    try:
        client.print_issues(format=args.format, priority=args.priority)
    except ConnectionError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except requests.RequestException as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted by user.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

