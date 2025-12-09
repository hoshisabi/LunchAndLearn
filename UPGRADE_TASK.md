# Priority Feature Upgrade Tasks

## Overview
Enhance the issue tracking system to support a three-level priority system (HIGH, MEDIUM, LOW) instead of a simple boolean `IsUrgent` flag.

---

## Task 1: Data Model & API Endpoint (10 minutes)

### Subtask 1a: Create Priority Enum (2-3 min)
**File**: `LunchAndLearn/Priority.cs` (NEW)

Create a priority enum with three values using uppercase naming:
```csharp
namespace LunchAndLearn;

public enum Priority
{
    LOW,
    MEDIUM,
    HIGH
}
```

**Important notes**:
- Use uppercase enum values: `LOW`, `MEDIUM`, `HIGH` (not `Low`, `Medium`, `High`)
- Do not specify explicit numeric values - let C# auto-assign 0, 1, 2
- File should be created in the `LunchAndLearn/` directory (same location as `Issue.cs`)

**What the AI tool should do**:
- Create the new file in `LunchAndLearn/` directory
- Define the enum with uppercase values (LOW, MEDIUM, HIGH)
- Add to the `LunchAndLearn` namespace

---

### Subtask 1b: Update C# Models (3-4 min)
**Files**: 
- `LunchAndLearn/Issue.cs` (modify)
- `LunchAndLearn/IssueDbContext.cs` (modify)

**Changes needed**:
1. Update `Issue` record to use `Priority Priority` instead of `bool IsUrgent`
2. Update `IssueDbContext.OnModelCreating()` to:
   - Configure Priority to be stored as **string** in database using `.HasConversion<string>()`
   - This allows Python migration scripts to work with string values ('HIGH', 'MEDIUM', 'LOW')
   - Optional: Set default value to `Priority.Medium` using `.HasDefaultValue(Priority.Medium)` (not required for demo)

**Important notes**:
- Store enum as **string** (not integer) for Python compatibility
- Use `.HasConversion<string>()` method in Entity Framework configuration
- The string storage format makes it easier for Python scripts to read/write priority values

**What the AI tool should do**:
- Replace the `IsUrgent` property with `Priority` property in `Issue.cs`
- Update `IssueDbContext.OnModelCreating()` to configure Priority with string conversion
- Ensure Entity Framework properly maps the enum to a string column in SQLite

---

### Subtask 1c: Update API Endpoint (2-3 min)
**File**: `LunchAndLearn/Program.cs` (modify)

**Changes needed**:
- Update `/issues` endpoint to filter by `?priority=low|medium|high` instead of `?urgent=true|false`
- Use `Enum.TryParse<Priority>(value, ignoreCase: true, out var priority)` for parsing the query parameter
- Query parameter should accept lowercase, uppercase, or mixed case (e.g., 'high', 'HIGH', 'High' all work)

**Important notes**:
- **Must use `ignoreCase: true`** in `Enum.TryParse` to handle case-insensitive input
- The existing `JsonNamingPolicy.CamelCase` configuration should serialize the enum as a string
- If the enum serializes as a number instead of string in JSON responses, add `JsonStringEnumConverter` to serialization options:
  ```csharp
  options.SerializerOptions.Converters.Add(new JsonStringEnumConverter(JsonNamingPolicy.CamelCase));
  ```
- Verify that API responses show priority as string values (e.g., "high", "medium", "low") not numbers

**What the AI tool should do**:
- Replace the urgent query parameter logic with priority filtering
- Use `Enum.TryParse<Priority>(value, ignoreCase: true, out var priority)` for case-insensitive parsing
- Ensure the query parameter accepts any case variation of priority values
- Verify JSON serialization outputs enum as string (may need to add JsonStringEnumConverter)

---

### Subtask 1d: Update HTTP Test File (1 min)
**File**: `LunchAndLearn/LunchAndLearn.http` (modify)

**Changes needed**:
- Update HTTP request examples to use `?priority=low|medium|high` instead of `?urgent=true|false`
- Add requests for each priority level (HIGH, MEDIUM, LOW)
- Keep the "Get all issues" request without a filter

**Example updated requests**:
```
### Get all issues
GET {{LunchAndLearn_HostAddress}}/issues
Accept: application/json

### Get only HIGH priority issues
GET {{LunchAndLearn_HostAddress}}/issues?priority=high
Accept: application/json

### Get only MEDIUM priority issues
GET {{LunchAndLearn_HostAddress}}/issues?priority=medium
Accept: application/json

### Get only LOW priority issues
GET {{LunchAndLearn_HostAddress}}/issues?priority=low
Accept: application/json
```

**What the AI tool should do**:
- Replace any `?urgent=` query parameters with `?priority=` parameters
- Add example requests for each priority level
- Ensure requests use lowercase priority values (matching API behavior)

---

## Task 2: Python Scripts & Migration (8-9 minutes)

