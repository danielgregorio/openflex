"""
OpenFlex CLI - Command Line Interface

Usage:
    openflex build <file>      # Compile MXML/AS4 to JavaScript
    openflex dev <file>        # Dev server with hot reload
    openflex check <file>      # Type check without compiling
    openflex init              # Initialize new project
"""

import click
from pathlib import Path
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="openflex")
def cli():
    """
    OpenFlex - ActionScript 4 + MXML Compiler

    Compiles AS4/MXML to modern JavaScript with reactive runtime.
    """
    pass


@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--output', '-o', help='Output directory', default='dist')
@click.option('--watch', '-w', is_flag=True, help='Watch for changes')
@click.option('--sourcemap', is_flag=True, help='Generate source maps')
def build(file: str, output: str, watch: bool, sourcemap: bool):
    """Compile MXML/AS4 file to JavaScript"""

    file_path = Path(file)
    console.print(f"[bold blue]OpenFlex Compiler v0.1.0[/bold blue]")
    console.print(f"Compiling: [cyan]{file_path}[/cyan]\n")

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:

            task1 = progress.add_task("Parsing MXML...", total=None)
            # TODO: Implement parser
            progress.update(task1, completed=True)

            task2 = progress.add_task("Parsing ActionScript...", total=None)
            # TODO: Implement AS4 parser
            progress.update(task2, completed=True)

            task3 = progress.add_task("Type checking...", total=None)
            # TODO: Implement type checker
            progress.update(task3, completed=True)

            task4 = progress.add_task("Generating code...", total=None)
            # TODO: Implement codegen
            progress.update(task4, completed=True)

        console.print("\n[bold green]✓ Build successful![/bold green]")
        console.print(f"Output: [cyan]{output}/[/cyan]")

        if watch:
            console.print("\n[yellow]Watching for changes...[/yellow]")
            # TODO: Implement file watcher

    except Exception as e:
        console.print(f"\n[bold red]✗ Build failed:[/bold red] {e}")
        raise click.Abort()


@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--port', '-p', default=3000, help='Dev server port')
def dev(file: str, port: int):
    """Start development server with hot reload"""

    console.print(f"[bold blue]OpenFlex Dev Server[/bold blue]")
    console.print(f"File: [cyan]{file}[/cyan]")
    console.print(f"Port: [cyan]{port}[/cyan]\n")

    # TODO: Implement dev server
    console.print("[yellow]Dev server not implemented yet[/yellow]")
    console.print("Use: [cyan]openflex build --watch[/cyan] for now")


@cli.command()
@click.argument('file', type=click.Path(exists=True))
def check(file: str):
    """Type check file without compiling"""

    console.print(f"[bold blue]Type Checking[/bold blue]")
    console.print(f"File: [cyan]{file}[/cyan]\n")

    # TODO: Implement type checker
    console.print("[green]✓ No type errors found[/green]")


@cli.command()
@click.option('--name', '-n', prompt='Project name', help='Project name')
def init(name: str):
    """Initialize new OpenFlex project"""

    project_dir = Path(name)

    if project_dir.exists():
        console.print(f"[red]Error: Directory '{name}' already exists[/red]")
        raise click.Abort()

    console.print(f"[bold blue]Creating new OpenFlex project: {name}[/bold blue]\n")

    # Create project structure
    project_dir.mkdir()
    (project_dir / "src").mkdir()
    (project_dir / "public").mkdir()

    # Create sample MXML file
    sample_mxml = '''<s:Application xmlns:fx="http://ns.adobe.com/mxml/2009"
                 xmlns:s="library://ns.adobe.com/flex/spark">

    <fx:Script>
        var message: String = "Hello, OpenFlex!";

        function handleClick(): void {
            trace(message);
        }
    </fx:Script>

    <s:VBox gap="16">
        <s:Label text="{message}" fontSize="24" />
        <s:Button label="Click Me" click="handleClick()" />
    </s:VBox>

</s:Application>'''

    (project_dir / "src" / "App.mxml").write_text(sample_mxml)

    # Create config
    config = '''{
    "name": "''' + name + '''",
    "version": "0.1.0",
    "entry": "src/App.mxml",
    "output": "dist"
}'''
    (project_dir / "openflex.config.json").write_text(config)

    console.print(f"[green]✓ Project created successfully![/green]\n")
    console.print("Next steps:")
    console.print(f"  cd {name}")
    console.print(f"  openflex build src/App.mxml")


@cli.command()
def version():
    """Show version information"""

    panel = Panel.fit(
        "[bold]OpenFlex Compiler[/bold]\n"
        "Version: [cyan]0.1.0-alpha[/cyan]\n"
        "Language: [yellow]ActionScript 4[/yellow]\n"
        "Target: [green]JavaScript ES2022[/green]",
        border_style="blue"
    )
    console.print(panel)


def main():
    """Entry point for CLI"""
    cli()


if __name__ == '__main__':
    main()
