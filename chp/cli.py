import ast
from chp import bundle
import click
import os


@click.group()
def cli():
    pass


@click.command()
@click.option('--entry-point', prompt='Entry point python script path',
              help='The python script to bundle for conversion to js')
def dependencies(entry_point):
    """List dependencies of a single file."""
    result = bundle.dependencies(os.path.abspath(entry_point))
    click.echo('\n'.join(result))


@click.command()
@click.option('--entry-point', prompt='Entry point python script path',
              help='The python script to bundle for conversion to js')
def generate(entry_point):
    """Bundle a python script with dependencies into a single file."""
    result = bundle.generate(entry_point)
    click.echo(result)

cli.add_command(dependencies)
cli.add_command(generate)

main = cli
if __name__ == '__main__':
    main()
