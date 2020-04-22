""".on cmd to see if your userbot is ALIVE or Dead"""

import asyncio
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from uniborg.util import admin_cmd
import uniborg
from os import remove
from platform import python_version, uname
from shutil import which
from telethon import version

from asyncio import create_subprocess_shell as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE

from shutil import which
from os import remove
from telethon import version

from platform import python_version, uname
from sample_config import Config


# ================= CONSTANT =================
DEFAULTUSER = Config.ALIVE_NAME if Config.ALIVE_NAME else uname().node
# ============================================


# @register(outgoing=True, pattern="^.alive$")
@borg.on(admin_cmd("on"))
async def amireallyalive(on):
    """ For .on command, check if the bot is running.  """
    await on.edit(
                     " Я ЖИВИИИИИИИЙ!!!\n"
                     " F l e x B o t (Based on UniBorg)\n"
                      " Modded by @justgl\n"
                     f"тєℓєтнση νєяѕιση: {version.__version__} \n"
                     f"P̳y̳t̳h̳o̳n̳ ̳v̳e̳r̳s̳i̳o̳n̳: {python_version()} \n"
                     f"------------------------------------ \n"
                     f"User: {DEFAULTUSER} \n"
                     f"Creator: @🄼🄰🅈🅄🅁_🄺🄰🅁🄰🄽🄸🅈🄰 \n"
                     "`FlexBot працювати нормально, всі системи в нормі, база даних функціонує нормально!\nБліп-блоп)))`")    

    
