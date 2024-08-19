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
    """Exception raised when no code is found in the API response."""
    pass


class TestGenerator(ABC):
    """
    Abstract base class for test generators.

    This class defines the interface for all test generators.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate tests based on the given prompt.

        Args:
            prompt (str): The prompt to generate tests from.

        Returns:
            str: The generated tests as a string.
        """
        pass


class AnthropicTestGenerator(TestGenerator):
    """
    Test generator using Anthropic's API.
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
    """

    def __init__(self, model: str = 'codestral'):
        """
        Initialize the Ollama test generator.

        Args:
            model (str, optional): The Ollama model to use. Defaults to 'codestral'.
        """
        self.model = model

    @staticmethod
    def __is_ollama_running() -> bool:
        """
        Check if Ollama is running.

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

        Raises:
            SystemExit: If Ollama is not installed.
        """
        return importlib.util.find_spec("ollama") is not None

    def generate(self, prompt: str) -> str:
        """
        Generate tests using Ollama.

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
