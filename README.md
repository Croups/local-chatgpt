# Local-ChatGPT

Local-ChatGPT is a project designed to demonstrate how to run local models—including vision, reasoning, and more—using Ollama on your own machine. The primary goal is to let you experiment with local models (via Ollama) that support features like vision (image processing) and reasoning. 

For users with hardware limitations or for those creating demo videos, an API version of the project has been hosted using Groq. The demo runs through Groq. 

---

## Project Purpose

- **Local Execution with Ollama:**  
  Run various models locally on your machine using Ollama. This allows you to experiment with models that support vision, reasoning, and other advanced features.  
  > **Note:** To use Ollama, you must download the Ollama application and pull the required models using the `ollama pull <model_name>` command.

- **API Demo via Groq:**  
  For users facing hardware limitations or for recording demos, an API version is available using Groq.  
  To use this version, obtain a Groq API key and add it to your `.env` file. The demo runs through Groq, eliminating local hardware constraints.

---

## Features

- **Local Execution with Ollama:**  
  - Test and run models locally with features such as vision and reasoning.
  - **Setup Required:** Download Ollama and pull the necessary models using the provided commands.

- **Groq API Demo:**  
  - Ideal for users with limited hardware or for creating demos.
  - Requires a Groq API key, which should be added to a `.env` file.

- **Multiple Model Support:**  
  - Switch between different models such as Llama3.2 Vision (multimodal), deepseek-r1:8b (reasoning, text-only), and phi3 (local, text-only).
  - Vision support is available only for the vision model.

- **Chainlit Integration:**  
  - A user-friendly, real-time chat interface powered by [Chainlit](https://docs.chainlit.io/).
  - Displays responses token by token for an interactive experience.

## DEMO

<!-- Uploading "2025-02-15 17-37-25.mp4"... -->
