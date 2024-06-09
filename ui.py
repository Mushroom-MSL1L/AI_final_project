import chainlit as cl
from Model import chain
import time
import asyncio

chain = chain.Chain()

@cl.on_chat_start
async def main():
    res = await cl.AskUserMessage(content="Welcome to Steam Top Expert Analysis Machine (STEAM)!\nPlease type your name.", timeout=30).send()
    if res:
        await cl.Message(
            content=f"Your name is: {res['output']}.\nChainlit installation is working!\nYou can now start typing the game name!",
        ).send()

@cl.on_message
async def main(message: str):
    loading_msg = cl.Message(content="loading, please wait...")
    await loading_msg.send()

    result = await asyncio.to_thread(chain, message.content)

    loading_msg.content = result
    await loading_msg.update()

@cl.on_chat_end
def on_chat_end():
    print("The user disconnected!")