### Subtask 2a: Transform CSV Data (2-3 min)
**File**: `LunchAndLearn/issues.csv` (modify)

**Changes needed**:
- Update the CSV file to replace `IsUrgent` column with `Priority` column
- Transform boolean values (0/1) to priority levels (LOW/MEDIUM/HIGH)
- Map: 0 (non-urgent) → LOW or MEDIUM, 1 (urgent) → HIGH or MEDIUM (mix it up)
- Updated CSV example:
  ```
  Code,ShortDescription,LongDescription,Priority
  ISSUE-001,Login button not working,Users report...,MEDIUM
  ISSUE-002,Performance lag,App slows down...,HIGH
  ISSUE-003,UI misalignment,Elements are...,LOW
  ISSUE-004,Security vulnerability,Potential SQL...,HIGH
  ISSUE-005,Feature request: Dark mode,Users want...,LOW
  ```

**What the AI tool should do**:
- Update the CSV headers (IsUrgent → Priority)
- Transform each row's boolean value to appropriate priority level
- Show practical data file manipulation (not just code changes)

**Presenter Note**: "Notice how the AI tool can handle data file transformations, not just code. This is practical for teams working with CSVs and data imports."

---

### Subtask 2b: Create Migration Script (3-4 min)
**File**: `LunchAndLearn/migrate_to_priority.py` (NEW)

**Must-haves**:
- Read from the updated CSV file to populate the database with Priority values
- Create automatic backup of the original CSV with timestamp
- Create automatic backup of the database before migration
- Provide rollback functionality with `--rollback` flag
- Report conversion statistics (how many of each priority level)
- Handle both fresh and partially-migrated databases

**What the AI tool should do**:
- Create comprehensive migration script that reads CSV and inserts into database
- Include backup/restore logic for both CSV and database
- Add command-line argument parsing
- Provide clear user feedback on migration progress

---

### Subtask 2c: Update Seed Script & Client (2-3 min)
**Files**: 
- `LunchAndLearn/seed_database.py` (modify)
- `LunchAndLearn/client.py` (modify)

**Changes needed**:

**seed_database.py**:
- Update to read Priority values from `issues.csv` instead of hardcoded data
- Use csv module to read and parse the file
- Insert CSV data directly into the database
- Provide feedback on how many issues were loaded from CSV

**client.py**:
- Replace `--urgent` / `--no-urgent` flags with `--priority low|medium|high`
- Update `get_issues()` method to accept priority parameter
- Update table format to show Priority instead of Urgent
- Add emoji indicators in simple format (🔴=High, 🟡=Medium, 🟢=Low)

**What the AI tool should do**:
- Update seed script to read CSV file using Python's csv module
- Update argument parsing in client.py
- Modify API call parameters
- Enhance output formatting with priority levels and emojis

---

## Task 3: Unit Tests (10-11 minutes)
**Files**:
- `LunchAndLearn.Tests/IssueTests.cs` (modify)
- `LunchAndLearn.Tests/IssueDbContextTests.cs` (modify)
- `LunchAndLearn/test_client.py` (NEW - Python unit tests)

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

3. `test_client.py` (Python unit tests):
   - Test `LunchAndLearnClient.get_issues()` with different urgent filters
   - Test `print_issues()` with different formats (table, json, simple)
   - Use mocking to avoid requiring a running server
   - Verify urgent filtering logic works correctly
   - Note that pytest is installed using uv in the "dev" environment

**Expected result**: 
- 8 passing C# tests (up from 7)
- 3-4 passing Python tests

**What the AI tool should do**:
- Refactor all C# test cases to use Priority enum
- Create Python unit tests using pytest with mocking
- Ensure comprehensive coverage of all three priority levels in C# tests
- Test Python client functionality without requiring running server
- Verify all tests pass with `dotnet test` and `pytest`

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
# Expected: 8/8 C# tests passed

pytest LunchAndLearn/test_client.py
# Expected: 7/7 Python tests passed
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
# Expected: 8/8 C# tests passed

pytest LunchAndLearn/test_client.py
# Expected: 7/7 Python tests passed

# Release build succeeds
dotnet build -c Release
```
# Optional: Test API endpoints using .http file
# Run the requests in LunchAndLearn.http to verify:
# - Get all issues returns all issues with priority values
# - Filtering by priority=high returns only HIGH priority issues
# - Filtering by priority=medium returns only MEDIUM priority issues
# - Filtering by priority=low returns only LOW priority issues

---

## Key Success Criteria

✅ All 8 C# unit tests pass (up from 7)
✅ All 7 Python unit tests pass
✅ Release build succeeds with no errors
✅ API correctly filters by `?priority=low|medium|high`
✅ Python client accepts `--priority` flag
✅ Migration script handles database conversion with backup
✅ Code compiles at each task completion
✅ HTTP test file (.http) updated with priority-based requests
