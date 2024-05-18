# AI final project Steam-Hot-Comment-Fetcher (SHCT)

## Introduction
* It's a project that can fetch the hot comments of the steam game.
* The project is a final project for NYCU CS AI course.
* Using LLM to generate the comments of the steam game.

# How to download Model
* Please access following HuggingFace to download .gguf file(not .ggml): https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/tree/main
* notice that after putting your model in directory, please change model_path in the class LLM

# How to use model.py
* class LLM: you can directly use llama2 and get the output for the question prompt
* class Chain: chain llm and database for purpose. you can use the retriver to get the related context from database, then feed the additioinal information for llm.