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
            false
        );

        // Act
        _context.Issues.Add(issue);
        await _context.SaveChangesAsync();

        // Assert
        var savedIssue = await _context.Issues.FindAsync("ISSUE-TEST-001");
        Assert.NotNull(savedIssue);
        Assert.Equal("ISSUE-TEST-001", savedIssue.Code);
        Assert.Equal("Test Issue", savedIssue.ShortDescription);
    }

    [Fact]
    public async Task QueryIssues_ShouldFilterByUrgent()
    {
        // Arrange
        var urgentIssue = new Issue("ISSUE-URGENT", "Urgent", "Urgent issue", true);
        var normalIssue = new Issue("ISSUE-NORMAL", "Normal", "Normal issue", false);

        _context.Issues.AddRange(urgentIssue, normalIssue);
        await _context.SaveChangesAsync();

        // Act
        var urgentIssues = await _context.Issues
            .Where(i => i.IsUrgent == true)
            .ToListAsync();

        var normalIssues = await _context.Issues
            .Where(i => i.IsUrgent == false)
            .ToListAsync();

        // Assert
        Assert.Single(urgentIssues);
        Assert.Equal("ISSUE-URGENT", urgentIssues[0].Code);
        
        Assert.Single(normalIssues);
        Assert.Equal("ISSUE-NORMAL", normalIssues[0].Code);
    }

    [Fact]
    public async Task GetAllIssues_ShouldReturnAllIssues()
    {
        // Arrange
        var issues = new[]
        {
            new Issue("ISSUE-001", "First", "First issue", true),
            new Issue("ISSUE-002", "Second", "Second issue", false),
            new Issue("ISSUE-003", "Third", "Third issue", true)
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
        var issue1 = new Issue("ISSUE-001", "Test", "Test", false);
        _context.Issues.Add(issue1);
        await _context.SaveChangesAsync();

        // Act & Assert - Try to add duplicate code should fail
        var issue2 = new Issue("ISSUE-001", "Duplicate", "Duplicate", true);
        _context.Issues.Add(issue2);
        
        await Assert.ThrowsAsync<DbUpdateException>(async () => 
            await _context.SaveChangesAsync());
    }

    public void Dispose()
    {
        _context.Database.EnsureDeleted();
        _context.Dispose();
    }
}

