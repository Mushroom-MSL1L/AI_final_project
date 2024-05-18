import chainlit as cl
from model import LLM
from model import Chain

llm = Chain(LLM())

# @cl.on_chat_start
# async def main():
#     res = await cl.AskUserMessage(content="What is the game name?", timeout=30).send()
#     if res:
#         await cl.Message(
#             content=f"Your name is: {res['content']}.\nChainlit installation is working!\nYou can now start building your own chainlit apps!",
#         ).send()

@cl.on_message
async def main(message: str):
    await cl.Message(
        content=llm.output(message.content),
    ).send()
