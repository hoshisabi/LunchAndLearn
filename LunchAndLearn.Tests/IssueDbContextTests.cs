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
            Priority.Medium
        );

        // Act
        _context.Issues.Add(issue);
        await _context.SaveChangesAsync();

        // Assert
        var savedIssue = await _context.Issues.FindAsync("ISSUE-TEST-001");
        Assert.NotNull(savedIssue);
        Assert.Equal("ISSUE-TEST-001", savedIssue.Code);
        Assert.Equal("Test Issue", savedIssue.ShortDescription);
        Assert.Equal(Priority.Medium, savedIssue.Priority);
    }

    [Fact]
    public async Task QueryIssues_ShouldFilterByPriority()
    {
        // Arrange
        var highPriorityIssue = new Issue("ISSUE-HIGH", "High Priority", "High priority issue", Priority.High);
        var mediumPriorityIssue = new Issue("ISSUE-MEDIUM", "Medium Priority", "Medium priority issue", Priority.Medium);
        var lowPriorityIssue = new Issue("ISSUE-LOW", "Low Priority", "Low priority issue", Priority.Low);

        _context.Issues.AddRange(highPriorityIssue, mediumPriorityIssue, lowPriorityIssue);
        await _context.SaveChangesAsync();

        // Act
        var highIssues = await _context.Issues
            .Where(i => i.Priority == Priority.High)
            .ToListAsync();

        var mediumIssues = await _context.Issues
            .Where(i => i.Priority == Priority.Medium)
            .ToListAsync();

        var lowIssues = await _context.Issues
            .Where(i => i.Priority == Priority.Low)
            .ToListAsync();

        // Assert
        Assert.Single(highIssues);
        Assert.Equal("ISSUE-HIGH", highIssues[0].Code);
        
        Assert.Single(mediumIssues);
        Assert.Equal("ISSUE-MEDIUM", mediumIssues[0].Code);

        Assert.Single(lowIssues);
        Assert.Equal("ISSUE-LOW", lowIssues[0].Code);
    }

    [Fact]
    public async Task GetAllIssues_ShouldReturnAllIssues()
    {
        // Arrange
        var issues = new[]
        {
            new Issue("ISSUE-001", "First", "First issue", Priority.High),
            new Issue("ISSUE-002", "Second", "Second issue", Priority.Medium),
            new Issue("ISSUE-003", "Third", "Third issue", Priority.Low)
        };

        _context.Issues.AddRange(issues);
        await _context.SaveChangesAsync();

        // Act
        var allIssues = await _context.Issues.ToListAsync();

        // Assert
        Assert.Equal(3, allIssues.Count);
    }

    [Fact]
    public async Task Issue_CodeIsPrimaryKey()
    {
        // Arrange
        var issue1 = new Issue("ISSUE-001", "Test", "Test", Priority.High);
        _context.Issues.Add(issue1);
        await _context.SaveChangesAsync();
        
        // Detach the first issue so we can test the primary key constraint
        _context.Entry(issue1).State = EntityState.Detached;

        // Act & Assert - Try to add duplicate code should fail
        // Note: InMemory database throws ArgumentException, not DbUpdateException
        var issue2 = new Issue("ISSUE-001", "Duplicate", "Duplicate", Priority.Medium);
        _context.Issues.Add(issue2);
        
        await Assert.ThrowsAsync<ArgumentException>(async () => 
            await _context.SaveChangesAsync());
    }

    public void Dispose()
    {
        _context.Database.EnsureDeleted();
        _context.Dispose();
    }
}

