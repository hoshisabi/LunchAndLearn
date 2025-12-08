# LunchAndLearn

## About This Project

This project is designed for an upcoming **Lunch & Learn session** focused on using **AI for code assistance**. The goal is to demonstrate how modern AI-powered development tools can help developers write, test, and maintain code more efficiently.

This is a simple web API application built with:
- **C# / .NET 9.0** - ASP.NET Core minimal API with Entity Framework Core
- **SQLite** - Lightweight database for storing issue data
- **Python** - Utility scripts for database seeding and API client testing

The application manages a simple issue tracking system with endpoints to query issues and filter by urgency. It serves as a practical example for exploring how different AI code assistants can help with various development tasks.

---

## Prerequisites

### Required Software

1. **.NET 9.0 SDK**
   - Download from: https://dotnet.microsoft.com/download/dotnet/9.0
   - Verify installation: `dotnet --version` (should show 9.0.x)

2. **Python 3.8+**
   - Download from: https://www.python.org/downloads/
   - Verify installation: `python --version`

3. **uv** (Python package manager)
   - Installation instructions below

4. **Git**
   - Download from: https://git-scm.com/download/win
   - Verify installation: `git --version`

### Optional but Recommended

- **Visual Studio Code** with C# extension (for C# development)
- **Visual Studio 2022** (alternative IDE for C# development)
- **Rider** or **PyCharm** (JetBrains IDEs with built-in AI assistance)

> **Note:** While these instructions are Windows-focused, this project will work on macOS and Linux as well. You may need to adjust paths and commands accordingly.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd LunchAndLearn
```

### 2. Install uv (Python Package Manager)

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Alternative (using pip):**
```bash
pip install uv
```

**Verify installation:**
```bash
uv --version
```

For more installation options, visit: https://github.com/astral-sh/uv

### 3. Set Up Python Environment

The project uses `uv` to manage Python dependencies. The first time you run a Python script, `uv` will automatically create a virtual environment and install dependencies.

To manually set up the environment:
```bash
cd LunchAndLearn
uv sync
```

This will:
- Create a virtual environment (`.venv`)
- Install all required Python packages (from `pyproject.toml`)

### 4. Set Up C# Project

**Using Visual Studio Code:**

1. Install the **C# Dev Kit** extension (or at minimum, the **C#** extension)
   - Open VS Code
   - Go to Extensions (Ctrl+Shift+X)
   - Search for "C# Dev Kit" and install
   - This includes the C# extension, IntelliCode, and other helpful tools

2. Restore NuGet packages:
   ```bash
   dotnet restore
   ```

3. Build the solution:
   ```bash
   dotnet build
   ```

**Using Visual Studio 2022:**

1. Open `LunchAndLearn.sln` in Visual Studio
2. Visual Studio will automatically restore NuGet packages
3. Build the solution (Ctrl+Shift+B)

### 5. Seed the Database

Before running the application, seed the database with sample data:

```bash
cd LunchAndLearn
uv run python seed_database.py
```

This will create `issues.db` (if it doesn't exist) and populate it with 5 sample issues.

---

## Running the Application

### Start the API Server

**From the `LunchAndLearn` directory:**

```bash
dotnet run
```

The API will start on `http://localhost:5099` (HTTP) or `https://localhost:7181` (HTTPS).

### Test the API

**Using the Python client:**

```bash
# List all issues (table format)
uv run python client.py

# Show only urgent issues
uv run python client.py --urgent

# Show only non-urgent issues
uv run python client.py --no-urgent

# Output as JSON
uv run python client.py --format json

# Simple one-line format
uv run python client.py --format simple

# Use a different URL
uv run python client.py --url http://localhost:7181
```

**Using curl or a browser:**

```bash
# Get all issues
curl http://localhost:5099/issues

# Get only urgent issues
curl "http://localhost:5099/issues?urgent=true"

# Get only non-urgent issues
curl "http://localhost:5099/issues?urgent=false"
```

Or simply open `http://localhost:5099/issues` in your browser.

---

## Running Tests

### Unit Tests

Run all unit tests:

```bash
dotnet test
```

Or run tests for a specific project:

```bash
dotnet test LunchAndLearn.Tests/LunchAndLearn.Tests.csproj
```

Expected output:
- **7 total tests** should pass
- Tests cover:
  - Issue model creation and equality
  - Database operations (add, query, filtering)
  - Filtering by urgency
  - Primary key constraints

### Manual Testing

To verify the application is working end-to-end:

1. **Build the solution (Debug):**
   ```bash
   dotnet build
   ```
   ✅ Should complete successfully with no compilation errors

2. **Build the solution (Release):**
   ```bash
   dotnet build -c Release
   ```
   ✅ Should complete successfully, confirming production-ready code

3. **Run the API server:**
   ```bash
   cd LunchAndLearn
   dotnet run
   ```
   ✅ Should output: `Now listening on: http://localhost:5099`

4. **In another terminal, seed the database:**
   ```bash
   cd LunchAndLearn
   uv run python seed_database.py
   ```
   ✅ Should confirm: `Successfully seeded the database`

5. **Test the API endpoints:**
   ```bash
   # Get all issues
   uv run python client.py
   
   # Filter for urgent issues only
   uv run python client.py --urgent
   
   # Filter for non-urgent issues only
   uv run python client.py --no-urgent
   ```
   ✅ Should return a formatted table of issues with all fields populated

---

## Project Structure

```
LunchAndLearn/
├── LunchAndLearn/              # Main C# API project
│   ├── Program.cs              # API entry point and endpoints
│   ├── Issue.cs                # Issue entity model
│   ├── IssueDbContext.cs       # Entity Framework DbContext
│   ├── client.py               # Python API client
│   ├── seed_database.py        # Database seeding script
│   └── issues.db               # SQLite database (created on first run)
│
├── LunchAndLearn.Tests/        # Unit tests
│   ├── IssueTests.cs           # Issue model tests
│   └── IssueDbContextTests.cs  # Database context tests
│
└── README.md                   # This file
```

---

## AI Code Generation Tools

This project is designed to demonstrate various AI-powered code assistance tools. Here are the tools you might encounter during the Lunch & Learn:

### Cursor
- **What it is:** AI-powered code editor built on VS Code
- **Where to get it:** https://cursor.sh/
- **Platforms:** Windows, macOS, Linux
- **Features:** AI chat, code completion, inline editing, codebase understanding
- **Note:** This is the tool being used to help create and maintain this project

### GitHub Copilot
- **What it is:** AI pair programmer that suggests code as you type
- **Where to get it:**
  - **VS Code:** Install "GitHub Copilot" extension from the marketplace
  - **Visual Studio:** Available in Visual Studio 2022 (requires subscription)
- **Platforms:** Windows, macOS, Linux
- **Features:** Code completion, chat interface, inline suggestions

### JetBrains AI Assistant (Junie)
- **What it is:** AI assistant integrated into JetBrains IDEs
- **Where to get it:** Built into Rider, PyCharm, IntelliJ IDEA, and other JetBrains IDEs
- **Platforms:** Windows, macOS, Linux
- **Features:** Code completion, refactoring suggestions, documentation generation
- **Note:** Requires a JetBrains subscription with AI features enabled

### Google Gemini CLI
- **What it is:** Command-line interface for Google's Gemini AI model
- **Where to get it:** https://github.com/google/generative-ai-cli
- **Platforms:** Windows, macOS, Linux
- **Features:** Code generation, analysis, and assistance via command line
- **Installation:** `npm install -g @google/generative-ai-cli` or via other package managers

### Other Tools
- **ChatGPT** (via web interface or API)
- **Claude** (Anthropic's AI assistant)
- **Codeium** (free alternative to Copilot)
- **Tabnine** (AI code completion)

---

## Troubleshooting

### Python/uv Issues

**Problem:** `uv` command not found
- **Solution:** Make sure `uv` is installed and in your PATH. Restart your terminal after installation.

**Problem:** Virtual environment not found
- **Solution:** Run `uv sync` to create the virtual environment and install dependencies.

### C#/.NET Issues

**Problem:** `dotnet` command not found
- **Solution:** Install .NET 9.0 SDK and restart your terminal. Verify with `dotnet --version`.

**Problem:** NuGet package restore fails
- **Solution:** Check your internet connection. Some corporate networks may block NuGet feeds. You may need to configure proxy settings.

**Problem:** Database file not found
- **Solution:** Run the application once (`dotnet run`) to create the database, then run `uv run python seed_database.py` to populate it.

### VS Code C# Issues

**Problem:** IntelliSense not working
- **Solution:** 
  1. Install the C# Dev Kit extension
  2. Run `dotnet restore` in the project directory
  3. Reload VS Code window (Ctrl+Shift+P → "Reload Window")

**Problem:** Build errors in VS Code
- **Solution:** Open the terminal in VS Code and run `dotnet build` to see detailed error messages.

---

## Contributing

This is a demonstration project for a Lunch & Learn session. Feel free to experiment with it and try different AI tools to modify or extend the codebase!

---

## License

This project is provided as-is for educational purposes.
