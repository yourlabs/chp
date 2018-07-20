import ast
from chp import bundle
import click
import os


IMPORT_SAFE=(
    'math',
    'random',
)


@click.command()
@click.option('--entry-point', prompt='Entry point python script path',
              help='The python script to bundle for conversion to js')
def hello(entry_point):
    """Bundle a python script with dependencies into a single file."""
    result = bundle.generate(entry_point)

    click.echo('result:')
    click.echo(result)

main = hello
if __name__ == '__main__':
    hello()
