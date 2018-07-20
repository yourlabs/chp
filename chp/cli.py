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
    for result in bundle.Path(entry_point).dependencies:
        click.echo(f'{result}: {result.path}')


@click.command()
@click.option('--entry-point', prompt='Entry point python script path',
              help='The python script to bundle for conversion to js')
def globalize_imports(entry_point):
    """List dependencies of a single file."""
    click.echo(bundle.GlobalizeImports.from_path(entry_point).to_source())


@click.command()
@click.option('--entry-point', prompt='Entry point python script path',
              help='The python script to bundle for conversion to js')
def generate(entry_point):
    """Bundle a python script with dependencies into a single file."""
    source = [bundle.GlobalizeImports.from_path(entry_point).to_source()]
    for result in bundle.Path(entry_point).dependencies:
        source.append(bundle.GlobalizeImports.from_path(result.path).to_source())
    click.echo('\n'.join(reversed(source)))

cli.add_command(dependencies)
cli.add_command(generate)
cli.add_command(globalize_imports)

main = cli
if __name__ == '__main__':
    main()
