import click
from .import auth
from .import profiles as prof


@click.group()
def cli():
    """Insighta Labs+ CLI"""
    ...



@cli.command()
def login():
    """Login with GitHub"""
    auth.login()


@cli.command()
def logout():
    """Logout and clear stored credentials"""
    auth.logout()


@cli.command()
def whoami():
    """Show currently logged in user"""
    auth.whoami()



@cli.group(name="profiles")
def profiles_group():
    """Manage profiles"""
    pass


@profiles_group.command(name="list")
@click.option("--gender", default=None, help="Filter by gender")
@click.option("--country", default=None, help="Filter by country code e.g. NG")
@click.option("--age-group", default=None, help="child, teenager, adult, senior")
@click.option("--min-age", default=None, type=int, help="Minimum age")
@click.option("--max-age", default=None, type=int, help="Maximum age")
@click.option("--sort-by", default=None, help="Field to sort by e.g. age")
@click.option("--order", default="asc", help="asc or desc")
@click.option("--page", default=1, type=int, help="Page number")
@click.option("--limit", default=10, type=int, help="Results per page")
def list_profiles(gender, country, age_group, min_age, max_age,
                  sort_by, order, page, limit):
    """List profiles with optional filters"""
    prof.list_profiles(gender, country, age_group, min_age,
                       max_age, sort_by, order, page, limit)


@profiles_group.command(name="get")
@click.argument("id")
def get_profile(id):
    """Get a single profile by ID"""
    prof.get_profile(id)


@profiles_group.command(name="search")
@click.argument("query")
def search(query):
    """Search profiles using natural language"""
    prof.search_profiles(query)


@profiles_group.command(name="create")
@click.option("--name", required=True, help="Name to create profile for")
def create(name):
    """Create a new profile (admin only)"""
    prof.create_profile(name)


@profiles_group.command(name="export")
@click.option("--format", "fmt", default="csv", help="Export format (csv)")
@click.option("--gender", default=None, help="Filter by gender")
@click.option("--country", default=None, help="Filter by country code")
def export(fmt, gender, country):
    """Export profiles to CSV"""
    prof.export_profiles(fmt, gender, country)