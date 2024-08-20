# file_processor.py
from pathlib import Path
from typing import Optional, List

import pyperclip
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress

from test_generator.generator import ModelType, Generator


class TestProcessor:
    """
    A class to manage the process of generating unit tests using AI models.

    This class handles the entire workflow of reading input files, generating
    tests using a specified AI model, and outputting the results either to a
    file or the clipboard.

    Attributes:
        console (Console): Rich console for output formatting.
        input_path (Path): Path to the input file containing the code to test.
        example_path (Optional[Path]): Path to an example test file, if provided.
        context_paths (List[Path]): Paths to additional context files.
        instruction (List[str]): Additional instructions for test generation.
        output_path (Optional[Path]): Path to save the generated tests, if provided.
        model (ModelType): The AI model to use for test generation.
        progress (Progress): Progress bar for tracking the process.
    """

    def __init__(self, console: Console,
                 input_path: Path,
                 example_path: Optional[Path],
                 context_paths: List[Path],
                 instruction: List[str],
                 output_path: Optional[Path],
                 model: ModelType,
                 progress: Progress):
        """
        Initialize the TestProcessor with the necessary parameters.

        Args:
            console (Console): Rich console for output formatting.
            input_path (Path): Path to the input file containing the code to test.
            example_path (Optional[Path]): Path to an example test file, if provided.
            context_paths (List[Path]): Paths to additional context files.
            instruction (List[str]): Additional instructions for test generation.
            output_path (Optional[Path]): Path to save the generated tests, if provided.
            model (ModelType): The AI model to use for test generation.
            progress (Progress): Progress bar for tracking the process.
        """
        self.console = console
        self.input_path = input_path
        self.example_path = example_path
        self.output_path = output_path
        self.model = model
        self.progress = progress
        self.context_paths = context_paths
        self.instruction = instruction

    def process(self):
        """
        Execute the main test generation process.

        This method orchestrates the entire test generation workflow, including
        reading input files, generating tests, and outputting results. It also
        manages the progress bar updates and error handling.

        Raises:
            Exception: If an error occurs during the test generation process.
        """
        task = self.progress.add_task("[cyan]Processing...", total=100)
        self.progress.update(task, description="[cyan]Reading input file...", advance=10)
        content = self.__read_file(self.input_path)

        self.progress.update(task, description="[cyan]Reading example file (if provided)...", advance=10)
        example = self.__read_file(self.example_path) if self.example_path else ""

        self.progress.update(task, description="[cyan]Reading context files...", advance=10)
        context_contents = self.__read_context_files() if self.context_paths else None

        self.progress.update(task, description=f"[cyan]Generating tests using {self.model.value}...", advance=10)
        try:
            processed_content = self.__process_with_llm(content, example, context_contents, self.instruction)
            self.progress.update(task, description="[cyan]Outputting result...", advance=50)
            self.__output_result(processed_content)
            self.progress.update(task, description="[green]Processing complete!", advance=10)

        except Exception as e:
            self.progress.update(task, description="[bold red]Error!", advance=60)
            self.console.print(
                Panel(f"[bold red]Error generating tests:[/bold red] {str(e)}", title="Processing Error", expand=False))

    def __read_file(self, file_path: Path) -> str:
        """
        Read the contents of a file.

        Args:
            file_path (Path): The path to the file to be read.

        Returns:
            str: The contents of the file as a string.

        Raises:
            FileNotFoundError: If the specified file is not found.
            IOError: If there's an error reading the file.
        """
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

    def __read_context_files(self) -> List[str]:
        """
        Read the contents of all context files.

        Returns:
            List[str]: A list containing the contents of all context files.
        """
        context_contents = []
        for path in self.context_paths:
            content = self.__read_file(path)
            if content:
                context_contents.append(content)
        return context_contents

    def __process_with_llm(self, content: str, example: str, context_contents: List[str],
                           instruction: List[str]) -> str:
        """
        Process the input content using the specified LLM model to generate tests.

        Args:
            content (str): The main content to generate tests for.
            example (str): An example of existing tests, if provided.
            context_contents (List[str]): Additional context for test generation.
            instruction (List[str]): Additional instructions for test generation.

        Returns:
            str: The generated tests as a string.
        """
        test_generator = Generator(self.console, class_code=content, context_code=context_contents,
                                   instruction=instruction, sample=example, model=self.model)
        return test_generator.generate_tests()

    def __output_result(self, processed_content: str):
        """
        Output the processed content either to a file or the clipboard.

        Args:
            processed_content (str): The content to be output.

        Raises:
            IOError: If there's an error writing to the output file.
        """
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
        """
        Copy the given content to the clipboard.

        Args:
            content (str): The content to be copied to the clipboard.

        Raises:
            Exception: If there's an error copying to the clipboard.
        """
        try:
            pyperclip.copy(content)
            self.console.print(f"[green]Result copied to clipboard...")
        except Exception as e:
            self.console.print(Panel(f"[bold red]Error:[/bold red] Unable to copy to clipboard\n{str(e)}",
                                     title="Clipboard Error", expand=False))
            self.console.print(Panel("Result:", title="Output", expand=False))
            self.console.print(content)
