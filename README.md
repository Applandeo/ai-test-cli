# AI Test Generator CLI

AI Test Generator CLI is a powerful command-line tool that leverages various AI models to automatically generate unit tests for your code. It supports multiple programming languages and can adapt to your existing testing style.

## Features

- Generate unit tests using state-of-the-art AI models
- Support for multiple AI providers (Anthropic, OpenAI, Mistral)
- Ability to provide context and example tests for better results
- Flexible output options (file or clipboard)
- Rich console interface with progress tracking

## Installation

Install the AI Test Generator CLI using pip:

```
pip install ai-test-generator
```

## Configuration

Before using the tool, you need to set up your API keys:

- For Anthropic: Set the `ANTHROPIC_API_KEY` environment variable
- For OpenAI: Set the `OPENAI_API_KEY` and `OPENAI_ORG_ID` environment variables

You can set these environment variables in your shell or use a `.env` file in your project directory.

### Installing Ollama for Local Model Usage

If you want to use the local model option with Ollama, you need to install Ollama separately. Follow these steps:

1. Visit the official Ollama website: [https://ollama.ai/](https://ollama.ai/)

2. Download the appropriate version for your operating system:
   - For macOS: [Download](https://ollama.com/download/mac) the .dmg file and follow the installation prompts
   - For Linux: Use the following command in your terminal:
     ```
     curl https://ollama.ai/install.sh | sh
     ```
   - For Windows: Visit the [Ollama](https://ollama.com/download/windows) website for instructions

3. After installation, you need to pull the Codestral model. Open a terminal and run:
   ```
   ollama pull codestral
   ```

4. Once the model is downloaded, you can start the Ollama service:
   ```
   ollama serve
   ```

5. Keep the Ollama service running in the background while using the Test Generator CLI with the `ollama` model option.

Please note that the Codestral model requires significant computational resources. Ensure your system meets the necessary requirements before attempting to use it.

## Usage

After installation, you can use the tool from the command line:

```
ai-test-generator <input_file> [options]
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
   ai-test-generator my_code.py
   ```

2. Generate tests using GPT-4o, with an example and output to a file:
   ```
   ai-test-generator my_code.py -m gpt4o -e example_test.py -o generated_test.py
   ```

3. Generate tests with additional context and instructions:
   ```
   ai-test-generator my_code.py -c utils.py constants.py -i "Use pytest" "Include property-based tests"
   ```

4. Generate tests using the local Codestral model:
   ```
   ai-test-generator my_code.py -m ollama
   ```

## Demo

Here's a quick demonstration of how the Test Generator CLI works:

![Test Generator CLI Demo](/images/cli-test.gif)

This GIF showcases the tool in action, demonstrating its user interface, command-line options, and the process of generating tests.

## Using the Prompt Directly

If you prefer not to use our CLI tool, you can still benefit from our carefully crafted prompt by using it directly in AI chat interfaces like ChatGPT or Claude. Here's how:

1. Visit the prompt in our GitHub repository: [Test Generator Prompt](https://github.com/Applandeo/ai-test-cli/blob/main/test_generator/generator.py#L124)

2. Copy the prompt text.

3. Paste the prompt into your preferred AI chat interface (e.g., ChatGPT, Claude).

4. Replace the placeholders in the prompt with your specific information:
   - `{class_code}`: Your actual code that needs tests
   - `{sample}`: An example of your preferred testing style (optional)
   - `{context_code}`: Any additional context code (optional)
   - `{instruction}`: Any specific instructions for test generation (optional)

5. Send the message and the AI will generate tests based on your input.

This method allows you to leverage the power of our prompt without using the CLI tool, giving you flexibility in how you generate your tests.

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

## AI-Assisted Development

It's worth noting that a significant portion of the code for this project, including core functionality and documentation, was generated with the assistance of the Claude 3.5 Sonnet AI model. This AI-powered approach allowed for rapid development and comprehensive documentation of the Test Generator CLI tool.

The use of AI in the development process showcases the potential of AI-assisted coding and serves as a practical example of how the Test Generator CLI itself can be utilized in real-world scenarios.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.