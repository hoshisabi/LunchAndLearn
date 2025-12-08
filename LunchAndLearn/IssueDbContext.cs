using Microsoft.EntityFrameworkCore;

namespace LunchAndLearn;

public class IssueDbContext : DbContext
{
    public DbSet<Issue> Issues { get; set; }

    public IssueDbContext(DbContextOptions<IssueDbContext> options) : base(options) { }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Issue>(entity =>
        {
            entity.HasKey(i => i.Code);
            entity.Property(i => i.Code).IsRequired().HasMaxLength(50);
            entity.Property(i => i.ShortDescription).IsRequired().HasMaxLength(200);
            entity.Property(i => i.LongDescription).IsRequired();
            entity.Property(i => i.Priority)
                .IsRequired()
                .HasConversion<int>()  // Store enum as integer in database
                .HasDefaultValue(Priority.Medium);
        });
    }
}
