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
            Priority.MEDIUM
        );

        // Act
        _context.Issues.Add(issue);
        await _context.SaveChangesAsync();

        // Assert
        var savedIssue = await _context.Issues.FindAsync("ISSUE-TEST-001");
        Assert.NotNull(savedIssue);
        Assert.Equal("ISSUE-TEST-001", savedIssue.Code);
        Assert.Equal("Test Issue", savedIssue.ShortDescription);
        Assert.Equal(Priority.MEDIUM, savedIssue.Priority);
    }

    [Fact]
    public async Task QueryIssues_ShouldFilterByPriority()
    {
        // Arrange
        var high = new Issue("ISSUE-HIGH", "High", "High priority", Priority.HIGH);
        var medium = new Issue("ISSUE-MEDIUM", "Medium", "Medium priority", Priority.MEDIUM);
        var low = new Issue("ISSUE-LOW", "Low", "Low priority", Priority.LOW);

        _context.Issues.AddRange(high, medium, low);
        await _context.SaveChangesAsync();

        // Act
        var highIssues = await _context.Issues
            .Where(i => i.Priority == Priority.HIGH)
            .ToListAsync();

        var mediumIssues = await _context.Issues
            .Where(i => i.Priority == Priority.MEDIUM)
            .ToListAsync();

        var lowIssues = await _context.Issues
            .Where(i => i.Priority == Priority.LOW)
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
    public async Task Issue_CodeIsPrimaryKey()
    {
        // Arrange
        var issue1 = new Issue("ISSUE-001", "Test", "Test", Priority.LOW);
        _context.Issues.Add(issue1);
        await _context.SaveChangesAsync();
        
        // Detach the first issue so we can test the primary key constraint
        _context.Entry(issue1).State = EntityState.Detached;

        // Act & Assert - Try to add duplicate code should fail
        // Note: InMemory database throws ArgumentException, not DbUpdateException
        var issue2 = new Issue("ISSUE-001", "Duplicate", "Duplicate", Priority.HIGH);
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

