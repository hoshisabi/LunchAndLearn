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
    
    // Check for urgent filter in query string
    if (httpContext.Request.Query.TryGetValue("urgent", out var urgentValue))
    {
        if (bool.TryParse(urgentValue.ToString(), out var urgent))
        {
            query = query.Where(i => i.IsUrgent == urgent);
        }
    }
    
    return await query.ToListAsync();
})
.WithName("GetIssues");  // Updated name for clarity

app.Run();