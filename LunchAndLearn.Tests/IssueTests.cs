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
            Priority.HIGH
        );

        // Assert
        Assert.Equal("ISSUE-001", issue.Code);
        Assert.Equal("Test Description", issue.ShortDescription);
        Assert.Equal("Long test description", issue.LongDescription);
        Assert.Equal(Priority.HIGH, issue.Priority);
    }

    [Fact]
    public void Issue_CanBeCreated_WithMediumPriority()
    {
        // Arrange & Act
        var issue = new Issue(
            "ISSUE-002",
            "Medium issue",
            "This is medium priority",
            Priority.MEDIUM
        );

        // Assert
        Assert.Equal(Priority.MEDIUM, issue.Priority);
    }

    [Fact]
    public void Issue_CanBeCreated_WithLowPriority()
    {
        // Arrange & Act
        var issue = new Issue(
            "ISSUE-003",
            "Low issue",
            "This is low priority",
            Priority.LOW
        );

        // Assert
        Assert.Equal(Priority.LOW, issue.Priority);
    }

    [Fact]
    public void Issue_RecordEquality_WorksCorrectly()
    {
        // Arrange
        var issue1 = new Issue("ISSUE-001", "Test", "Long", Priority.HIGH);
        var issue2 = new Issue("ISSUE-001", "Test", "Long", Priority.HIGH);
        var issue3 = new Issue("ISSUE-002", "Test", "Long", Priority.MEDIUM);

        // Assert
        Assert.Equal(issue1, issue2);
        Assert.NotEqual(issue1, issue3);
    }
}

