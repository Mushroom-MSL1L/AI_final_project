import chainlit as cl
import model

chain = model.Chain()

@cl.on_chat_start
async def main():
    res = await cl.AskUserMessage(content="Welcome to Steam-Hot-Comment-Fetcher (SHCT)!\nPlease type your name.", timeout=30).send()
    if res:
        await cl.Message(
            content=f"Your name is: {res['output']}.\nChainlit installation is working!\nYou can now start typing the game name!",
        ).send()


@cl.on_message
async def main(message: str):
    await cl.Message(
            # content=f"The game name is: {message.content}.",
            content = chain(message.content),
    ).send()

@cl.on_chat_end
def on_chat_end():
    print("The user disconnected!")
