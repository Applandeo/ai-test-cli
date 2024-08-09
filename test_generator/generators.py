import importlib
from abc import ABC, abstractmethod

import anthropic
import openai
from openai import OpenAI
from typing import List, Any
import importlib.util
import sys


class CodeNotFoundException(Exception):
    """Exception raised when no code is found in the API response."""
    pass


class TestGenerator(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass


class AnthropicTestGenerator(TestGenerator):
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def generate(self, prompt: str) -> str:
        try:
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
        except anthropic.APIError as e:
            return f"Error generating tests: {str(e)}"
        except CodeNotFoundException as e:
            return str(e)

    @staticmethod
    def __extract_code_from_message(content: List[Any]) -> str:
        for block in content:
            if block.type == "text":
                return block.text.strip()
        raise CodeNotFoundException("No code found in the API response.")


class OpenAITestGenerator(TestGenerator):
    def __init__(self, api_key: str, organization: str):
        self.client = OpenAI(api_key=api_key, organization=organization)

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates unit tests."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=4096
            )
            return response.choices[0].message.content
        except openai.OpenAIError as e:
            return f"Error generating tests: {str(e)}"


class OllamaTestGenerator(TestGenerator):
    def __init__(self, model: str = 'codestral'):
        self.model = model
        self._check_ollama_installed()

    @staticmethod
    def _check_ollama_installed():
        if importlib.util.find_spec("ollama") is None:
            sys.exit(1)

    def generate(self, prompt: str) -> str:
        try:
            import ollama
            response = ollama.generate(self.model, prompt)
            return response['response']
        except ImportError:
            return "Error: Ollama is not installed. Please install it using: pip install ollama"
        except Exception as e:
            return f"Error generating tests: {str(e)}"
