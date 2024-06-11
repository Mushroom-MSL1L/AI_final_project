# AI final project --- STEAM (Steam top expert analysis machine)
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
* ***Llama 2 is licensed under the LLAMA 2 Community License, Copyright (c) Meta Platforms, Inc. All Rights Reserved.***

* The project is a final project for NYCU CS AI course.
* Using LLM to generate the comments of the steam game.

## Introduction
* It's a project that can analysis the hot comments of the steam game.
* By clicking down a game name in UI, this program will automatically search the top comments of the game, and llama will organize top comments as a brief summerization. 
* If you want to know whether a game is good or not, but you don't rely on the grading, besides, you don't want to look reviews one by one. This program is extraordinary suit for you. 

## On local machine
### How to set up 
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
### How to use 
* cd to this folder `AI_final_project_SteamHotCommentFetcher\`
* run `chainlit run ui.py -w` in terminal
* open your browser and go to `http://localhost:8000`
* Type one game name you want to analysis
    * we recommend below games to test
        * "Cyberpunk 2077"
        * "Forza Horizon 4"
        * "Forza Horizon 5"
        * "The Witcher 3: Wild Hunt"
* wait for a while, you will see the result.

## On Colab
### How to set up
* Upload `STEAM.ipynb` to google Colab notebook.
* Run the code one by one in the notebook.
    * `Download llm model` part may need 30 seconds
    * `llama-cpp-python GPU ver. install` part may need 10 minutes
* In `Run` part you need to update `add-authtoken` with your own token.
    * go to [ngrok](https://ngrok.com/) and sign up.
    * get your token from [your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken)
    * Just press the `copy` button and paste it to the code.
    * like `!ngrok config add-authtoken 2hYXWxSKTePaAIU6Xb86s9EJgYa_53qzsH6jSz88QHBaKt4Ad`
* Keep run the remaining code, until it shows `http://localhost:8000`.
### How to use
* Click the link `http://localhost:8000` in the output.
* Type one game name you want to analysis
    * we recommend below games to test
        * "Cyberpunk 2077"
        * "Forza Horizon 4"
        * "Forza Horizon 5"
        * "The Witcher 3: Wild Hunt"
* wait for a while, you will see the result.

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Mushroom-MSL1L"><img src="https://avatars.githubusercontent.com/u/136601880?v=4?s=100" width="100px;" alt="Lu Junyou"/><br /><sub><b>Lu Junyou</b></sub></a><br /><a href="https://github.com/Mushroom-MSL1L/NYCU-AI-Final-Project-STEAM/commits?author=Mushroom-MSL1L" title="Code">💻</a> <a href="https://github.com/Mushroom-MSL1L/NYCU-AI-Final-Project-STEAM/issues?q=author%3AMushroom-MSL1L" title="Bug reports">🐛</a> <a href="#tutorial-Mushroom-MSL1L" title="Tutorials">✅</a> <a href="https://github.com/Mushroom-MSL1L/NYCU-AI-Final-Project-STEAM/pulls?q=is%3Apr+reviewed-by%3AMushroom-MSL1L" title="Reviewed Pull Requests">👀</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/WilsonNYCU"><img src="https://avatars.githubusercontent.com/u/166817905?v=4?s=100" width="100px;" alt="WilsonNYCU"/><br /><sub><b>WilsonNYCU</b></sub></a><br /><a href="#talk-WilsonNYCU" title="Talks">📢</a> <a href="https://github.com/Mushroom-MSL1L/NYCU-AI-Final-Project-STEAM/commits?author=WilsonNYCU" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>
<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
