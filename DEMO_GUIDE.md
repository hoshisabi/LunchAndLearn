# Lunch & Learn Demo Guide

## Overview
This guide maps each AI tool to a specific task for the Priority Feature Upgrade demo.

**Total Demo Time**: 50 minutes
- **Implementation**: ~32-34 minutes (4 tasks)
- **Q&A**: ~16-18 minutes

---

## Demo Setup (Before You Start)

### Prerequisites
1. Reset to clean `main` branch
   ```bash
   git checkout main
   git reset --hard origin/main
   git pull origin main
   ```

2. Have these tools ready:
   - **Cursor IDE** - for Task 1
   - **VS Code with GitHub Copilot** - for Task 2
   - **JetBrains Rider with Junie** - for Task 3
   - **Copilot CLI or Gemini** - for Task 4

3. Have this repository open in each tool

4. Keep `UPGRADE_TASK.md` visible for reference

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

**Expected time breakdown:**
- Subtask 1a (Priority.cs): 2-3 min
- Subtask 1b (Issue.cs + IssueDbContext.cs): 3-4 min
- Subtask 1c (Program.cs): 2-3 min
- Build verification: 2 min

---

### Task 2: Python Scripts & Migration (8-9 min) - **COPILOT (VS Code)**
**What Copilot will demonstrate:**
- Language switching (C# → Python)
- Creating complex scripts with error handling
- Database operations and refactoring
- Multi-file modifications across different language stacks

**Steps** (from UPGRADE_TASK.md, Task 2):
1. Update `seed_database.py`
2. Create new `migrate_to_priority.py` with backup/rollback
3. Update `client.py` with new priority filtering

**Your role:**
- Explain: "Now we need to update the Python side to support the new priority system"
- Highlight Copilot's ability to switch between C# and Python
- After completion: Review the migration script and its robustness
- No build verification needed (Python is interpreted)

**Expected time breakdown:**
- Subtask 2a (seed_database.py): 2-3 min
- Subtask 2b (migrate_to_priority.py): 3-4 min
- Subtask 2c (client.py): 2-3 min

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

### Task 4: Documentation (5-6 min) - **COPILOT CLI** (or Gemini)
**What Copilot CLI will demonstrate:**
- AI assistance for non-code tasks (documentation)
- Different interface/interaction model (CLI vs IDE)
- Communication and clarity in technical writing
- Real-world business use case (customer-facing docs)

**Steps** (from UPGRADE_TASK.md, Task 4):
1. Update README.md testing section
   - Fix test count reference (7 → 8)
   - Update example API calls (`?priority=` instead of `?urgent=`)
   - Update Python client examples

**Your role:**
- Explain: "Finally, let's ensure our documentation reflects the new feature"
- Show how AI can help with documentation accuracy, not just code
- Review the updated README for clarity and correctness
- No verification needed (documentation review only)

**Expected time breakdown:**
- README updates: 5-6 min

---

## Talking Points for Each Tool

### Cursor
> "Cursor excels at understanding your entire codebase. Notice how it immediately understood the relationships between the Issue model, the database context, and the API endpoint. It modified all three files in a coordinated way, showing deep codebase comprehension."

### Copilot (VS Code)
> "GitHub Copilot shows its versatility here, seamlessly switching between C# and Python. The migration script is particularly complex with error handling and backup logic—notice how Copilot created production-ready code with proper safety features."

### Junie (JetBrains Rider)
> "JetBrains AI Assistant is deeply integrated with Rider's refactoring capabilities. The IDE-integrated experience offers real-time suggestions and coordinated refactoring across test files. Also notice how running tests directly from the IDE gives immediate feedback."

### Copilot CLI / Gemini
> "AI isn't just for code. Here we used it for technical documentation to ensure consistency and clarity. This demonstrates how modern AI can improve the entire development experience, not just code generation."

---

## Timing & Pacing Tips

| Time | Task | Duration |
|------|------|----------|
| 0:00-0:10 | Task 1 (Cursor) | 10 min |
| 0:10-0:19 | Task 2 (Copilot) | 8-9 min |
| 0:19-0:28 | Task 3 (Junie) | 8-9 min |
| 0:28-0:34 | Task 4 (Copilot CLI) | 5-6 min |
| 0:34-0:50 | Q&A | 16 min |

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
3. **Key takeaway**: "These tools freed you to focus on architecture and logic, while AI handled the implementation details"

---

## Demo Success Criteria

✅ All 4 tasks complete
✅ All 8 tests passing
✅ Release build succeeds
✅ Each tool clearly demonstrated its unique strengths
✅ Code is clean and production-ready
✅ Audience understands the value of AI assistance in development
