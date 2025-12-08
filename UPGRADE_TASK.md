# Priority Feature Upgrade Tasks

## Overview
Enhance the issue tracking system to support a three-level priority system (HIGH, MEDIUM, LOW) instead of a simple boolean `IsUrgent` flag.

---

## Task 1: Data Model & API Endpoint (10 minutes)

### Subtask 1a: Create Priority Enum (2-3 min)
**File**: `LunchAndLearn/Priority.cs` (NEW)

Create a priority enum with three values:
```csharp
public enum Priority
{
    Low = 0,
    Medium = 1,
    High = 2
}
```

**What the AI tool should do**:
- Create the new file
- Define the enum with correct values
- Add to the LunchAndLearn namespace

---

### Subtask 1b: Update C# Models (3-4 min)
**Files**: 
- `LunchAndLearn/Issue.cs` (modify)
- `LunchAndLearn/IssueDbContext.cs` (modify)

**Changes needed**:
1. Update `Issue` record to use `Priority Priority` instead of `bool IsUrgent`
2. Update `IssueDbContext.OnModelCreating()` to:
   - Configure Priority as integer enum in database
   - Set default value to Medium

**What the AI tool should do**:
- Replace the IsUrgent property with Priority property
- Update the database configuration for the enum
- Ensure Entity Framework properly maps the enum

---

### Subtask 1c: Update API Endpoint (2-3 min)
**File**: `LunchAndLearn/Program.cs` (modify)

**Changes needed**:
- Update `/issues` endpoint to filter by `?priority=low|medium|high` instead of `?urgent=true|false`
- Use `Enum.TryParse<Priority>()` for parsing the query parameter

**What the AI tool should do**:
- Replace the urgent query parameter logic with priority filtering
- Ensure case-insensitive priority parsing

---

## Task 2: Python Scripts & Migration (8-9 minutes)

### Subtask 2a: Update Seed Script (2-3 min)
**File**: `LunchAndLearn/seed_database.py` (modify)

**Changes needed**:
- Update INSERT statement to use `Priority` column instead of `IsUrgent`
- Use priority values (0=Low, 1=Medium, 2=High) in seed data
- Mix of priorities: ISSUE-001→Medium, ISSUE-002→High, ISSUE-003→Low, etc.

**What the AI tool should do**:
- Replace IsUrgent with Priority in seed data
- Ensure proper integer values for each priority level

---

### Subtask 2b: Create Migration Script (3-4 min)
**File**: `LunchAndLearn/migrate_to_priority.py` (NEW)

**Must-haves**:
- Convert existing `IsUrgent` boolean to Priority enum
- Create automatic backup with timestamp
- Provide rollback functionality with `--rollback` flag
- Report conversion statistics (how many of each priority level)
- Handle both fresh and partially-migrated databases

**What the AI tool should do**:
- Create comprehensive migration with error handling
- Include backup/restore logic
- Add command-line argument parsing
- Provide clear user feedback

---

### Subtask 2c: Update Python Client (2-3 min)
**File**: `LunchAndLearn/client.py` (modify)

**Changes needed**:
- Replace `--urgent` / `--no-urgent` flags with `--priority low|medium|high`
- Update `get_issues()` method to accept priority parameter
- Update table format to show Priority instead of Urgent
- Add emoji indicators in simple format (🔴=High, 🟡=Medium, 🟢=Low)

**What the AI tool should do**:
- Update argument parsing
- Modify API call parameters
- Enhance output formatting with priority levels

---

## Task 3: Unit Tests (8-9 minutes)
**Files**:
- `LunchAndLearn.Tests/IssueTests.cs` (modify)
- `LunchAndLearn.Tests/IssueDbContextTests.cs` (modify)

**Changes needed**:
1. `IssueTests.cs`:
   - Replace bool tests with Priority enum tests
   - Test for High, Medium, and Low priority creation
   - Update equality tests to use Priority values

2. `IssueDbContextTests.cs`:
   - Update database save test to use Priority
   - Replace "FilterByUrgent" test with "FilterByPriority" test
   - Test filtering by each priority level (High, Medium, Low)
   - Update primary key tests to use Priority values

**Expected result**: 8 passing tests (up from 7)

**What the AI tool should do**:
- Refactor all test cases to use Priority enum
- Ensure comprehensive coverage of all three priority levels
- Verify tests pass with `dotnet test`

---

## Task 4: Documentation (5-6 minutes)
**File**: `README.md` (modify - focus on Testing section)

**Changes needed**:
1. Update test examples to show priority filtering (not urgent filtering)
2. Update expected test count from 7 to 8
3. Update sample API calls with `?priority=` instead of `?urgent=`
4. Update Python client examples with `--priority` flag

**What the AI tool should do**:
- Update testing section of README
- Ensure examples show new priority syntax
- Keep it concise and focused on testing

---

## Verification After Each Task

### After Task 1 (Data Model & API):
```bash
dotnet build
# Should compile successfully
```

### After Task 2 (Python Scripts):
```bash
# No verification needed - Python scripts are reviewed manually
```

### After Task 3 (Unit Tests):
```bash
dotnet test
# Expected: 8/8 tests passed
```

### After Task 4 (Documentation):
```bash
# No verification needed - documentation review only
```

---

## Final Verification (All Tasks Complete)

```bash
# Clean build
dotnet clean
dotnet build

# All tests pass
dotnet test
# Expected: 8/8 tests passed

# Release build succeeds
dotnet build -c Release
```

---

## Key Success Criteria

✅ All 8 unit tests pass (up from 7)
✅ Release build succeeds with no errors
✅ API correctly filters by `?priority=low|medium|high`
✅ Python client accepts `--priority` flag
✅ Migration script handles database conversion with backup
✅ Code compiles at each task completion
