import textwrap
from enum import Enum
from typing import Optional, List, Union

from rich.console import Console

from test_generator.generators import TestGenerator, AnthropicTestGenerator, OpenAITestGenerator, OllamaTestGenerator
from test_generator.settings import Settings


class ModelType(Enum):
    """
    Enumeration representing different AI model types for test generation.

    Attributes:
        SONNET (str): Represents the Claude 3.5 Sonnet model.
        GPT4 (str): Represents the GPT-4o model.
        OLLAMA (str): Represents the Codestral model.
    """
    SONNET = "sonnet3.5"
    GPT4 = "gpt4o"
    OLLAMA = "ollama"


class Generator:
    """
    A class to generate unit tests for a given class using various AI models.

    This class encapsulates the logic for creating prompts and generating unit tests
    using different AI models such as Anthropic's Claude 3 Sonnet, OpenAI's GPT-4o, or Ollama(Codestral).

    Attributes:
        console (Console): Rich console for output formatting.
        class_code (str): The code of the class for which tests are to be generated.
        context_code (List[str]): Additional contextual code to understand the class.
        sample (str): An optional sample of existing unit tests to guide the style.
        instruction (List[str]): Additional instructions for test generation.
        model (ModelType): The AI model to use for generation.
        settings (Settings): Configuration settings for API keys and other parameters.
        generator (TestGenerator): The specific test generator based on the chosen model.
    """

    def __init__(self, console: Console,
                 class_code: str,
                 context_code: Union[List[str], str, None] = None,
                 instruction: Union[List[str], str, None] = None,
                 sample: Optional[str] = None,
                 model: ModelType = ModelType.SONNET):
        """
        Initialize the Generator with the necessary parameters.

        Args:
            console (Console): Rich console for output formatting.
            class_code (str): The code of the class for which tests are to be generated.
            context_code (List[str], optional): Additional contextual code. Defaults to None.
            instruction (List[str], optional): Additional instructions for test generation. Defaults to None.
            sample (str, optional): An example of existing unit tests. Defaults to None.
            model (ModelType, optional): The AI model to use. Defaults to ModelType.SONNET.
        """
        self.console = console
        self.class_code = class_code
        self.context_code = self._process_input(context_code, "\n", "No contextual code provided.")
        self.instruction = self._process_input(instruction, ", ", "No additional instruction provided.")
        self.sample = sample or "No example provided."
        self.model = model
        self.settings = Settings()
        self.generator = self.__get_generator()

    @staticmethod
    def _process_input(input_data: Union[List[str], str, None],
                       separator: str, default: str) -> str:
        """
        Process input data, handling different types consistently.

        Args:
            input_data: The input data to process.
            separator: The separator to use when joining list elements.
            default: The default value to return if input is empty or None.

        Returns:
            Processed string representation of the input.
        """
        if isinstance(input_data, list) and input_data:
            return separator.join(input_data)
        elif isinstance(input_data, str) and input_data.strip():
            return input_data
        return default

    def __get_generator(self) -> TestGenerator:
        """
        Create and return the appropriate TestGenerator based on the selected model.

        This method initializes and returns the specific TestGenerator subclass
        corresponding to the chosen AI model.

        Returns:
            TestGenerator: An instance of the appropriate TestGenerator subclass.

        Raises:
            ValueError: If an unsupported model type is specified.
        """
        self.console.print(f"[cyan]Initializing {self.model.value} generator...")
        if self.model == ModelType.SONNET:
            return AnthropicTestGenerator(self.settings.ANTHROPIC_API_KEY)
        elif self.model == ModelType.GPT4:
            return OpenAITestGenerator(self.settings.OPENAI_API_KEY, self.settings.OPENAI_ORG_ID)
        elif self.model == ModelType.OLLAMA or self.model == ModelType.OLLAMA:
            return OllamaTestGenerator()
        else:
            raise ValueError(f"Unsupported model: {self.model}")

    def __create_prompt(self) -> str:
        """
        Create a detailed prompt for the AI model to generate unit tests.

        This method constructs a comprehensive prompt that includes instructions
        for generating unit tests, the class code, contextual code, and any
        provided examples or additional instructions.

        Returns:
            str: A formatted string containing the complete prompt for the AI model.
        """
        return textwrap.dedent(f"""
            You are an AI model designed to help write unit tests for a provided class. The user will supply one or two pieces of information:
            1. A class for which unit tests need to be written.
            2. (Optional) An example unit tests class that demonstrates the structure and style of the tests.
            3. (Optional) The contextual code to better understand the class from point 1.

            Your task is to generate unit tests for the provided class. If an example unit tests class is provided, ensure that the tests adhere to the same style, structure, and level of detail as the example. Additionally, use the Given-When-Then format to explain each test case and ensure that edge cases are considered. Follow best practices for writing tests, ensuring the generated code is clean and easy for developers to read.
            
            **Instructions:**
            
            1. Detect the programming language of the provided class.
            2. Analyze the provided class to understand its methods and functionalities.
            3. (If provided) Review the example unit tests class to understand its structure, naming conventions, and testing approach.
            4. Write unit tests for the provided class, ensuring each method is adequately tested, including edge cases.
            5. Use the Given-When-Then format to explain each test:
               - **Given**: The initial context or state.
               - **When**: The action or event that triggers the behavior.
               - **Then**: The expected outcome or result.
            6. Use appropriate libraries, frameworks, and patterns from the detected programming language to write the tests.
            7. Follow best practices for writing unit tests, including:
               - Clear naming conventions
               - Proper use of setup and teardown methods
               - Comprehensive assertions
               - Test isolation (ensure tests don't depend on each other)
               - Efficient test design to avoid unnecessarily slow tests
            8. Implement mocking and dependency injection where necessary to isolate the unit under test.
            9. Use parameterized tests when appropriate to test multiple scenarios with the same test logic.
            10. Aim for high code coverage (e.g., 80% or higher) and include a comment in the code about the estimated coverage achieved.
            11. Add code comments to explain complex test setups or assertions.
            12. Include tests for error scenarios and exception handling.
            13. Consider how the tests would run in a Continuous Integration (CI) environment and add any necessary setup or configuration as code or configuration files.
            14. Ensure the tests are clear, readable, and maintain consistency.
            15. Include necessary imports, setup methods, and assertions. If an example unit tests class is provided, follow its conventions.
            
            **Additional instructions:**
            {self.instruction}
            
            **Example:**
            
            - **Provided Class:**
            ```
            {self.class_code}
            ```
            
            - **(Optional) Contextual code:**
            ```
            {self.context_code}
            ```
            
            - **(Optional) Example Unit Tests Class:**
            ```
            {self.sample}
            ```
            
            **Output:**
            
            Generate a unit tests class for the provided class, and if an example is provided, format it similarly to the example unit tests class. Include Given-When-Then explanations for each test case as code comments, covering both typical scenarios and edge cases. Ensure the code follows best practices, is clean, and easy to read. Use the appropriate libraries and patterns from the detected programming language. 
            
            The output should contain ONLY the following, without any additional explanation or comments from the AI:
            1. The complete code for the unit tests, including imports and any necessary setup.
            2. A code comment about the estimated code coverage achieved.
            3. Any necessary setup or configuration for running in a CI environment, as code or configuration files.
            4. Code comments explaining complex test setups or assertions.
            
            Ensure that the generated tests are isolated, efficient, and cover error scenarios. Use mocking and dependency injection where appropriate, and implement parameterized tests for multiple similar scenarios. Do not include any text or explanations outside of the code and code comments.
            """)

    def generate_tests(self) -> str:
        """
        Generate unit tests using the configured AI model.

        This method creates the prompt, sends it to the appropriate AI model,
        and returns the generated unit tests.

        Returns:
            str: The generated unit tests as a string.
        """
        prompt = self.__create_prompt()
        self.console.print(f"[cyan]Sending request to {self.model.value}...")
        result = self.generator.generate(prompt)
        self.console.print(f"[green]Received response from {self.model.value}")
        return result
