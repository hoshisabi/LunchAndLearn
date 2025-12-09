# Lunch & Learn Demo Guide

## Overview

This guide maps each AI tool to a specific task for the Priority Feature Upgrade demo.

**Total Demo Time**: 50 minutes

- **Implementation**: ~32-34 minutes (4 tasks)
- **Q&A**: ~16-18 minutes

---

## Demo Setup (Before You Start)

### Prerequisites

1. Create a fresh demo branch from `main`
   ```pwsh
   git checkout main
   git pull origin main
   git checkout -b demo/priority-feature
   ```
   
2. Have these tools ready:
    - **Cursor IDE** - for Task 1
    - **VS Code with GitHub Copilot** - for Task 2
    - **JetBrains Rider with Junie** - for Task 3
    - **Copilot CLI or Gemini** - for Task 4

3. Have this repository open in each tool

4. Keep `UPGRADE_TASK.md` visible for reference

---

## Planning with AI: A Practical Example

An important part of the usage of AI tools is to generate your list of requirements before you begin. Many of the tools
are more than happy start improvising details that you don't specify, so it's often helpful to come up with a checklist
like this file to help keep track of the task. In addition, the tools can help you brainstorm this very checklist. For
this, I took a very rough list of steps:

> - Our users have expressed that they need to have finer grained control over the priority of tasks, instead of just
    urgent as a boolean, we should have a priority field with three values right now. HIGH, MEDIUM, and LOW, with
    HIGH > MEDIUM > LOW.
> - We should have a small python migration script that can update an existing DB to use these new values.
> - We should update our seed script to use this new value.
> - We should update our server to take priority as a parameter.
> - We should update our client.py to use this as a parameter.

I then had Copilot help me model it into the UPGRADE_TASK.md file to help plan out the work that the tools will be
doing.
One of the most valuable uses of AI code generation tools is **planning and specification before coding**. Here's how
we used Copilot/Gemini in a browser to plan this demo:

> **💡 Presenter Note:** Mention this planning phase during intro/Q&A (~1-2 min). Don't interrupt the flow of tasks, but
> highlight how the rough requirements became the structured UPGRADE_TASK.md. This reinforces the meta-lesson: *Use AI
not just to code, but to organize and plan.*

---

## Task Assignments

### Task 1: Data Model & API Endpoint (10 min) - **CURSOR**

**What Cursor will demonstrate:**

- Creating new files from scratch
- Understanding existing codebase structure
- Making changes across multiple related files
- Refactoring with full codebase context

**Steps** (from UPGRADE_TASK.md, Task 1):

1. Create `Priority.cs` enum
2. Update `Issue.cs` model
3. Update `IssueDbContext.cs` configuration
4. Update `Program.cs` API endpoint

**Your role:**

- Explain the task: "We need to replace the boolean urgent flag with a three-level priority system"
- Let Cursor work through all subtasks
- After completion: Run `dotnet build` to verify compilation
- Show the changes across files as evidence of codebase understanding

