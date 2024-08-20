import importlib
from abc import ABC, abstractmethod
from typing import List, Any
import importlib.util
import sys

import anthropic
import ollama
import psutil
from openai import OpenAI


class CodeNotFoundException(Exception):
    """
    Exception raised when no code is found in the API response.

    This exception is typically raised when parsing the response from an AI service
    and no code block is found in the expected format.
    """
    pass


class TestGenerator(ABC):
    """
    Abstract base class for test generators.

    This class defines the interface for all test generators. Concrete implementations
    should inherit from this class and implement the generate method.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate tests based on the given prompt.

        This abstract method should be implemented by all concrete test generator classes.

        Args:
            prompt (str): The prompt to generate tests from.

        Returns:
            str: The generated tests as a string.
        """
        pass


class AnthropicTestGenerator(TestGenerator):
    """
    Test generator using Anthropic's API.

    This class implements the TestGenerator interface for Anthropic's AI service.
    It uses the Anthropic API to generate unit tests based on the given prompt.
    """

    def __init__(self, api_key: str):
        """
        Initialize the Anthropic test generator.

        Args:
            api_key (str): The API key for Anthropic's service.
        """
        self.client = anthropic.Anthropic(api_key=api_key)

    def generate(self, prompt: str) -> str:
        """
        Generate tests using Anthropic's API.

        This method sends the prompt to Anthropic's API and processes the response
        to extract the generated code.

        Args:
            prompt (str): The prompt to generate tests from.

        Returns:
            str: The generated tests as a string.

        Raises:
            CodeNotFoundException: If no code is found in the API response.
        """
        message = self.client.messages.create(
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="claude-3-sonnet-20240229",
        )
        return self.__extract_code_from_message(message.content)

    @staticmethod
    def __extract_code_from_message(content: List[Any]) -> str:
        """
         Extract code from the API response.

         This method parses the content returned by Anthropic's API and extracts
         the code block.

         Args:
             content (List[Any]): The content of the API response.

         Returns:
             str: The extracted code.

         Raises:
             CodeNotFoundException: If no code is found in the content.
         """
        for block in content:
            if block.type == "text":
                return block.text.strip()
        raise CodeNotFoundException("No code found in the API response.")


class OpenAITestGenerator(TestGenerator):
    """
    Test generator using OpenAI's API.

    This class implements the TestGenerator interface for OpenAI's service.
    It uses the OpenAI API to generate unit tests based on the given prompt.
    """

    def __init__(self, api_key: str, organization: str):
        """
        Initialize the OpenAI test generator.

        Args:
            api_key (str): The API key for OpenAI's service.
            organization (str): The organization ID for OpenAI.
        """
        self.client = OpenAI(api_key=api_key, organization=organization)

    def generate(self, prompt: str) -> str:
        """
        Generate tests using OpenAI's API.

        This method sends the prompt to OpenAI's API and processes the response
        to extract the generated code.

        Args:
            prompt (str): The prompt to generate tests from.

        Returns:
            str: The generated tests as a string.
        """
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates unit tests."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4096
        )
        return response.choices[0].message.content


class OllamaTestGenerator(TestGenerator):
    """
    Test generator using Ollama.

    This class implements the TestGenerator interface for Ollama.
    It uses Ollama(Codestral) to generate unit tests based on the given prompt.
    """

    def __init__(self, model: str = 'codestral'):
        """
        Initialize the Ollama test generator.

        Args:
            model (str, optional): The model to use. Defaults to 'codestral'.
        """
        self.model = model

    @staticmethod
    def __is_ollama_running() -> bool:
        """
         Check if Ollama is running.

         This method checks the system's running processes to determine if
         Ollama is currently active.

         Returns:
             bool: True if Ollama is running, False otherwise.
         """
        for process in psutil.process_iter(['name']):
            if process.name() == 'ollama':
                return True
        return False

    @staticmethod
    def __check_ollama_installed() -> bool:
        """
        Check if Ollama is installed.

        This method checks if the Ollama package is installed in the current
        Python environment.

        Returns:
            bool: True if Ollama is installed, False otherwise.
        """
        return importlib.util.find_spec("ollama") is not None

    def generate(self, prompt: str) -> str:
        """
        Generate tests using Ollama.

        This method checks if Ollama is installed and running, then uses it to
        generate unit tests based on the given prompt.

        Args:
            prompt (str): The prompt to generate tests from.

        Returns:
            str: The generated tests as a string.

        Raises:
            RuntimeError: If Ollama is not running or not installed.
        """
        if not self.__is_ollama_running():
            raise RuntimeError("Ollama is not running. Please start Ollama.")

        if not self.__check_ollama_installed():
            raise RuntimeError("Ollama is not installed. Please install it using: pip install ollama.")

        response = ollama.generate(self.model, prompt)
        return response['response']
