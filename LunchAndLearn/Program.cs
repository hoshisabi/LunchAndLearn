using Microsoft.EntityFrameworkCore;
using System.Text.Json;
using System.Text.Json.Serialization;
using LunchAndLearn;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
builder.Services.AddOpenApi();

// Configure JSON serialization to use camelCase for API responses
builder.Services.ConfigureHttpJsonOptions(options =>
{
    options.SerializerOptions.PropertyNamingPolicy = JsonNamingPolicy.CamelCase;
    // Serialize enums (e.g., Priority) as strings
    options.SerializerOptions.Converters.Add(new JsonStringEnumConverter());
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
    
    // Check for priority filter in query string (HIGH|MEDIUM|LOW)
    if (httpContext.Request.Query.TryGetValue("priority", out var priorityValue))
    {
        var raw = priorityValue.ToString();
        if (!string.IsNullOrWhiteSpace(raw) && Enum.TryParse<Priority>(raw, true, out var prio))
        {
            query = query.Where(i => i.Priority == prio);
        }
    }
    
    return await query.ToListAsync();
})
.WithName("GetIssues");  // Updated name for clarity

app.Run();