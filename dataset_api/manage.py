import click
from flask.cli import with_appcontext

VGSALES_CSV = r"data/vgsales.csv"

@click.command("init")
@with_appcontext
def init():
    """Create a new admin user"""
    from dataset_api.extensions import db
    from dataset_api.models import User

    click.echo("create user")
    user = User(username="admin", email="admin@mail.com", password="admin", active=True)
    db.session.add(user)
    db.session.commit()
    click.echo("created user admin")

@click.command("load_vg")
@with_appcontext
def load_vgsales_data():
    """Create a new admin user"""
    from dataset_api.extensions import db

    click.echo("loading data into db...")
    import pandas as pd
    data = pd.read_csv(VGSALES_CSV)
    data = data[data['Year'].notnull()]
    data = data['Publisher'].fillna("Not Specified")
    data.rename({'Rank': 'rank', 'Name': 'name', 'Platform': 'platform', 'Year': 'year', 'Genre': 'genre',
                 'Publisher': 'publisher', 'NA_Sales': 'na_sales', 'EU_Sales': 'eu_sales', 'JP_Sales': 'jp_sales',
                 'Other_Sales': 'other_sales', 'Global_Sales': 'global_sales'}, inplace=True, axis=1)
    try:
        db.engine.echo = False
        with db.engine.begin() as connection:
            data.to_sql('vg_sales', con=connection, method='multi', if_exists='append', index=False, chunksize=1000)
        click.echo("data loaded Successfully")
    except Exception as ex:
        click.echo("failed to load data.")
        print(ex)

