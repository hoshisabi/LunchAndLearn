namespace LunchAndLearn.Tests;

public class IssueTests
{
    [Fact]
    public void Issue_CanBeCreated_WithAllProperties()
    {
        // Arrange & Act
        var issue = new Issue(
            "ISSUE-001",
            "Test Description",
            "Long test description",
            Priority.High
        );

        // Assert
        Assert.Equal("ISSUE-001", issue.Code);
        Assert.Equal("Test Description", issue.ShortDescription);
        Assert.Equal("Long test description", issue.LongDescription);
        Assert.Equal(Priority.High, issue.Priority);
    }

    [Fact]
    public void Issue_CanBeCreated_WithDifferentPriorities()
    {
        // Arrange & Act
        var lowIssue = new Issue(
            "ISSUE-002",
            "Low priority issue",
            "This is low priority",
            Priority.Low
        );
        
        var mediumIssue = new Issue(
            "ISSUE-003",
            "Medium priority issue",
            "This is medium priority",
            Priority.Medium
        );

        // Assert
        Assert.Equal(Priority.Low, lowIssue.Priority);
        Assert.Equal(Priority.Medium, mediumIssue.Priority);
    }

    [Fact]
    public void Issue_RecordEquality_WorksCorrectly()
    {
        // Arrange
        var issue1 = new Issue("ISSUE-001", "Test", "Long", Priority.High);
        var issue2 = new Issue("ISSUE-001", "Test", "Long", Priority.High);
        var issue3 = new Issue("ISSUE-002", "Test", "Long", Priority.High);

        // Assert
        Assert.Equal(issue1, issue2);
        Assert.NotEqual(issue1, issue3);
    }
    
    [Fact]
    public void Issue_PriorityOrdering_IsCorrect()
    {
        // Arrange
        var highIssue = new Issue("ISSUE-HIGH", "High", "High priority", Priority.High);
        var mediumIssue = new Issue("ISSUE-MEDIUM", "Medium", "Medium priority", Priority.Medium);
        var lowIssue = new Issue("ISSUE-LOW", "Low", "Low priority", Priority.Low);

        // Assert - Verify enum values for ordering
        Assert.True((int)Priority.High > (int)Priority.Medium);
        Assert.True((int)Priority.Medium > (int)Priority.Low);
        Assert.True((int)Priority.High > (int)Priority.Low);
    }
}

