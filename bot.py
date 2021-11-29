import discord
from discord.ext import commands
import urllib
import random
import asyncio
import qrcode

from discord_webhook import DiscordWebhook, DiscordEmbed

prefix = "?"
bot = commands.Bot(command_prefix=prefix)
bot.remove_command('help')
answers = ['Ja', 'Nein', 'Möglich', 'Defenetiv ja', 'Eventuell', 'Auf jeden Fall!', 'Da bin ich mir sicher', 'Nö',
           'Ne', 'Warscheinlich', 'Unwarscheinlich', 'Sehr Warscheinlich', 'Sehr Unwarscheinlich', 'Nicht möglich']
nummer = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
buchstabe = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
             'v', 'w', 'x', 'y', 'z']
def make_qr(msg):
    img= qrcode.make(msg)
    img.save("cache/qr.png")

@bot.event
async def on_ready():
    print('\r\nBot stertet LOL (hoffentlich crasht er nicht)')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Meet the Cores 3"),
                              status=discord.Status.do_not_disturb)


# HilfeListe
@bot.command()
async def help(ctx, page):
    if "meme" in page:
        embed = discord.Embed(color=0x0055ff, title="Meme Befehle")
        embed.add_field(name=f"**{prefix}dora**", value="Zeigt dir ein Video!", inline=False)
        embed.add_field(name=f"**{prefix}ripchat**", value="Here lies this Conversation!", inline=False)
        embed.add_field(name=f"**{prefix}ours**", value="Communism Kick!", inline=False)
        await ctx.send(embed=embed)
    if "fun" in page:
        embed = discord.Embed(color=0x0055ff, title="Fun Befehle")
        embed.add_field(name=f"**{prefix}sagmir <Frage>**", value="Beantwortet dir Entscheidungs Fragen!", inline=False)
        embed.add_field(name=f"**{prefix}rscreen**", value="Zeigt dir einen Random Screenshot an!", inline=False)
        embed.add_field(name=f"**{prefix}rimage**", value="Zeigt dir eine random Bild an!", inline=False)
        await ctx.send(embed=embed)

    if "tools" in page:
        embed = discord.Embed(color=0x0055ff, title="Minecraft Tools")
        embed.add_field(name=f"**{prefix}wetter <Stadt>**", value="Zeigt dir das Wetter an", inline=False)
        embed.add_field(name=f"**{prefix}delete <Menge>**", value="Löscht eine Gewisse Anzahl an Nachrichten",
                        inline=False)
        embed.add_field(name=f"**{prefix}ping**", value="Zeigt dir den Ping des Bots an", inline=False)
        embed.add_field(name=f"**{prefix}guilds**", value="Zeigt dir, auf wie vielen Servern ich bin", inline=False)
        await ctx.send(embed=embed)

    if "mc" in page:
        embed = discord.Embed(color=0x0055ff, title="Tools")
        embed.add_field(name=f"**{prefix}skin <Mc-Name>**", value="Zeigt dir den Skin eines Spielers an", inline=False)
        embed.add_field(name=f"**{prefix}kopf <Mc-Name>**", value="Zeigt dir den kopf eines Spielers an", inline=False)
        await ctx.send(embed=embed)


@help.error
async def help_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=0x0055ff, title="Kategorien",
                              description=f"**{prefix}help meme \r\n{prefix}help tools \r\n{prefix}help fun\r\n{prefix}help mc **")
        await ctx.send(embed=embed)


# Wetter Command
@bot.command()
async def wetter(ctx, *, wetter):
    urllib.request.urlretrieve('http://wttr.in/{0}.png?0?q'.format(wetter), 'cache/wheather.png')
    await ctx.send(file=discord.File('cache/wheather.png'))


@wetter.error
async def wetter_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=0xff0000)
        embed.add_field(name="Fehler! ", value="Falsche Verwendung, Versuche: \r\n `?wetter <Ort>`", inline=False)
        await ctx.send(embed=embed)


# Sagmir Command
@bot.command()
async def sagmir(ctx, *, question):
    async with ctx.typing():
        await asyncio.sleep(5)
    embed = discord.Embed(color=0x0055ff,
                          description=f" {ctx.author.mention} hat mir folgende Frage gestellt:\r\n\r\n**{question}** \r\n\r\n Meine Antwort lautet:\r\n\r\n **{random.choice(answers)}**")
    await ctx.send(embed=embed)