**Key points to highlight during demo:**
- Emphasize Cursor's codebase understanding: it automatically connected related files (Issue.cs → IssueDbContext.cs → Program.cs) without explicit instructions
- Show the multi-file diff view to demonstrate coordinated changes across the entire codebase
- Mention Plan mode as an example of planning before execution (aligns with the demo's planning philosophy)

**Important hints for Cursor execution:**
- **Priority enum**: Use uppercase `LOW`, `MEDIUM`, `HIGH` (no explicit numeric values - C# will auto-assign 0, 1, 2)
- **Database storage**: Use `.HasConversion<string>()` in `IssueDbContext.cs` to store enum as string in SQLite (for Python script compatibility)
- **Query parsing**: Use `Enum.TryParse<Priority>(value, ignoreCase: true, out var priority)` for case-insensitive input (accepts 'high', 'HIGH', 'High', etc.)
- **JSON serialization**: Verify enum serializes as string in API responses (may need `JsonStringEnumConverter` if enum serializes as number instead of string)
- **File location**: Create `Priority.cs` in `LunchAndLearn/` directory (same location as `Issue.cs`)

**Expected time breakdown:**

- Subtask 1a (Priority.cs): 2-3 min
- Subtask 1b (Issue.cs + IssueDbContext.cs): 3-4 min
- Subtask 1c (Program.cs): 2-3 min
- Build verification: 2 min

---

### Task 2: Python Scripts & Migration (8-9 min) - **COPILOT CLI**

**What Copilot CLI will demonstrate:**

- Iterative refinement through conversation (not just single-shot generation)
- How AI assistance works outside the IDE (accessibility for CLI-first developers)
- Data file transformation workflows (CSV manipulation is practical, real-world work)
- Complex script development with progressive improvement
- Multi-step problem solving with back-and-forth discussion

**Steps** (iterative conversation approach):

1. Transform the CSV data file (IsUrgent → Priority columns)
2. Generate migration script that reads from updated CSV
3. Refine with backup/rollback feature through follow-up requests
4. Update seed script and client to work with new data structure

**Your role:**

- Explain: "Not everyone works in an IDE. Copilot CLI brings AI assistance to the terminal—and the workflow is just as powerful. Watch how we refine the migration script through conversation."
- **Key point**: "Notice we're also working with CSV files—data transformation is just as important as code generation. Many of you work with CSVs daily."
- Show the conversational back-and-forth: each request builds on the previous one
- Highlight: "We're not asking for one perfect script—we're iteratively improving it"
- After completion: Review the final migration script's robustness and backup/rollback logic
- Emphasize: "This is how CLI-first developers can use AI effectively, whether for code or data"

**Key conversation sequence:**
```bash
# First, transform the CSV file
gh copilot suggest "Update the issues.csv file to replace the IsUrgent boolean column with a Priority column, mapping 0->LOW/MEDIUM and 1->MEDIUM/HIGH"

# Then generate migration script that reads CSV
gh copilot suggest "Create a Python migration script that reads the updated issues.csv file and inserts the data into the database with Priority values"

# Add backup functionality
gh copilot suggest "Add backup functionality with timestamp to the migration script, backing up both the CSV and database"

# Add rollback support
gh copilot suggest "Add a --rollback flag to restore from backups and improve error messages"
```

**Expected time breakdown:**

- CSV transformation + migration generation: 3-4 min
- Backup/rollback refinement: 2-3 min
- Review and seed script updates: 2-3 min

**No build verification needed** (Python is interpreted)

---

### Task 3: Unit Tests (8-9 min) - **JUNIE (JetBrains Rider)**

**What Junie will demonstrate:**

- IDE integration and refactoring capabilities
- Test-driven development practices
- Comprehensive test coverage
- Different IDE experience than VS Code

**Steps** (from UPGRADE_TASK.md, Task 3):

1. Update `IssueTests.cs` - Create tests for all three priority levels
2. Update `IssueDbContextTests.cs` - Refactor filtering tests for priority

**Your role:**

- Explain: "Let's ensure our changes are properly tested with comprehensive test coverage"
- Show Junie's test navigation and refactoring UI (different from Copilot in VS Code)
- After completion: Run `dotnet test` to show all 8 tests passing (up from 7)
- Highlight the test coverage verification

**Expected time breakdown:**

- IssueTests.cs refactoring: 3-4 min
- IssueDbContextTests.cs refactoring: 3-4 min
- Test execution & verification: 1-2 min

---

### Task 4: Documentation (5-6 min) - **COPILOT (VS Code)**

**What Copilot will demonstrate:**

- Context-aware documentation updates (AI understands code changes from Tasks 1-3)
- Keeping code and documentation in sync automatically
- Inline editing with immediate codebase context
- How AI catches inconsistencies without being explicitly told

**Steps** (from UPGRADE_TASK.md, Task 4):

1. Open README.md alongside recent code changes
2. Use Copilot to update testing section
     - Fix test count reference (7 → 8)
     - Update example API calls (`?priority=` instead of `?urgent=`)
     - Update Python client examples

**Your role:**

- Explain: "Finally, documentation. The interesting thing about using Copilot here is that it has immediate context about the code changes we just made. It's not guessing—it understands what changed."
- Show how Copilot infers the test count change from the actual code
- Highlight: "Watch how it catches inconsistencies without us explicitly pointing them out"
- Review the updated README for clarity and correctness
- Emphasize: "This is about keeping code and documentation in sync, which is a real problem teams face"

**Expected time breakdown:**

- README updates with context-aware refinement: 5-6 min

**No verification needed** (documentation review only)

---

## Talking Points for Each Tool

### Cursor

> "Cursor excels at understanding your entire codebase. Notice how it immediately understood the relationships between
> the Issue model, the database context, and the API endpoint. It modified all three files in a coordinated way, showing
> deep codebase comprehension."

### Copilot (VS Code)

> "GitHub Copilot shows its versatility here, seamlessly switching between C# and Python. The migration script is
> particularly complex with error handling and backup logic—notice how Copilot created production-ready code with proper
> safety features."

### Junie (JetBrains Rider)

> "JetBrains AI Assistant is deeply integrated with Rider's refactoring capabilities. The IDE-integrated experience
> offers real-time suggestions and coordinated refactoring across test files. Also notice how running tests directly
> from the IDE gives immediate feedback."

### Copilot CLI / Gemini

> "AI isn't just for code. Here we used it for technical documentation to ensure consistency and clarity. This
> demonstrates how modern AI can improve the entire development experience, not just code generation."

---

## Timing & Pacing Tips

| Time      | Task                 | Duration |
|-----------|----------------------|----------|
| 0:00-0:10 | Task 1 (Cursor)      | 10 min   |
| 0:10-0:19 | Task 2 (Copilot CLI) | 8-9 min |
| 0:19-0:28 | Task 3 (Junie)       | 8-9 min  |
| 0:28-0:34 | Task 4 (Copilot) | 5-6 min |
| 0:34-0:50 | Q&A                  | 16 min   |

---

## What If Something Goes Wrong?

### If a tool makes a mistake:

1. **Acknowledge it**: "Interesting—the tool suggested this, but we need..."
2. **Show the debugging process**: Use the AI tool to explain and fix the error
3. **Turn it into a teaching moment**: "This shows why we have testing and code review!"

### If you're running behind:

1. Skip detailed explanations in Tasks 2-4
2. Focus on showing the *result* rather than full generation
3. Use Task 4 (Docs) as a "buffer task"—it's the easiest to compress

### If you're ahead of schedule:

1. Spend extra time on Q&A
2. Show additional features of each tool
3. Do a deeper dive into the test coverage

---

## After the Demo

1. **Show the final result**: Run full test suite and release build
2. **Discuss the journey**: Point back to the 4 different tools and what each brought
3. **Key takeaway**: "These tools freed you to focus on architecture and logic, while AI handled the implementation
   details"

---

## Demo Success Criteria

✅ All 4 tasks complete
✅ All 8 tests passing
✅ Release build succeeds
✅ Each tool clearly demonstrated its unique strengths
✅ Code is clean and production-ready
✅ Audience understands the value of AI assistance in development
