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
        """Sample issue data for testing."""
        return [
            {
                "code": "ISSUE-001",
                "shortDescription": "Login button not working",
                "longDescription": "Users report that the login button is unresponsive.",
                "isUrgent": False
            },
            {
                "code": "ISSUE-002",
                "shortDescription": "Performance lag",
                "longDescription": "App slows down after extended use.",
                "isUrgent": True
            },
            {
                "code": "ISSUE-003",
                "shortDescription": "UI misalignment",
                "longDescription": "Elements are misaligned on high-resolution screens.",
                "isUrgent": False
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
            # Verify no urgent parameter was passed
            call_args = mock_get.call_args
            assert "urgent" not in call_args.kwargs.get("params", {})
    
    def test_get_issues_urgent_only(self, client, sample_issues):
        """Test getting only urgent issues."""
        urgent_issues = [issue for issue in sample_issues if issue["isUrgent"]]
        
        with patch('client.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = urgent_issues
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            result = client.get_issues(urgent=True)
            
            assert len(result) == 1
            assert result[0]["code"] == "ISSUE-002"
            assert result[0]["isUrgent"] is True
            # Verify urgent parameter was passed
            call_args = mock_get.call_args
            assert call_args.kwargs["params"]["urgent"] == "true"
    
    def test_get_issues_non_urgent_only(self, client, sample_issues):
        """Test getting only non-urgent issues."""
        non_urgent_issues = [issue for issue in sample_issues if not issue["isUrgent"]]
        
        with patch('client.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = non_urgent_issues
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            result = client.get_issues(urgent=False)
            
            assert len(result) == 2
            assert all(not issue["isUrgent"] for issue in result)
            # Verify urgent parameter was passed as false
            call_args = mock_get.call_args
            assert call_args.kwargs["params"]["urgent"] == "false"
    
    def test_print_issues_table_format(self, client, sample_issues, capsys):
        """Test printing issues in table format."""
        client.print_issues(issues=sample_issues, format="table")
        
        captured = capsys.readouterr()
        assert "Code" in captured.out
        assert "Urgent" in captured.out
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
        assert "🔴 URGENT" in captured.out  # Should show urgent indicator
        assert "⚪" in captured.out  # Should show non-urgent indicator
    
    def test_print_issues_empty_list(self, client, capsys):
        """Test printing when no issues are found."""
        client.print_issues(issues=[])
        
        captured = capsys.readouterr()
        assert "No issues found." in captured.out

