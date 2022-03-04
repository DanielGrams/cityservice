import click
from flask.cli import AppGroup

from project import app

scrape_cli = AppGroup("scrape")


@scrape_cli.command("news")
def scrape_news():
    from project.cli.scrape_news import scrape

    click.echo("Scraping news..")
    scrape()
    click.echo("Done.")


@scrape_cli.command("weather_warnings")
def scrape_weather_warnings():
    from project.cli.scrape_weather_warnings import scrape

    click.echo("Scraping weather warnings..")
    scrape()
    click.echo("Done.")


@scrape_cli.command("recycling")
def scrape_recycling():
    from project.cli.scrape_recycling import scrape

    click.echo("Scraping recycling..")
    scrape()
    click.echo("Done.")


app.cli.add_command(scrape_cli)
