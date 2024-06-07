# AI final project --- STEAM (Steam top expert analysis machine)

* ***Llama 2 is licensed under the LLAMA 2 Community License, Copyright (c) Meta Platforms, Inc. All Rights Reserved.***

* The project is a final project for NYCU CS AI course.

## Introduction
* It's a project that can analysis the hot comments of the steam game.
* By clicking down a game name in UI, this program will automatically search the top comments of the game, and llama will organize top comments as a brief summerization. 
* If you want to know whether a game is good or not, but you don't rely on the grading, besides, you don't want to look reviews one by one. This program is extraordinary suit for you. 

## How to set up 
* programming language
    * We are recommend to use `python 3.10` or higher.
* packages 
    * cd to this folder `AI_final_project_SteamHotCommentFetcher\`
    * run `pip install -r requirements.txt`
* model
    * This repo do not provide model, you need to download a one. 
    * Download ```llama-2-7B.Q4_k_M model``` as ```gguf``` file from [here](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/blob/main/llama-2-7b-chat.Q4_K_M.gguf), so that you don't need to change any code.
    * Rename the file name as `llama-2-7b-chat.Q4_K_M.gguf`.
    * Make a folder whose name is `llama.cpp` under ```Model``` folder. And put your gguf file in it. There should has a path like ```AI_final_project_SteamHotCommentFetcher\Model\llama.cpp\llama-2-7b-chat.Q4_K_M.gguf```
    * More information can take a look at `supplement.md`.

## How to use 

## Contributor 


## to do 
* describe your functionality
* describe the steps of reproducibility at the end of the project