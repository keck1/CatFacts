from datetime import datetime

import discord
import requests
from discord.ext import tasks, commands

intents = discord.Intents.default()
intents.message_content = True

botToken = "Token"
channelID = "Channel ID"

bot = commands.Bot(command_prefix="!", intents=intents)


async def fetch_random_fact():
    response = requests.get("https://meowfacts.herokuapp.com/")
    data = response.json()
    return data["data"][0]


async def fetch_random_pic():
    response = requests.get("https://api.thecatapi.com/v1/images/search")
    data = response.json()
    return data[0]["url"]


class fact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.random_fact_task.start()


# change the 'seconds' in @tasks.loop(seconds=300) to desired interval. default is 5 minutes.
    @tasks.loop(seconds=300)
    async def random_fact_task(self):
        channel = self.bot.get_channel(channelID)
        fact = await fetch_random_fact()
        image = await fetch_random_pic()

    # embed
        embed = discord.Embed(colour=0x8ceae0, timestamp=datetime.now())
        embed.set_author(name="Random Cat Facts", url="https://github.com/keck1")
        embed.set_image(url=image)
        embed.add_field(name="Did you know?", value=fact, inline=False)
        embed.set_thumbnail(url="https://i.ibb.co/3v7pHT7/catfactslog-removebg-preview.png")
        embed.set_footer(text="@keck1 on GitHub")

        await channel.send(embed=embed)

    @random_fact_task.before_loop
    async def before_random_fact_task(self):
        await self.bot.wait_until_ready()


# only visible in terminal
@bot.event
async def on_ready():
    print(f"{bot.user} is online")
    print(f"-"*30)
    await bot.add_cog(fact(bot))


bot.run(botToken)
