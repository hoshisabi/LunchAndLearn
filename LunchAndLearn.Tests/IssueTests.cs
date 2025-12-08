namespace LunchAndLearn.Tests;

public class IssueTests
{
    [Fact]
    public void Issue_CanBeCreated_WithHighPriority()
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
    public void Issue_CanBeCreated_WithMediumPriority()
    {
        // Arrange & Act
        var issue = new Issue(
            "ISSUE-002",
            "Medium issue",
            "This is medium priority",
            Priority.Medium
        );

        // Assert
        Assert.Equal(Priority.Medium, issue.Priority);
    }

    [Fact]
    public void Issue_CanBeCreated_WithLowPriority()
    {
        // Arrange & Act
        var issue = new Issue(
            "ISSUE-003",
            "Low priority issue",
            "This has low priority",
            Priority.Low
        );

        // Assert
        Assert.Equal(Priority.Low, issue.Priority);
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
}

