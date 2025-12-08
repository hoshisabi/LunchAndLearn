# Priority Feature Upgrade

## Overview
Enhance the issue tracking system to support a three-level priority system (HIGH, MEDIUM, LOW) instead of a simple boolean `IsUrgent` flag.

**Estimated time: 25-40 minutes** (5-8 minutes per AI tool)

---

## Implementation Steps

### Step 1: Create Priority Enum (2-3 min)
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

### Step 2: Update C# Models (3-4 min)
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

### Step 3: Update API Endpoint (2-3 min)
**File**: `LunchAndLearn/Program.cs` (modify)

**Changes needed**:
- Update `/issues` endpoint to filter by `?priority=low|medium|high` instead of `?urgent=true|false`
- Use `Enum.TryParse<Priority>()` for parsing the query parameter

**What the AI tool should do**:
- Replace the urgent query parameter logic with priority filtering
- Ensure case-insensitive priority parsing

---

### Step 4: Update Seed Script (2-3 min)
**File**: `LunchAndLearn/seed_database.py` (modify)

**Changes needed**:
- Update INSERT statement to use `Priority` column instead of `IsUrgent`
- Use priority values (0=Low, 1=Medium, 2=High) in seed data
- Mix of priorities: ISSUE-001→Medium, ISSUE-002→High, ISSUE-003→Low, etc.

**What the AI tool should do**:
- Replace IsUrgent with Priority in seed data
- Ensure proper integer values for each priority level

---

### Step 5: Create Migration Script (3-4 min)
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

### Step 6: Update Python Client (3-4 min)
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

### Step 7: Update Unit Tests (4-5 min)
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

### Step 8: Update README (2-3 min)
**File**: `README.md` (modify)

**Changes needed**:
1. Update description to mention priority levels instead of urgency
2. Update API examples:
   - Old: `--urgent`, `--no-urgent`
   - New: `--priority high|medium|low`
3. Update curl examples with priority parameter
4. Add "Priority System" section explaining:
   - Three levels: Low, Medium, High
   - Database migration instructions
5. Update project structure to list new files
6. Update test count from 7 to 8

**What the AI tool should do**:
- Find and replace all references to IsUrgent/urgent with Priority
- Ensure examples are clear and up-to-date
- Add migration guide section

---

## Verification Steps (Before & After Demo)

### Before presenting:
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

### During demo (optional quick check):
```bash
# Verify it compiles
dotnet build

# Verify tests pass
dotnet test --verbosity quiet
```

---

## Demo Tips for Smooth Execution

1. **Pre-demo setup**:
   - Start from clean main branch
   - Have the requirements visible (this file)
   - Open the project in your chosen AI IDE

2. **Per-tool workflow (5-8 min each)**:
   - Read the step description
   - Explain what needs to change
   - Let the AI tool generate/modify the code
   - Review for correctness
   - Run `dotnet build` and `dotnet test` to verify

3. **Expected outputs**:
   - Each step should compile without errors
   - Final result: All 8 tests passing
   - Release build succeeds

4. **If something breaks**:
   - `git checkout -- .` to reset
   - Review the error with the AI tool
   - Fix and retry
   - This actually demonstrates the debugging workflow!

---

## Key Success Criteria

✅ All 8 unit tests pass
✅ Release build succeeds  
✅ No compilation errors
✅ API correctly filters by priority
✅ Client tool shows priority with new flags
✅ Migration script handles database conversion
✅ README is updated with new examples
