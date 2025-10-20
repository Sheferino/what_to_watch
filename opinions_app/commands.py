import click
import csv

from . import app, db
from .models import Opinion


@app.cli.command('load_csv')
def load_csv():
    """Функция загрузки мнений из csv в БД
    """
    counter = 0
    with open('opinions.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            opinion = Opinion(**row)
            db.session.add(opinion)
            counter += 1
        db.session.commit()
    click.echo(f'Загружено {counter} записей!')
