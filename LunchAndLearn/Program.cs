using Microsoft.EntityFrameworkCore;
using System.Text.Json;
using LunchAndLearn;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
builder.Services.AddOpenApi();

// Configure JSON serialization to use camelCase for API responses
builder.Services.ConfigureHttpJsonOptions(options =>
{
    options.SerializerOptions.PropertyNamingPolicy = JsonNamingPolicy.CamelCase;
});

// Add DbContext for SQLite
builder.Services.AddDbContext<IssueDbContext>(options =>
    options.UseSqlite(builder.Configuration.GetConnectionString("DefaultConnection") ?? "Data Source=issues.db"));

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}

// Ensure database is created
using (var scope = app.Services.CreateScope())
{
    var dbContext = scope.ServiceProvider.GetRequiredService<IssueDbContext>();
    dbContext.Database.EnsureCreated();  // Creates the DB if it doesn't exist
    // Note: Database seeding is handled by seed_database.py
}

app.UseHttpsRedirection();

app.MapGet("/issues", async (IssueDbContext dbContext, HttpContext httpContext) =>
{
    var query = dbContext.Issues.AsQueryable();
    
    // Check for priority filter in query string
    if (httpContext.Request.Query.TryGetValue("priority", out var priorityValue))
    {
        var priorityStr = priorityValue.ToString();
        // Try case-insensitive parsing
        if (Enum.TryParse<Priority>(priorityStr, ignoreCase: true, out var priority))
        {
            query = query.Where(i => i.Priority == priority);
        }
    }
    
    // Order by priority: HIGH > MEDIUM > LOW
    query = query.OrderByDescending(i => i.Priority);
    
    return await query.ToListAsync();
})
.WithName("GetIssues");

app.Run();