@sagmir.error
async def sagmir_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=0xff0000)
        embed.add_field(name="Fehler! ", value="Falsche Verwendung, Versuche: \r\n `?sagmir <Ja/Nein Frage>`",
                        inline=False)
        await ctx.send(embed=embed)


# Lösch command
@bot.command()
async def delete(ctx, amount):
    if ctx.author.permissions_in(ctx.channel).manage_messages:
        if amount.isdigit():
            count = int(amount) + 1
            deleted = await ctx.channel.purge(limit=count)
            await ctx.channel.send(
                'Ich habe {} Nachrichten brutal ermordet.:knife::drop_of_blood:'.format(len(deleted) - 1))
            await asyncio.sleep(3)
            await ctx.channel.purge(limit=1)
    else:
        print("Schas")


@delete.error
async def delete_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=0xff0000)
        embed.add_field(name="Fehler! ", value=f"Falsche Verwendung, Versuche: \r\n `{prefix}delete <Anzahl>`",
                        inline=False)
        await ctx.send(embed=embed)


# Rscreen command
@bot.command()
async def rscreen(ctx):
    await ctx.send('https://prnt.sc/{0}{1}{2}{3}{4}{5}'.format(random.choice(buchstabe), random.choice(buchstabe),
                                                               random.choice(nummer), random.choice(nummer),
                                                               random.choice(nummer), random.choice(nummer)))


# ping command
@bot.command()
async def ping(ctx):
    await ctx.send('Pong: **{0}ms** '.format(round(bot.latency * 1000)))


# dora command
@bot.command()
async def dora(ctx):
    await ctx.send('credits:**@tom_dude_360**')
    await ctx.send(file=discord.File('assets/dora.mp4'))


# ripchat
@bot.command()
async def ripchat(ctx):
    await ctx.send(file=discord.File('assets/hereliesthisconversation.jpeg'))


# guilds command
@bot.command()
async def guilds(ctx):
    await ctx.send('Ich bin auf {0} Servern'.format(len(ctx.guilds)))


# rimage command
@bot.command()
async def rimage(ctx):
    urllib.request.urlretrieve('https://picsum.photos/512', 'cache/random.png')
    await ctx.send(file=discord.File('cache/random.png'))


@bot.command()
async def guess(ctx, guesser):
    nummerbot = random.choice(nummer)
    if guesser is nummerbot:
        embed = discord.Embed(color=0x00ff08)
        embed.add_field(name="Richtig! ", value=f"Ich dachte an **{nummerbot}** und du an **{guesser}**!", inline=False)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=0xff0000)
        embed.add_field(name="Falsch! ", value=f"Ich dachte an **{nummerbot}** und du an **{guesser}**!", inline=False)
        await ctx.send(embed=embed)


@guess.error
async def guess_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=0xff0000)
        embed.add_field(name="Fehler! ",
                        value=f"Falsche Verwendung, Versuche: \r\n `{prefix}guess <Zahl zwischen 0 und 9>`",
                        inline=False)
        await ctx.send(embed=embed)


# mc Skin cmd
@bot.command()
async def skin(ctx, mcacc):
    urllib.request.urlretrieve('https://mc-heads.net/body/{0}'.format(mcacc), 'cache/body.png')
    await ctx.send(file=discord.File('cache/body.png'))


@bot.command()
async def kopf(ctx, mcacc):
    urllib.request.urlretrieve('https://cravatar.eu/helmhead/{0}/128.png'.format(mcacc), 'cache/Avatar.png')
    await ctx.send(file=discord.File('cache/Avatar.png'))


@bot.command()
async def ours(ctx):
    await ctx.send(file=discord.File('assets/ours.jpg'))


@bot.command()
async def russia(ctx):
    channel = ctx.author.voice.channel
    vc = await channel.connect()
    embed = discord.Embed(color=0xff0000)
    embed.add_field(name="Soundboard ", value=f"Russische Hymne\r\n requestet von {ctx.author.mention} ", inline=False)
    await ctx.send(embed=embed)
    vc.play(discord.FFmpegPCMAudio("sounds/russia.mp3"))
    while vc.is_playing():
        await asyncio.sleep(1)
    await vc.disconnect()


