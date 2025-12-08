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
            Priority.HIGH
        );

        // Assert
        Assert.Equal("ISSUE-001", issue.Code);
        Assert.Equal("Test Description", issue.ShortDescription);
        Assert.Equal("Long test description", issue.LongDescription);
        Assert.Equal(Priority.HIGH, issue.Priority);
    }

    [Fact]
    public void Issue_CanBeCreated_WithLowPriority()
    {
        // Arrange & Act
        var issue = new Issue(
            "ISSUE-002",
            "Non-urgent issue",
            "This is not urgent",
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
        var issue3 = new Issue("ISSUE-002", "Test", "Long", Priority.HIGH);

        // Assert
        Assert.Equal(issue1, issue2);
        Assert.NotEqual(issue1, issue3);
    }
}

