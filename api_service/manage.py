# encoding: utf-8

import click
from flask.cli import with_appcontext


@click.group()
def cli():
    """Main entry point"""
    pass


@cli.command("init")
@with_appcontext
def init():
    """Create a new admin user
    Uage: write in the command line python manage.py init"""
    from api_service.extensions import db
    from api_service.models import User,StockCall
    from api_service.wsgi import create_app

    app = create_app()

    click.echo("create admin user")
    with app.app_context():
        db.create_all()
        user = User(username="admin", email="admin@mail.com", password="admin", active=True, role='ADMIN')
        db.session.add(user)
        user = User(username="johndoe", email="johndoe@mail.com", password="john", active=True, role='USER')
        db.session.add(user)
        db.session.commit()
    click.echo("created users.")


if __name__ == "__main__":
    cli()
