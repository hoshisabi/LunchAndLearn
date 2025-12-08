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
            true
        );

        // Assert
        Assert.Equal("ISSUE-001", issue.Code);
        Assert.Equal("Test Description", issue.ShortDescription);
        Assert.Equal("Long test description", issue.LongDescription);
        Assert.True(issue.IsUrgent);
    }

    [Fact]
    public void Issue_CanBeCreated_AsNonUrgent()
    {
        // Arrange & Act
        var issue = new Issue(
            "ISSUE-002",
            "Non-urgent issue",
            "This is not urgent",
            false
        );

        // Assert
        Assert.False(issue.IsUrgent);
    }

    [Fact]
    public void Issue_RecordEquality_WorksCorrectly()
    {
        // Arrange
        var issue1 = new Issue("ISSUE-001", "Test", "Long", true);
        var issue2 = new Issue("ISSUE-001", "Test", "Long", true);
        var issue3 = new Issue("ISSUE-002", "Test", "Long", true);

        // Assert
        Assert.Equal(issue1, issue2);
        Assert.NotEqual(issue1, issue3);
    }
}

