import discord
from discord.ext import commands
import logging 
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
db = sqlite3.connect('tasks.db')
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    list_name TEXT,
    task TEXT,
    duration INTEGER
)
""")

db.commit()

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

list = {}


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}!')
    print('------')


# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return

#     if "shit" in message.content.lower():
#         await message.delete()
#         await message.channel.send(f'Please watch your language, {message.author.mention}!')

#     await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def add_task(ctx, list_name: str, duration: int, *, task: str):
    if list_name not in list:
        await ctx.send(f'List "{list_name}" does not exist! Please create it first using !add_list command.')
        return
    
    cursor.execute(
        "INSERT INTO tasks (list_name, task, duration) VALUES (?, ?, ?)",
        (list_name, task, duration)
    )
    db.commit()
    await ctx.send(f'Task "{task}" is added to list "{list_name}"! You have {duration} days to finish it.')


@bot.command()
async def add_list(ctx, *, list_name: str):
    list[list_name] = []
    await ctx.send(f'"{list_name}" is added!')

@bot.command()
async def show_tasks(ctx, list_name: str):
    cursor.execute(
        "SELECT task, duration FROM tasks WHERE list_name = ?",
        (list_name,)
    )

    rows = cursor.fetchall()

    if not rows:
        await ctx.send(f'No tasks found in {list_name}.')
        return

    for task, duration in rows:
        await ctx.send(f'{task} - {duration} days')



bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)