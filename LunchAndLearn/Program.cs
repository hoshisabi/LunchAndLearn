using Microsoft.EntityFrameworkCore;
using LunchAndLearn;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
builder.Services.AddOpenApi();

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

app.MapGet("/issues", async (IssueDbContext dbContext) =>
{
    return await dbContext.Issues.ToListAsync();
})
.WithName("GetIssues");  // Updated name for clarity

app.Run();