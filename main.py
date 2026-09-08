import discord
from discord.ext import commands
import logging 
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}!')
    print('------')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send(f'Please watch your language, {message.author.mention}!')

    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')
    
bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)