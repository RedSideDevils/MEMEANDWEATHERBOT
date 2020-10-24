from discord.ext import commands
from bs4 import BeautifulSoup
import requests as r
import discord
import os
import random
import pyowm
from pyowm import OWM

class MyBot(commands.Bot):
    
    def __init__(self, command_prefix, self_bot):
        commands.Bot.__init__(self, command_prefix=command_prefix, self_bot=self_bot)
        self.message1 = "[INFO]: Bot now online"
        self.message2 = "Bot still online"
        self.add_commands()
    
    async def on_ready(self):
        print(self.message1)
    
    def add_commands(self):
        @self.command(name="meme", pass_context=True)
        async def meme(ctx):
            filter = []
            url_main = "https://www.memedroid.com/"
            content = r.get(url_main)
            soup = BeautifulSoup(content.text,'html.parser')
            memes = soup.find_all("img")

            for n in memes:
                if n['src'].startswith("https", 0, 5):
                    filter.append(n['src'])

            meme = random.choice(filter)
            embed = discord.Embed(title="Memes 1337",description="For {0.author.mention}".format(ctx))
            embed.set_image(url=meme)
            await ctx.channel.send(embed = embed)
        
        @self.command(name="wb", pass_context = True)
        async def wb(ctx,arg1):
            api_key = "6ea6db3313156ff68d16871e95ffc1b4"
            owm = OWM(api_key)

            if arg1 == "":
                await ctx.channel.send('{0.author.mention} To Activate Bot You need To Write Location.'.format(ctx))

            else:
                observation = owm.weather_at_place(str(arg1))
                w = observation.get_weather()
                data = {
                    'status':w.get_status(),
                    'temp'  :str(w.get_temperature('celsius')['temp']) + "*c"
                }
                embed = discord.Embed(title=arg1,description="{0.author.mention}".format(ctx))
                embed.add_field(name="Status",value = data['status'])
                embed.add_field(name='Temperature', value = data['temp'])
                await ctx.channel.send(embed=embed)

bot = MyBot(command_prefix="!", self_bot=False)
bot.run("token")
