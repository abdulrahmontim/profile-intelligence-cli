# Insighta CLI — profile-intelligence-cli

A command line tool for interacting with the Insighta Labs+ Profile Intelligence API.
Supports authentication, profile management, search, and CSV export from your terminal.

---

## Requirements

- Python 3.12+
- A GitHub account
- Access to the Insighta Labs+ backend

---

## Installation

```bash
git clone https://github.com/abdulrahmontim/profile-intelligence-cli
cd profile-intelligence-cli
pip install -e .
```

After installation, `insighta` is available globally from any directory.

Verify:
```bash
insighta --help
```

---

## Configuration

Create a `.env` file in the project root:

```bash
GITHUB_CLIENT_ID=your_github_cli_oauth_app_client_id
INSIGHTA_API_URL=https://profile-intelligence-api-production.up.railway.app
```

Tokens are stored automatically at `~/.insighta/credentials.json` after login.

---

## Authentication

### Login
```bash
insighta login
```
Opens GitHub OAuth in your browser. After authorizing, tokens are saved locally.

### Logout
```bash
insighta logout
```
Invalidates your session on the backend and clears local tokens.

### Whoami
```bash
insighta whoami
```
Shows your currently logged in GitHub username and role.

---

## Profile Commands

### List Profiles

```bash
# All profiles (default: page 1, limit 10)
insighta profiles list

# Filter by gender
insighta profiles list --gender male
insighta profiles list --gender female

# Filter by country (use ISO country code)
insighta profiles list --country NG
insighta profiles list --country US

# Filter by age group
insighta profiles list --age-group adult
insighta profiles list --age-group child
insighta profiles list --age-group teenager
insighta profiles list --age-group senior

# Filter by age range
insighta profiles list --min-age 20 --max-age 40

# Sorting
insighta profiles list --sort-by age --order asc
insighta profiles list --sort-by age --order desc

# Pagination
insighta profiles list --page 2 --limit 20

# Combined filters
insighta profiles list --gender male --country NG --age-group adult
insighta profiles list --gender female --sort-by age --order desc --page 1 --limit 5
```

### Get Single Profile

```bash
insighta profiles get <id>
```

Example:
```bash
insighta profiles get 019dd6d0-4dce-7647-ad8b-336542a02024
```

### Search Profiles (Natural Language)

```bash
insighta profiles search "<query>"
```

Examples:
```bash
insighta profiles search "young males from nigeria"
insighta profiles search "females from the US"
insighta profiles search "senior women"
insighta profiles search "adult males"
insighta profiles search "children from canada"
```

### Create Profile (Admin only)

```bash
insighta profiles create --name "<name>"
```

Example:
```bash
insighta profiles create --name "Harriet Tubman"
```

Fetches gender, age, and nationality data automatically from external APIs.

### Export Profiles to CSV

```bash
# Export all profiles
insighta profiles export --format csv

# Export with filters
insighta profiles export --format csv --gender male
insighta profiles export --format csv --country NG
insighta profiles export --format csv --gender female --country US
```

CSV file is saved to your current working directory with a timestamp:
```
profiles_20240101_120000.csv
```

---

## Token Handling

| Behaviour | Details |
|-----------|---------|
| Token storage | `~/.insighta/credentials.json` |
| Access token expiry | 3 minutes |
| Refresh token expiry | 5 minutes |
| Auto-refresh | Yes — on 401 response, refresh is attempted automatically |
| Re-login prompt | If refresh also fails, user is told to run `insighta login` |

Every request automatically sends:
```
Authorization: Bearer <access_token>
X-API-Version: 1
```

---

## Role Permissions

| Command | Analyst | Admin |
|---------|---------|-------|
| `profiles list` | ✅ | ✅ |
| `profiles get` | ✅ | ✅ |
| `profiles search` | ✅ | ✅ |
| `profiles export` | ✅ | ✅ |
| `profiles create` | ❌ | ✅ |

---

## CI/CD

GitHub Actions runs on every PR to `main`:
- Linting with `flake8`
- Verifies CLI installs and loads correctly

See `.github/workflows/ci.yml` for configuration.

---

## Project Structure

```
profile-intelligence-cli/
├── insighta/
│   ├── __init__.py
│   ├── main.py        ← CLI entry point, all commands defined here
│   ├── auth.py        ← login, logout, whoami
│   ├── profiles.py    ← profile commands and table display
│   ├── api.py         ← authenticated HTTP client with auto-refresh
│   └── config.py      ← token storage and base URL config
├── setup.py           ← makes CLI installable via pip
├── requirements.txt
└── .github/
    └── workflows/
        └── ci.yml
```

---

## Live Backend

```
https://profile-intelligence-api-production.up.railway.app
```
