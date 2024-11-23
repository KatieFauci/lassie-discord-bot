import discord
from dotenv import load_dotenv
import os
from quotes import quotes
import random



load_dotenv()

# Define intents
intents = discord.Intents.default()  # Default intents (e.g., messages, reactions)
intents.message_content = True      # Enable specific intents, such as message content

# Create bot instance with intents
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print("We're Up And Running Baby!!!")


@bot.event
async def on_message(message):
    if message.content == "hello":
        await message.channel.send("WHAT SPENCER")

    # Gets a PSYCH quote
    if message.content == "/gimmiethatsweetknowledge":
        random_quote_id = random.randint(1, len(quotes))
        await message.channel.send(quotes[random_quote_id])

    if message.content == "/fuckoff":
        await message.channel.send("This is where I block some bitch")

    if message.content == "/yes":
        await message.channel.send(file=discord.File('assets/yes.gif'))

print(os.getenv("TOKEN"))
bot.run(os.getenv("TOKEN"))


    