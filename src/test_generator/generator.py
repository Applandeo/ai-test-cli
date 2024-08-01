import textwrap
from enum import Enum
from typing import Optional

from rich.console import Console

from generators import TestGenerator, AnthropicTestGenerator, OpenAITestGenerator, OllamaTestGenerator
from settings import Settings


class ModelType(Enum):
    SONNET = "sonnet3.5"
    GPT4 = "gpt4o"
    OLLAMA = "ollama"
    CODESTRAL = "codestral"
    STARCODER2 = "starcoder2:3b"


class Generator:
    def __init__(self, console: Console,
                 class_code: str,
                 context_code: [str] = None,
                 instruction: str = None,
                 sample: Optional[str] = None,
                 model: ModelType = ModelType.SONNET):
        self.console = console
        self.class_code = class_code
        self.context_code = "\n".join(context_code) if context_code else "No contextual code provided."
        self.sample = sample or "No example provided."
        self.instruction = instruction or "No additional instruction provided."
        self.model = model
        self.settings = Settings()
        self.generator = self.__get_generator()

    def __get_generator(self) -> TestGenerator:
        self.console.print(f"[cyan]Initializing {self.model.value} generator...")
        if self.model == ModelType.SONNET:
            return AnthropicTestGenerator(self.settings.ANTHROPIC_API_KEY)
        elif self.model == ModelType.GPT4:
            return OpenAITestGenerator(self.settings.OPENAI_API_KEY, self.settings.OPENAI_ORG_ID)
        elif self.model == ModelType.OLLAMA or self.model == ModelType.CODESTRAL:
            return OllamaTestGenerator()
        elif self.model == ModelType.STARCODER2:
            return OllamaTestGenerator(model=ModelType.STARCODER2.value)
        else:
            raise ValueError(f"Unsupported model: {self.model}")

    def __create_prompt(self) -> str:
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
        prompt = self.__create_prompt()
        self.console.print(f"[cyan]Sending request to {self.model.value}...")
        result = self.generator.generate(prompt)
        self.console.print(f"[green]Received response from {self.model.value}")
        return result
