namespace LunchAndLearn;

public enum Priority
{
    Low = 0,
    Medium = 1,
    High = 2
}

public record Issue(string Code, string ShortDescription, string LongDescription, Priority Priority);

