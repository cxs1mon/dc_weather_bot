import json
import discord
import requests

from weather import *

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
# token = insert token here before use
weather_prefix = 't.weather.'
command_prefix = 't.'
# api_key = insert api_key here before use


@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name=f'{command_prefix}command'))
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author != client.user and message.content.startswith(weather_prefix):
        location = message.content.replace(weather_prefix, '').lower()
        if len(location) >= 1:
            print(location)
            url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'
            try:
                data = json.loads(requests.get(url).content)
                data = parse_data(data)
                await message.channel.send(embed=weather_message(data, location))
            except KeyError:
                await message.channel.sen(embed=error_message(location))


client.run(token)
