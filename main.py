import discord
from discord.ext import commands

import logging
import requests
import json
import random
import os
from dotenv import load_dotenv

load_dotenv()


TOKEN = os.getenv("DISCORD_API_KEY")
COOKIE = {'steamLoginSecure': os.getenv("STEAM_COOKIE")}

description = 'Python Discord Bot'

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix = '?', description=description)


@bot.event
async def on_ready():
    print("The bot is now ready for use")
    print("----------------------------")
    myActivity = discord.Game(name = "at your mum\'s 💦")
    await bot.change_presence(activity=myActivity, status=discord.Status.online)

@bot.command()
async def hello(ctx):
    await ctx.send("world")

@bot.command()
async def popuś(ctx):
    await ctx.send("Popuś! Popuś!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith('debil'):
        await message.channel.send('twoja stara')
    if message.content.startswith('bajo jajo'):
        await message.channel.send('ja ci dam bajo jajo')
    if message.content.startswith('helikopter helikopter'):
        await message.channel.send('Para kofer, para kofer')
    if message.content.startswith('despacito'):
        await message.channel.send('quiero respirar tu cuello despacito')
    if message.content.startswith('Wesołych Świąt'):
        await message.channel.send('Nawzajem')
    if message.content.find('trans') >= 0 or message.content.find('Trans') >= 0 or message.content.find('TRANS')>= 0 :
        await message.channel.send('Trans rights are human rights')
    if message.author.name == 'GGMW':
        insults = ['Jesteś useless na bocie!', 'Jesteś useless na topie!', 'Jesteś useless w lesie!',
        'Kochasz grać w drewutnię!', 'Masz większe ego niż Tymek lufę!', 'Jesteś fanboyem anime!', 'https://i.ibb.co/0Vzcpt9/Screenshot-2021-12-25-163816.png']
        await message.reply(random.choice(insults))

    await bot.process_commands(message)



@bot.command()
async def pullsteamprice(ctx, *arg):
    joining_word = ' '
    weapon_name = joining_word.join(arg)
    weapon_name_url = weapon_name
    weapon_name_url.replace(' ', '%20')
    response = requests.get('https://steamcommunity.com/market/priceoverview/?appid=730&market_hash_name=' + weapon_name_url + '&currency=6',  cookies=COOKIE)
    json_response = response.json()
    print(json_response)
    await ctx.send("Najniższa cena " + weapon_name + " na rynku to: " + json_response['lowest_price'])
    await ctx.send("Na rynku jest " + json_response['volume'] + ' ' + weapon_name)


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(652821241144541194)
    await channel.send("No siema")

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(652821241144541194)
    await channel.send("Żegnam")

bot.run(TOKEN)