import textwrap
from enum import Enum
from typing import Optional

from rich.console import Console

from .generators import TestGenerator, AnthropicTestGenerator, OpenAITestGenerator, OllamaTestGenerator
from .settings import Settings


class ModelType(Enum):
    SONNET = "sonnet3.5"
    GPT4 = "gpt4o"
    OLLAMA = "ollama"


class Generator:
    def __init__(self, console: Console, class_code: str, sample: Optional[str] = None,
                 model: ModelType = ModelType.SONNET):
        self.console = console
        self.class_code = class_code
        self.sample = sample or "No example provided."
        self.model = model
        self.settings = Settings()
        self.generator = self.__get_generator()

    def __get_generator(self) -> TestGenerator:
        self.console.print(f"[cyan]Initializing {self.model.value} generator...")
        if self.model == ModelType.SONNET:
            return AnthropicTestGenerator(self.settings.ANTHROPIC_API_KEY)
        elif self.model == ModelType.GPT4:
            return OpenAITestGenerator(self.settings.OPENAI_API_KEY, self.settings.OPENAI_ORG_ID)
        elif self.model == ModelType.OLLAMA:
            return OllamaTestGenerator()
        else:
            raise ValueError(f"Unsupported model: {self.model}")

    def __create_prompt(self) -> str:
        return textwrap.dedent(f"""
            You are an AI model designed to help write unit tests for a provided class. The user will supply one or two pieces of information:
            1. A class for which unit tests need to be written.
            2. (Optional) An example unit tests class that demonstrates the structure and style of the tests.

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
            7. Follow best practices for writing unit tests, including clear naming conventions, proper use of setup and teardown methods, and comprehensive assertions.
            8. Ensure the tests are clear, readable, and maintain consistency.
            9. Include necessary imports, setup methods, and assertions. If an example unit tests class is provided, follow its conventions.

            **Example:**

            - **Provided Class:**
              ```
                {self.class_code}
              ```

            - **(Optional) Example Unit Tests Class:**
              ```
                {self.sample}
              ```

            **Output:**

            Generate a unit tests class for the provided class, and if an example is provided, format it similarly to the example unit tests class. Include Given-When-Then explanations for each test case, covering both typical scenarios and edge cases. Ensure the code follows best practices, is clean, and easy to read. Use the appropriate libraries and patterns from the detected programming language. The output should contain only the code.
            """)

    def generate_tests(self) -> str:
        prompt = self.__create_prompt()
        self.console.print(f"[cyan]Sending request to {self.model.value}...")
        result = self.generator.generate(prompt)
        self.console.print(f"[green]Received response from {self.model.value}")
        return result
