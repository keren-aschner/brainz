import pathlib

import click


@click.command()
@click.argument("parser_name")
@click.option("-c", "--class-parser", is_flag=True, help="Add class parser.")
def add_parser(parser_name, class_parser):
    """
    Add a parser named PARSER_NAME.
    Add class if class-parser flag is on, otherwise add method.
    """
    brainz = pathlib.Path(__file__).absolute().parent.parent / "brainz"
    filename = brainz / "parsers" / "parsers" / f"{parser_name}_parser.py"

    if pathlib.Path.is_file(filename):
        click.echo(f"A parser named {parser_name} already exists.")
        return

    parser_type = "class" if class_parser else "method"
    template = brainz / "resources" / f"{parser_type}_parser.template"

    with open(template, "r") as f:
        code = f.read().format(parser_name=parser_name.capitalize() if class_parser else parser_name)

    with open(filename, "w+") as f:
        f.write(code)

    click.echo(f"Successfully added parser {parser_name}")


if __name__ == "__main__":
    add_parser()
