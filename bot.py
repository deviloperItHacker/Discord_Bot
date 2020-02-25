import discord
import re

from discord import Embed
from datetime import datetime

patern = re.compile(r"\@\&\d+")

bot = discord.Client()

TOKEN = ""

PREFIX = '$'

def count_week():
	td = datetime.today()
	wd = td.weekday()

	ds = datetime(year=td.year, month=td.month, day=td.day-wd)
	de = datetime(year=td.year, month=td.month, day=td.day)

	return ds, de

@bot.event
async def on_ready():
	print("I'm alive")

@bot.event
async def on_message(mes):
	member = mes.author
	guild = mes.guild
	channel = mes.channel

	content = mes.content

	if member.bot:
		return
	else:
		if content.startswith(PREFIX+'show_users'):
			command = content.split(" ")
			if len(command) > 1:
				try:
					res = patern.findall(command[1])[0][2:]
				except:
					for r in guild.roles:
						if r.name.lower() == command[1].lower():
							res = r.id
						else:
							res = 0	

				role = guild.get_role(int(res))
				if role != None:
					text = Embed()
					text.colour = role.color
					text.title = 'All members with role: '+role.name

					for i, mem in enumerate(role.members):
						text.add_field(name=str(i+1), value=mem.mention, inline=False)
					await channel.send(embed=text)	

		if content.startswith(PREFIX+'count_mes'):
			command = content.split(' ')

			text = Embed()
			text.colour = member.color
			text.title = 'Чё смотришь сюда!!!'

			try:
				chn = guild.fetch_channel(command[3:-1])
			except:
				chn = channel			
			
			all_mes = 0
			async for _ in chn.history(limit=None):
				all_mes += 1

			sth = count_week()

			per_week = 0
			async for _ in chn.history(limit=None, after=sth[0]):
				per_week += 1

			per_day = 0
			async for _ in chn.history(limit=None, after=sth[1]):	
				per_day += 1

			text.add_field(name="Messages per this day", value=str(per_day), inline=False)
			text.add_field(name="Messages per this week", value=str(per_week), inline=False)
			text.add_field(name="Messages per all time", value=str(all_mes), inline=False)	


			await channel.send(embed=text)

if __name__ == '__main__':
	bot.run(TOKEN)


