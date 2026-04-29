import httpx
from rich.console import Console
from .config import load_credentials, save_credentials, clear_credentials, BASE_URL

console = Console()


def get_headers():
    creds = load_credentials()
    if creds:
        return {
        "Authorization": f"Bearer {creds['access_token']}",
        "X-API-Version": "1"
        }
    
    return None


def refresh_tokens():
    creds = load_credentials()
    
    if not creds:
        return False
    
    res  = httpx.post(
        f"{BASE_URL}/auth/refresh",
        json={"refresh_token": creds["refresh_token"]}
    )
    
    if res.status_code == 200:
        data = res.json()
        
        creds["access_token"] = data["access_token"]
        creds["refresh_token"] = data["refresh_token"]
        save_credentials(creds)
        return True

    clear_credentials()
    return False


def request(method, path, **kwargs):
    headers = get_headers()
    if not headers:
        console.print("[red]Not logged in. Run: insighta login[/red]")
        return None
    
    extra_headers = kwargs.pop("headers", {})
    headers.update(extra_headers)

    url = f"{BASE_URL}{path}"
    res = httpx.request(method, url, headers=headers, **kwargs)

    if res.status_code == 401:
        console.print("[yellow]Token expired. Refreshing...[/yellow]")
        if refresh_tokens():
            headers = get_headers()
            headers.update(extra_headers)
            res = httpx.request(method, url, headers=headers, **kwargs)
        else:
            console.print("[red]Session expired. Please run: insighta login[/red]")
            return None

    return res





