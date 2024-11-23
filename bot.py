import discord
from dotenv import load_dotenv
import os
from quotes import quotes
import random



load_dotenv()

# Define intents
intents = discord.Intents.default()  # Default intents (e.g., messages, reactions)
intents.message_content = True      # Enable specific intents, such as message content
intents.members = True
# Create bot instance with intents
bot = discord.Client(intents=intents)

prefix = "!"
ALLOWED_ROLES = ["Admin", "Psychic Detective Shrimp Spencer", "Big Shrimp Burton", ]

ALLOWED_COMMANDS = [
    f'{prefix}hello',
    f'{prefix}gimmiethatsweetknowledge',
    f'{prefix}shutit',
    f'{prefix}unshutit',
    f'{prefix}yes'
]

def has_allowed_role(user):
    """Check if the user has any of the allowed roles."""
    if isinstance(user, discord.Member):  # Ensure we have a Member object
        return any(role.name in ALLOWED_ROLES for role in user.roles)
    return False


@bot.event
async def on_ready():
    print("We're Up And Running Baby!!!")


@bot.event
async def on_message(message):

    if message.content == f'{prefix}hello':
        await message.channel.send("WHAT SPENCER")

    if not has_allowed_role(message.author) and any(message.content.startswith(c) for c in ALLOWED_COMMANDS):
        await message.channel.send(file=discord.File('assets/come_on_son.gif'))
        return

    # Gets a PSYCH quote
    if message.content == f'{prefix}gimmiethatsweetknowledge':
        random_quote_id = random.randint(1, len(quotes))
        await message.channel.send(quotes[random_quote_id])

    
    if message.content.startswith(f'{prefix}shutit'):
        if not message.author.guild_permissions.manage_roles:
            await message.channel.send("You don't have permission to use this command.")
            return

        try:
            # Extract the username from the command
            content = message.content.split()
            if len(content) < 2:
                await message.channel.send("Usage: !shutup @username")
                return

            # Get the mentioned user
            target_user = message.mentions[0] if message.mentions else None
            if not target_user:
                await message.channel.send("Please mention a valid user to mute.")
                return

            # Set channel permissions to mute the user
            overwrite = message.channel.overwrites_for(target_user)
            overwrite.send_messages = False
            await message.channel.set_permissions(target_user, overwrite=overwrite)
            await message.channel.send(
                content=f"{target_user.mention}",
                 file=discord.File('assets/shut_it.gif')
            )

        except discord.Forbidden:
            await message.channel.send("I don't have permission to modify this user's permissions.")
        except discord.HTTPException as e:
            await message.channel.send(f"An error occurred: {e}")
        except Exception as e:
            await message.channel.send(f"Unexpected error: {e}")

    # Unmute a user in the channel
    if message.content.startswith(f'{prefix}unshutit'):
        try:
            content = message.content.split()
            if len(content) < 2:
                await message.channel.send("Usage: !unshutup @username")
                return

            target_user = message.mentions[0] if message.mentions else None
            if not target_user:
                await message.channel.send("Please mention a valid user to unmute.")
                return

            # Unmute the user
            overwrite = message.channel.overwrites_for(target_user)
            overwrite.send_messages = None  # Clear the permission for sending messages
            await message.channel.set_permissions(target_user, overwrite=overwrite)

            # Notify about unmute
            await message.channel.send(
                content=f"{target_user.mention} has been unmuted!", 
            )
        except discord.Forbidden:
            await message.channel.send("I don't have permission to modify this user's permissions.")
        except discord.HTTPException as e:
            await message.channel.send(f"An error occurred: {e}")
        except Exception as e:
            await message.channel.send(f"Unexpected error: {e}")

    if message.content == f'{prefix}yes':
        await message.channel.send(file=discord.File('assets/yes.gif'))

print(os.getenv("TOKEN"))
bot.run(os.getenv("TOKEN"))


    