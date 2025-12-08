using Microsoft.EntityFrameworkCore;

namespace LunchAndLearn.Tests;

public class IssueDbContextTests : IDisposable
{
    private readonly IssueDbContext _context;

    public IssueDbContextTests()
    {
        var options = new DbContextOptionsBuilder<IssueDbContext>()
            .UseInMemoryDatabase(databaseName: Guid.NewGuid().ToString())
            .Options;

        _context = new IssueDbContext(options);
        _context.Database.EnsureCreated();
    }

    [Fact]
    public async Task AddIssue_ShouldSaveToDatabase()
    {
        // Arrange
        var issue = new Issue(
            "ISSUE-TEST-001",
            "Test Issue",
            "This is a test issue",
            Priority.LOW
        );

        // Act
        _context.Issues.Add(issue);
        await _context.SaveChangesAsync();

        // Assert
        var savedIssue = await _context.Issues.FindAsync("ISSUE-TEST-001");
        Assert.NotNull(savedIssue);
        Assert.Equal("ISSUE-TEST-001", savedIssue.Code);
        Assert.Equal(Priority.LOW, savedIssue.Priority);
    }

    [Fact]
    public async Task QueryIssues_ShouldFilterByPriority()
    {
        // Arrange
        var highPriorityIssue = new Issue("ISSUE-HIGH", "High", "High priority issue", Priority.HIGH);
        var lowPriorityIssue = new Issue("ISSUE-LOW", "Low", "Low priority issue", Priority.LOW);

        _context.Issues.AddRange(highPriorityIssue, lowPriorityIssue);
        await _context.SaveChangesAsync();

        // Act
        var highPriorityIssues = await _context.Issues
            .Where(i => i.Priority == Priority.HIGH)
            .ToListAsync();

        var lowPriorityIssues = await _context.Issues
            .Where(i => i.Priority == Priority.LOW)
            .ToListAsync();

        // Assert
        Assert.Single(highPriorityIssues);
        Assert.Equal("ISSUE-HIGH", highPriorityIssues[0].Code);
        
        Assert.Single(lowPriorityIssues);
        Assert.Equal("ISSUE-LOW", lowPriorityIssues[0].Code);
    }

    [Fact]
    public async Task GetAllIssues_ShouldReturnAllIssues()
    {
        // Arrange
        var issues = new[]
        {
            new Issue("ISSUE-001", "First", "First issue", Priority.HIGH),
            new Issue("ISSUE-002", "Second", "Second issue", Priority.LOW),
            new Issue("ISSUE-003", "Third", "Third issue", Priority.MEDIUM)
        };

        _context.Issues.AddRange(issues);
        await _context.SaveChangesAsync();

        // Act
        var allIssues = await _context.Issues.ToListAsync();

        // Assert
        Assert.Equal(3, allIssues.Count);
    }

    [Fact]
    public void Issue_CodeIsPrimaryKey()
    {
        // Arrange
        var issue1 = new Issue("ISSUE-001", "Test", "Test", Priority.LOW);
        _context.Issues.Add(issue1);
        _context.SaveChanges();

        // Act & Assert - Try to add duplicate code should fail
        var issue2 = new Issue("ISSUE-001", "Duplicate", "Duplicate", Priority.HIGH);
        Assert.Throws<InvalidOperationException>(() => _context.Issues.Add(issue2));
    }

    public void Dispose()
    {
        _context.Database.EnsureDeleted();
        _context.Dispose();
    }
}

