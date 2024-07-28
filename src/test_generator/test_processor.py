# file_processor.py
from pathlib import Path
from typing import Optional

import pyperclip
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress

from generator import ModelType, Generator


class TestProcessor:
    def __init__(self, console: Console, input_path: Path, example_path: Optional[Path], output_path: Optional[Path],
                 model: ModelType, progress: Progress):
        self.console = console
        self.input_path = input_path
        self.example_path = example_path
        self.output_path = output_path
        self.model = model
        self.progress = progress

    def process(self):
        task = self.progress.add_task("[cyan]Processing...", total=100)
        self.progress.update(task, description="[cyan]Reading input file...", advance=10)
        content = self.__read_file(self.input_path)

        self.progress.update(task, description="[cyan]Reading example file (if provided)...", advance=10)
        example = self.__read_file(self.example_path) if self.example_path else ""

        self.progress.update(task, description=f"[cyan]Generating tests using {self.model.value}...", advance=10)
        processed_content = self.__process_with_llm(content, example)

        self.progress.update(task, description="[cyan]Outputting result...", advance=60)
        self.__output_result(processed_content)

        self.progress.update(task, description="[green]Processing complete!", advance=10)

    def __read_file(self, file_path: Path) -> str:
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            self.console.print(Panel(f"[bold yellow]Warning:[/bold yellow] File not found: {file_path}",
                                     title="File Not Found", expand=False))
            return ""
        except IOError as e:
            self.console.print(Panel(f"[bold red]Error:[/bold red] Unable to read file: {file_path}\n{str(e)}",
                                     title="File Read Error", expand=False))
            return ""

    def __process_with_llm(self, content: str, example: str) -> str:
        test_generator = Generator(self.console, content, example, self.model)
        return test_generator.generate_tests()

    def __output_result(self, processed_content: str):
        if self.output_path:
            try:
                with open(self.output_path, 'w') as file:
                    file.write(processed_content)
                self.console.print(Panel(f"Result written to [bold green]{self.output_path}[/bold green]",
                                         title="Success", expand=False))
            except IOError as e:
                self.console.print(
                    Panel(f"[bold red]Error:[/bold red] Unable to write to file: {self.output_path}\n{str(e)}",
                          title="File Write Error", expand=False))
                self.__copy_to_clipboard(processed_content)
        else:
            self.__copy_to_clipboard(processed_content)

    def __copy_to_clipboard(self, content: str):
        try:
            pyperclip.copy(content)
            self.console.print(f"[green]Result copied to clipboard...")
        except Exception as e:
            self.console.print(Panel(f"[bold red]Error:[/bold red] Unable to copy to clipboard\n{str(e)}",
                                     title="Clipboard Error", expand=False))
            self.console.print(Panel("Result:", title="Output", expand=False))
            self.console.print(content)