# Test Generator CLI

Test Generator CLI is a powerful command-line tool that leverages various AI models to automatically generate unit tests for your code. It supports multiple programming languages and can adapt to your existing testing style.

## Features

- Generate unit tests using state-of-the-art AI models
- Support for multiple AI providers (Anthropic, OpenAI, Mistral)
- Ability to provide context and example tests for better results
- Flexible output options (file or clipboard)
- Rich console interface with progress tracking

## Installation

Install the Test Generator CLI using pip:

```
pip install test-generator
```

## Configuration

Before using the tool, you need to set up your API keys:

- For Anthropic: Set the `ANTHROPIC_API_KEY` environment variable
- For OpenAI: Set the `OPENAI_API_KEY` and `OPENAI_ORG_ID` environment variables

You can set these environment variables in your shell or use a `.env` file in your project directory.

## Usage

After installation, you can use the tool from the command line:

```
test-generator <input_file> [options]
```

### Options:

- `-o`, `--output`: Path to the output file (optional, defaults to clipboard)
- `-m`, `--model`: AI model to use (default: sonnet3.5)
- `-e`, `--example`: Path to an example test file (optional)
- `-c`, `--context`: List of paths to context files
- `-i`, `--instruction`: Additional instructions for test generation

### Examples:

1. Generate tests for a Python file using the default model (Claude 3.5 Sonnet):
   ```
   test-generator my_code.py
   ```

2. Generate tests using GPT-4o, with an example and output to a file:
   ```
   test-generator my_code.py -m gpt4o -e example_test.py -o generated_test.py
   ```

3. Generate tests with additional context and instructions:
   ```
   test-generator my_code.py -c utils.py constants.py -i "Use pytest" "Include property-based tests"
   ```

## Supported Models

- `sonnet3.5`: Anthropic's [Claude 3.5 Sonnet](https://www.anthropic.com/news/claude-3-5-sonnet)
- `gpt4o`: OpenAI's [GPT-4o](https://openai.com/index/hello-gpt-4o/) 
- `ollama`: Ollama ([Codestral](https://mistral.ai/news/codestral/))

### Important Note on Ollama and Codestral Model

When using the Ollama option, Test Generator CLI currently utilizes the Codestral model. Please be aware of the following limitations:

- Codestral is a large language model with 22B parameters.
- It requires a significant amount of computer memory (VRAM) to run.
- The model is currently under a non-production license.
- It is intended for research and testing purposes only.
- Due to these constraints, Codestral is not suitable for everyday use in production projects.

Please ensure your system meets the necessary requirements before attempting to use the Ollama option with the Codestral model.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.