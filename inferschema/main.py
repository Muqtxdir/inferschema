"""CLI."""
import typer
import logging
from pathlib import Path
from rich.console import Console
from inferschema.schema_gen import Schemagenerator

app=typer.Typer(name= "inferschema", add_completion=False)


@app.command()
def generate_schema(file_path: Path = typer.Argument(..., help = "Provide the Input file."),
                    has_header: bool = typer.Option(False, "--header", "-h", is_flag = True, help = "Provide whether CSV has header.")):
    
    schema_generator = Schemagenerator()
    console = Console()

    if file_path.is_dir():
        for file in file_path.iterdir():
            if file.is_file():
                schema = schema_generator.generate_schema(file, has_header)
                if schema is not None:
                    console.print(f"Processing file: {file.name}")
                    console.print_json(schema.json())
    else:
        schema = schema_generator.generate_schema(file_path, has_header)
        if schema is not None:
            console.print_json(schema.json())

if __name__ == "__main__":
    app()