#!/usr/bin/env python3
"""
Unit tests for the LunchAndLearn Python client.
Tests the client functionality with mocking to avoid requiring a running server.
"""

import pytest
from unittest.mock import Mock, patch
from client import LunchAndLearnClient


class TestLunchAndLearnClient:
    """Test cases for LunchAndLearnClient class."""
    
    @pytest.fixture
    def client(self):
        """Create a client instance for testing."""
        return LunchAndLearnClient(base_url="http://localhost:5099")
    
    @pytest.fixture
    def sample_issues(self):
        """Sample issue data for testing with priority levels."""
        return [
            {
                "code": "ISSUE-001",
                "shortDescription": "Login button not working",
                "longDescription": "Users report that the login button is unresponsive.",
                "priority": "medium",
            },
            {
                "code": "ISSUE-002",
                "shortDescription": "Performance lag",
                "longDescription": "App slows down after extended use.",
                "priority": "high",
            },
            {
                "code": "ISSUE-003",
                "shortDescription": "UI misalignment",
                "longDescription": "Elements are misaligned on high-resolution screens.",
                "priority": "low",
            }
        ]
    
    def test_get_issues_all(self, client, sample_issues):
        """Test getting all issues without filter."""
        with patch('client.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = sample_issues
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            result = client.get_issues()
            
            assert len(result) == 3
            assert result[0]["code"] == "ISSUE-001"
            mock_get.assert_called_once()
            # Verify no priority parameter was passed
            call_args = mock_get.call_args
            assert "priority" not in call_args.kwargs.get("params", {})

    def test_get_issues_high_only(self, client, sample_issues):
        """Test getting only high priority issues."""
        high_issues = [issue for issue in sample_issues if issue["priority"] == "high"]
        
        with patch('client.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = high_issues
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            result = client.get_issues(priority="high")
            
            assert len(result) == 1
            assert result[0]["code"] == "ISSUE-002"
            assert result[0]["priority"] == "high"
            # Verify priority parameter was passed
            call_args = mock_get.call_args
            assert call_args.kwargs["params"]["priority"] == "high"

    def test_get_issues_low_only(self, client, sample_issues):
        """Test getting only low priority issues."""
        low_issues = [issue for issue in sample_issues if issue["priority"] == "low"]
        
        with patch('client.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = low_issues
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            result = client.get_issues(priority="low")
            
            assert len(result) == 1
            assert all(issue["priority"] == "low" for issue in result)
            # Verify priority parameter was passed as low
            call_args = mock_get.call_args
            assert call_args.kwargs["params"]["priority"] == "low"
    
    def test_print_issues_table_format(self, client, sample_issues, capsys):
        """Test printing issues in table format."""
        client.print_issues(issues=sample_issues, format="table")
        
        captured = capsys.readouterr()
        assert "Code" in captured.out
        assert "Priority" in captured.out
        assert "ISSUE-001" in captured.out
        assert "ISSUE-002" in captured.out
        assert "Total: 3 issue(s)" in captured.out
    
    def test_print_issues_json_format(self, client, sample_issues, capsys):
        """Test printing issues in JSON format."""
        import json
        
        client.print_issues(issues=sample_issues, format="json")
        
        captured = capsys.readouterr()
        # Verify it's valid JSON
        parsed = json.loads(captured.out)
        assert len(parsed) == 3
        assert parsed[0]["code"] == "ISSUE-001"
    
    def test_print_issues_simple_format(self, client, sample_issues, capsys):
        """Test printing issues in simple format."""
        client.print_issues(issues=sample_issues, format="simple")
        
        captured = capsys.readouterr()
        assert "ISSUE-001" in captured.out
        assert "ISSUE-002" in captured.out
        # Should show emoji indicators for priorities
        assert "🔴" in captured.out  # High priority
        assert "🟡" in captured.out or "🟢" in captured.out  # Medium/Low priority
    
    def test_print_issues_empty_list(self, client, capsys):
        """Test printing when no issues are found."""
        client.print_issues(issues=[])
        
        captured = capsys.readouterr()
        assert "No issues found." in captured.out

