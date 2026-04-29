import os
import httpx
import secrets
import hashlib
import base64
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode, urlparse, parse_qs
from rich.console import Console
from dotenv import load_dotenv
from .config import save_credentials, clear_credentials, load_credentials, BASE_URL


load_dotenv()
console = Console()


def generate_code_verifier():
    return secrets.token_urlsafe(32)


def generate_code_challenge(verifier):
    digest = hashlib.sha256(verifier.encode()).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode()


def generate_state():
    return secrets.token_urlsafe(16)


def login():
    """
    Full PKCE OAuth flow:
    1. Generate PKCE values
    2. Open GitHub in browser
    3. Start local server to capture callback
    4. Send code + verifier to backend
    5. Save tokens
    """
    verifier = generate_code_verifier()
    challenge = generate_code_challenge(verifier)
    state = generate_state()

    result = {}

    class CallbackHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)

            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"<h2>Login successful. You can close this tab.</h2>"
            )

            returned_state = params.get("state", [None])[0]
            code = params.get("code", [None])[0]

            if returned_state != state:
                result["error"] = "State mismatch"
                return

            result["code"] = code

        def log_message(self, format, *args):
            pass

    server = HTTPServer(("localhost", 9876), CallbackHandler)
    redirect_uri = "http://localhost:9876/callback"

    params = urlencode({
        "client_id": os.environ.get("GITHUB_CLIENT_ID"),
        "redirect_uri": redirect_uri,
        "scope": "read:user user:email",
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    })

    auth_url = f"https://github.com/login/oauth/authorize?{params}"

    console.print("[cyan]Opening GitHub login in your browser...[/cyan]")
    webbrowser.open(auth_url)

    server.handle_request()
    server.server_close()

    if "error" in result:
        console.print(f"[red]Login failed: {result['error']}[/red]")
        return

    if not result.get("code"):
        console.print("[red]Login failed. No code received.[/red]")
        return

    # Send code + verifier to backend CLI endpoint
    with console.status("[cyan]Completing login...[/cyan]"):
        response = httpx.post(
            f"{BASE_URL}/auth/cli/callback",
            json={
                "code": result["code"],
                "code_verifier": verifier,
                "redirect_uri": redirect_uri,
            },
            timeout=15,
        )

        if response.status_code != 200:
            console.print(f"[red]Login failed: {response.status_code} — {response.text}[/red]")
            return

    data = response.json()

    save_credentials({
        "access_token": data["access_token"],
        "refresh_token": data["refresh_token"],
        "username": data.get("username", ""),
        "role": data.get("role", "analyst"),
    })

    console.print(f"[green]Logged in as @{data.get('username')}[/green]")


def logout():
    creds = load_credentials()
    if not creds:
        console.print("[yellow]Not logged in.[/yellow]")
        return

    httpx.post(
        f"{BASE_URL}/auth/logout",
        json={"refresh_token": creds["refresh_token"]},
    )

    clear_credentials()
    console.print("[green]Logged out successfully.[/green]")


def whoami():
    creds = load_credentials()
    if creds:
        console.print(f"[cyan]Logged in as @{creds['username']} ({creds.get('role', 'analyst')})[/cyan]")
    else:
        console.print("[red]Not logged in. Run: insighta login[/red]")
        return