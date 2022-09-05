import disnake
from disnake.ext import commands

intents = disnake.Intents.default()
ibot = commands.InteractionBot(intents=intents)


@ibot.slash_command(description='create the invite')
async def create(inter, channel: disnake.TextChannel, max_uses: int, time_until_expire: int, unique: bool):
    if channel.is_nsfw():
        await inter.send(
            'i refuse to create invites for nsfw channels\n' +
            'do not uncheck the nsfw mark\njust pick another channel'
        )
        return
    if not channel.permissions_for(inter.guild.default_role).view_channel:
        await inter.send(
            'i refuse to create invites for private channels\n' +
            'do not uncheck the private mark\njust pick another channel'
        )
        return
    try:
        invite: disnake.Invite = await channel.create_invite(
            reason=f'invited by {inter.author.name}#{inter.author.discriminator}', max_uses=max_uses,
            max_age=time_until_expire, unique=unique
        )
    except disnake.Forbidden:
        await inter.send('i cant create an invite\nbecause i dont have perms')
    else:
        await inter.send(f'your next invite is {invite}')


@ibot.slash_command(description='get the vanity invite')
async def vanity(inter):
    invite = inter.guild.vanity_url_code
    if invite:
        await inter.send(f'your next invite is https://discord.gg/{invite}')
    else:
        await inter.send(f'no invite set')


with open(r'D:\\token_for_create_invite.py') as f:  # this path should be the path to a file o the token
    token = f.read()  # init should be nothing else than a token, or just assign to token directly
ibot.run(token)
