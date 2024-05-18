# AI final project Steam-Hot-Comment-Fetcher (SHCT)

"notice" : Llama 2 is licensed under the LLAMA 2 Community License, 
Copyright (c) Meta Platforms, Inc. All Rights Reserved.

## Introduction
* It's a project that can fetch the hot comments of the steam game.
* The project is a final project for NYCU CS AI course.
* Using LLM to generate the comments of the steam game.

## How to download llama model
* You can download the llama model from the following two options.
    * You will need to request access from Meta AI to receive download links
        * [llama request](https://llama.meta.com/llama-downloads/)
    * Access meta-llama models on HuggingFace.
        * [hugging face](https://huggingface.co/meta-llama)
* Once you got approved, download the Llama model of your preference. For example, let’s say, you downloaded the llama-2–7b (the smallest) model.
* And the following instructions can look this link. [Llama 2 models for text embedding](https://medium.com/@liusimao8/using-llama-2-models-for-text-embedding-with-langchain-79183350593d)
    * note : If your are using MAC, in the convertion step, it may generate gguf file not bin file. And you need to ```./quantize ./models/llama-2-7b/llama-2-7b-7B-F32.gguf models/llama-2-7b/llama-2-7b-7B-F32-q4_0.gguf q4_0
``` rather than ```./quantize ./models/llama-2-7b/llama-2-7b-7B-F32.bin models/llama-2-7b/llama-2-7b-7B-F32-q4_0.bin q4_0
```. 