@bot.command()
async def tacobell(ctx):
    channel = ctx.author.voice.channel
    vc = await channel.connect()
    embed = discord.Embed(color=0xff0000)
    embed.add_field(name="Soundboard ", value=f"Tacobell Gong \r\n requestet von {ctx.author.mention} ", inline=False)
    await ctx.send(embed=embed)
    vc.play(discord.FFmpegPCMAudio("sounds/tacobell.mp3"))
    while vc.is_playing():
        await asyncio.sleep(1)
    await vc.disconnect()


@bot.command()
async def amogus(ctx):
    channel = ctx.author.voice.channel
    vc = await channel.connect()
    embed = discord.Embed(color=0xff0000)
    embed.add_field(name="Soundboard ", value=f"Amogus \r\n requestet von {ctx.author.mention} ", inline=False)
    await ctx.send(embed=embed)
    vc.play(discord.FFmpegPCMAudio("sounds/amogus.mp3"))
    while vc.is_playing():
        await asyncio.sleep(1)
    await vc.disconnect()


@bot.command()
async def boom(ctx):
    channel = ctx.author.voice.channel
    vc = await channel.connect()
    embed = discord.Embed(color=0xff0000)
    embed.add_field(name="Soundboard ", value=f"VineBoom \r\n requestet von {ctx.author.mention} ", inline=False)
    await ctx.send(embed=embed)
    vc.play(discord.FFmpegPCMAudio("sounds/vineboom.mp3"))
    while vc.is_playing():
        await asyncio.sleep(1)
    await vc.disconnect()


@bot.command()
async def fortnite(ctx):
    channel = ctx.author.voice.channel
    vc = await channel.connect()
    embed = discord.Embed(color=0xff0000)
    embed.add_field(name="Soundboard ", value=f"Deine Ohren wurden gekillt! \r\n requestet von {ctx.author.mention} ", inline=False)
    await ctx.send(embed=embed)
    vc.play(discord.FFmpegPCMAudio("sounds/fortnite.mp3"))
    while vc.is_playing():
        await asyncio.sleep(1)
    await asyncio.sleep(2)
    await vc.disconnect()


@bot.command()
async def again(ctx):
    channel = ctx.author.voice.channel
    vc = await channel.connect()
    embed = discord.Embed(color=0xff0000)
    embed.add_field(name="Soundboard ", value=f"Here we go again \r\n requestet von {ctx.author.mention} ", inline=False)
    await ctx.send(embed=embed)
    vc.play(discord.FFmpegPCMAudio("sounds/again.mp3"))
    while vc.is_playing():
        await asyncio.sleep(1)
    await asyncio.sleep(2)
    await vc.disconnect()


@bot.command()
async def speedrun(ctx):
    channel = ctx.author.voice.channel
    vc = await channel.connect()
    embed = discord.Embed(color=0xff0000)
    embed.add_field(name="Soundboard ", value=f"Dream Speedrun \r\n requestet von {ctx.author.mention} ", inline=False)
    await ctx.send(embed=embed)
    vc.play(discord.FFmpegPCMAudio("sounds/speedrun.mp3"))
    while vc.is_playing():
        await asyncio.sleep(1)
    await asyncio.sleep(2)
    await vc.disconnect()

@bot.command()
async def qrcode(ctx, *, args):
    make_qr(ctx)
    await ctx.send(file=discord.File('cache/qr.png'))

@bot.command()
async def table(ctx):
    channel = ctx.author.voice.channel
    vc = await channel.connect()
    embed = discord.Embed(color=0xff0000)
    embed.add_field(name="Soundboard ", value=f"Oh no, our Table, it's Broken \r\n requestet von {ctx.author.mention} ", inline=False)
    await ctx.send(embed=embed)
    vc.play(discord.FFmpegPCMAudio("sounds/table.mp3"))
    while vc.is_playing():
        await asyncio.sleep(1)
    await asyncio.sleep(2)
    await vc.disconnect()

@bot.command()
async def test(ctx, loc):
    for line in urllib.request.urlopen(f"http://wttr.in/{loc}?0?q?T"):
        await ctx.send(line)


bot.run("TOKEN")
