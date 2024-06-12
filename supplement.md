# Supplement in detailed 

## How to use model.py
* class LLM: you can directly use llama2 and get the output for the question prompt
* class Chain: chain llm and database for purpose. you can use the retriver to get the related context from database, then feed the additioinal information for llm.

## How to download llama model
* notice for changing model
    * please change `model_path` variable in `\AI_final_project_SteamHotCommentFetcher\Model\model.py` file
    * we are using __gguf__ file not ~~ggml~~
* You can download the llama model from the following two options.
    * You will need to request access from Meta AI to receive download links
        * [llama request](https://llama.meta.com/llama-downloads/)
    * Access meta-llama models on HuggingFace.
        * [hugging face](https://huggingface.co/meta-llama)
        * Our model is from [here](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/tree/main)
* Once you got approved, download the Llama model of your preference. For example, let’s say, you downloaded the llama-2–7b (the smallest) model.
* And the following instructions can look this link. [Llama 2 models for text embedding](https://medium.com/@liusimao8/using-llama-2-models-for-text-embedding-with-langchain-79183350593d)
    * note : If your are using MAC, in the convertion step, it may generate gguf file not bin file. And you need to ```./quantize ./models/llama-2-7b/llama-2-7b-7B-F32.gguf models/llama-2-7b/llama-2-7b-7B-F32-q4_0.gguf q4_0
``` rather than ```./quantize ./models/llama-2-7b/llama-2-7b-7B-F32.bin models/llama-2-7b/llama-2-7b-7B-F32-q4_0.bin q4_0```
## How to Use Fireworks API
* Create the `.env` file, in which you write your Fireworks API from ``https://fireworks.ai/api-keys`` Write your API KEY as,  `FIREWORKS_API_KEY="Your_API_KEY"`
* You are able to call function `fireworks(prompt: str)` by using `class LLM` in `Model` directory. Input and Output are all in string form. 

## How you find recommend games
* Access `game_list.txt`
* All games here are available in our STEAM system!!

## How to Reset cache
* Since we use cache to accelerate output, it may have same result for the same game name.
* If you are not satisfied with our STEAM's output,delete `cache.pkl` file. Then, all memoried cache is reset.
