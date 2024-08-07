import argparse
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

from test_generator.generator import ModelType
from test_generator.test_processor import TestProcessor

console = Console()


def main():
    parser = argparse.ArgumentParser(description="Process a file using specified LLM model")
    parser.add_argument("input_path", help="Path to the input file")
    parser.add_argument("-o", "--output", help="Path to the output file (optional)")
    parser.add_argument("-m", "--model", type=ModelType, choices=list(ModelType),
                        default=ModelType.SONNET, help="LLM model to use (default: sonnet3.5)")
    parser.add_argument("-e", "--example", help="Path to the example test file (optional)")
    parser.add_argument("-c", "--context", nargs='+', help="List of paths to context files e.g. -c file1.py file2.py")
    parser.add_argument("-i", "--instruction", nargs='+', help="Additional instructions e.g. -i 'Use mocktail lib'")

    args = parser.parse_args()

    input_path = Path(args.input_path)
    output_path = Path(args.output) if args.output else None
    example_path = Path(args.example) if args.example else None
    context_paths = [Path(path) for path in args.context] if args.context else []
    instruction = args.instruction if args.instruction else None

    if not input_path.exists():
        console.print(Panel(f"[bold red]Error:[/bold red] Input file '{input_path}' does not exist.",
                            title="File Not Found", expand=False))
        sys.exit(1)

    console.print(Panel(f"Processing file: [bold]{input_path}[/bold]\n"
                        f"Model: [bold]{args.model.value}[/bold]\n"
                        f"Output: [bold]{output_path or 'Clipboard'}[/bold]\n"
                        f"Example: [bold]{example_path or 'Not provided'}[/bold]\n"
                        f"Context files: [bold]{'\n'.join(str(p) for p in context_paths) or 'Not provided'}[/bold]"
                        f"Instruction: [bold]{instruction or 'Not provided'}[/bold]\n",
                        title="File Processing", expand=False))

    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
    ) as progress:
        processor = TestProcessor(console, input_path, example_path, context_paths, instruction, output_path, args.model, progress)
        processor.process()

    console.print("[bold green]Processing complete![/bold green]")


if __name__ == "__main__":
    main()