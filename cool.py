import os
import discord
from discord.ext import commands
import youtube_dl

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Bot online!')

server, server_id, name_channel = None, None, None

domains = ['htts://www.youtube.com/', 'http://www.youtube.com/', 'https://youtu.be/', 'http://youtu.be/']
async def check_domains(link):
    for x in domains:
        if link.startswith(x):
            return True
    return False


@bot.command()
async def play(ctx, *, command = None):
    global server, server_id, name_channel
    author = ctx.author
    if command == None:
        server = ctx.guild
        name_channel = author.voice.channel.name
        voice_channel = discord.utils.get(server.voice_channels, name = name_channel)
    params = command.split(' ')
    if len(params) == 1:
     sourse  = params[0]
     server = ctx.guild
     name_channel = author.voice.channel.name
     voice_channel = discord.utils.get(server.voice_channels, name = name_channel)
     print('param 1')
    elif len(params) == 3:
        server_id = params[0]
        voice_id = params[1]
        sourse  = params[2]
        try:
            server_id = int(server_id)
            voice_id = int(voice_id)
        except:
            await ctx.chanell.send(f'{author.mention}, id сервера или войса должно быть целочисленным')
            return
        print('param 3')
        server = bot.get_guild(server_id)
        voice_channel = discord.utils.get(server.voice_channels, id=voice_id)
    else:
        await ctx.channel.send(f'{author.mention} команда не корректна!')
        return

    if voice_channel is None:
        await ctx.channel.send(f'{author.mention}, указанный голосовой канал не найден!')
    return

    voice = discord.utils.get(bot.voice_clients, guild = server)
    if voice is None:
        await voice_channel.connect()
        voice = discord.utils.get(bot.voice_clients, guild = server)

    if sourse == None:
        pass
    elif sourse.startswith('http'):
        if not check_domains(sourse):
            await ctx.channel.send(f'{author.mention}, ссылка не является разрешенной!')
            return
        song_there = os.path.isfile('music/song.mp3')
        try:
            if song_there:
                os.remove('music/song.mp3')
        except PermissionError:
            await ctx.channel.send('Недостаточно прав для удаления файла!')
            return
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessons': [
                {
                    'key': 'FFmpegExtractAudio',
                    'prefferedcodec': 'mp3',
                    'preferredquality': '192',
                }
            ],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([sourse])
        for file in os.listdir('music/'):
            if file.endswith('.mp3'):
                os.rename(file, 'song.mp3')
        voice.play(discord.FFmpegPCMAudio('music/song.mp3'))
    else:
        voice.play(discord.FFmpegPCMAudio('music/{sourse}'))


bot.run('MTEwNDEyMjc0OTU0NDMwNDY0MA.GrJNMO.ROETaB7WO2jZmiW_O9VUZZQR0Z7FbvoAPULmUM')