# Credits to https://t.me/anubisxx for this plugin


"""AFK Plugin for @UniBorg
Syntax: .afkb REASON"""
import asyncio
from asyncio import sleep
import datetime
import shutil 
import random, re
from random import choice, randint
import time
from time import gmtime, strftime
from datetime import timedelta
from datetime import datetime
from telethon import events
from telethon.tl import functions, types
from uniborg.util import progress, is_read, humanbytes, time_formatter, admin_cmd
from sample_config import Config
from platform import python_version, uname

# ================= CONSTANT =================
DEFAULTUSER = Config.ALIVE_NAME if Config.ALIVE_NAME else uname().node
# ============================================

# ========================= CONSTANTS ============================
AFKSTR = [
    "`AFK! Я зайнятий зараз. Якщо щось важливе - можете це написати. Або постарайтесь не забути це`",
    "AFK! Я тимчасово відсутній. Якщо вам щось потрібно - залиште повідомлення після сигналу:\n`ааааааааннннннііііімеееееееее`!",
    "`AFK! Я повернусь через кілька хвилин, а якщо ні...,\nтоді прочитайте це ще раз.`",
    "`AFK! Зараз я не тут, тому я, мабуть, десь ще.`",
    "`AFK! Киця робить 'Мяу',\nСобачка робить кусь,\nЗалиште мені повідомлення,\nЯ скоро повернусь.`",
    "`AFK! Іноді найкращих речей у житті варто чекати…\nЯ скоро повернусь.`",
    "`AFK! Я скоро повернусь,\nякщо не повернусь,\nЗачекайте трошки довше.`",
    "`AFK! Якщо ви цього ще не зрозуміли,\nЯ зараз не тут.`",
    "`AFK! Доброго здоров'ячка.\nВас вітає FlexBot.\nКористувач зараз не в мережі.\nОчікуйте відповіді`",
    "`AFK! Поїхав у навколосвітню подорож. Повернусь через 80 днів. Але ви можете написати СМС і я постараюсь вам чим швидше відписати`",
    "`AFK! На даний момент я не біля клавіатури, але якщо ви будете кричати досить голосно в екран, я зможу просто почути вас.`",
    "`AFK! Я пішов туди\n---->`",
    "`AFK! Я пішов сюди\n<----`",
    "`AFK! Пождіть, я тимчасово оффлайн.`",
    "`AFK! Якби я був би тут,\nЯ би про це сказав.\n\nАле я не тут...\nТому не скажу... Скоро повернусь`",
    "`AFK! Я зараз відсутній\nНе знаю, коли повернусь\nНадіюсь, що скоро`",
    "`AFK! Тимчасово відстуній!\nВи можете залишити заявку. Для цього потрібні ваші паспортні дані, адреса, а також фото вашої кредитної карти з обох сторін 😂😂😂`",
    "`AFK! Вибачте, я зараз відстуній.\nМожете поспілкуватись з FlexBot-ом прямо зараз.\nАле я не раджу цього робити...\nКраще зачекайте, коли я повернусь.`",
    "`AFK! Життя коротке... Ще треба зробити стільки речей...\nІ я роблю одну з них...`",
    "`AFK! Мене тут зараз немає...\nале якби був...\n\nЧи не було б це судово?`",
    
]
# ============================================

global USER_AFKB  # pylint:disable=E0602
global afkb_time  # pylint:disable=E0602
global last_afkb_message  # pylint:disable=E0602
global afkb_start
global afkb_end
USER_AFKB = {}
afkb_time = None
last_afkb_message = {}
afkb_start = {}

AFKSK = str(choice(AFKSTR))

@borg.on(events.NewMessage(pattern=r"\.afkb ?(.*)", outgoing=True))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    global USER_AFKB  # pylint:disable=E0602
    global afkb_time  # pylint:disable=E0602
    global last_afkb_message  # pylint:disable=E0602
    global afkb_start
    global afkb_end
    global reason
    USER_AFKB = {}
    afkb_time = None
    last_afkb_message = {}
    afkb_end = {}
    start_1 = datetime.now()
    afkb_start = start_1.replace(microsecond=0)
    reason = event.pattern_match.group(1)
    if not USER_AFKB:  # pylint:disable=E0602
        last_seen_status = await borg(  # pylint:disable=E0602
            functions.account.GetPrivacyRequest(
                types.InputPrivacyKeyStatusTimestamp()
            )
        )
        if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
            afkb_time = datetime.datetime.now()  # pylint:disable=E0602
        USER_AFKB = f"yes: {reason}"  # pylint:disable=E0602
        if reason:
            await borg.send_message(event.chat_id, f"** Користувач {DEFAULTUSER} перейшов у AFK,** __тому що він ~ {reason}__")
        else:
            await borg.send_message(event.chat_id, f"**Користувач 👑 {DEFAULTUSER} перейшов у AFK! Причина невідома...**")
        await asyncio.sleep(5)
        await event.delete()
        try:
            await borg.send_message(  # pylint:disable=E0602
                Config.PRIVATE_GROUP_BOT_API_ID,  # pylint:disable=E0602
                f"Set AFK mode to True, and Reason is {reason}"
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            logger.warn(str(e))  # pylint:disable=E0602


@borg.on(events.NewMessage(outgoing=True))  # pylint:disable=E0602
async def set_not_afkb(event):
    global USER_AFKB  # pylint:disable=E0602
    global afkb_time  # pylint:disable=E0602
    global last_afkb_message  # pylint:disable=E0602
    global afkb_start
    global afkb_end
    back_alive = datetime.now()
    afkb_end = back_alive.replace(microsecond=0)
    total_afkb_time = str(afkb_end - afkb_start)
    current_message = event.message.message
    if ".afkb" not in current_message and "yes" in USER_AFKB:  # pylint:disable=E0602
        shite = await borg.send_message(event.chat_id, "__КОРИСТУВАЧ ПОВЕРНУВСЯ__\n**USER IS BACK.**\n `Я був AFK :``" + total_afkb_time + "`")
        try:
            await borg.send_message(  # pylint:disable=E0602
                Config.PRIVATE_GROUP_BOT_API_ID,  # pylint:disable=E0602
                "Set AFK mode to False"
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await borg.send_message(  # pylint:disable=E0602
                event.chat_id,
                "Please set `PRIVATE_GROUP_BOT_API_ID` " + \
                "for the proper functioning of afk functionality " + \
                "ask in related group for more info.\n\n `{}`".format(str(e)),
                reply_to=event.message.id,
                silent=True
            )
        await asyncio.sleep(5)
        await shite.delete()
        USER_AFKB = {}  # pylint:disable=E0602
        afkb_time = None  # pylint:disable=E0602


@borg.on(events.NewMessage(  # pylint:disable=E0602
    incoming=True,
    func=lambda e: bool(e.mentioned or e.is_private)
))
async def on_afkb(event):
    if event.fwd_from:
        return
    global USER_AFKB  # pylint:disable=E0602
    global afkb_time  # pylint:disable=E0602
    global last_afkb_message  # pylint:disable=E0602
    global afkb_start
    global afkb_end
    back_alivee = datetime.now()
    afkb_end = back_alivee.replace(microsecond=0)
    total_afkb_time = str(afkb_end - afkb_start)
    afkb_since = "**a while ago**"
    current_message_text = event.message.message.lower()
    if "afkb" in current_message_text:
        # userbot's should not reply to other userbot's
        # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
        return False
    if USER_AFKB and not (await event.get_sender()).bot:  # pylint:disable=E0602
        if afkb_time:  # pylint:disable=E0602
            now = datetime.datetime.now()
            datime_since_afkb = now - afkb_time  # pylint:disable=E0602
            time = float(datime_since_afkb.seconds)
            days = time // (24 * 3600)
            time = time % (24 * 3600)
            hours = time // 3600
            time %= 3600
            minutes = time // 60
            time %= 60
            seconds = time
            if days == 1:
                afkb_since = "**Yesterday**"
            elif days > 1:
                if days > 6:
                    date = now + \
                        datetime.timedelta(
                            days=-days, hours=-hours, minutes=-minutes)
                    afkb_since = date.strftime("%A, %Y %B %m, %H:%I")
                else:
                    wday = now + datetime.timedelta(days=-days)
                    afkb_since = wday.strftime('%A')
            elif hours > 1:
                afkb_since = f"`{int(hours)}h{int(minutes)}m` **ago**"
            elif minutes > 0:
                afkb_since = f"`{int(minutes)}m{int(seconds)}s` **ago**"
            else:
                afkb_since = f"`{int(seconds)}s` **ago**"
        msg = None
        message_to_reply = f"Користувач {DEFAULTUSER} відсутній уже* {total_afkb_time}" + \
            f"\n__але скоро повернеться__\nВін сказав, що зараз він: {reason}" \
            if reason \
            else f"{AFKSK}\n`.Користувач {DEFAULTUSER} 👑 відсутній уже {total_afkb_time}.` "
        msg = await event.reply(message_to_reply)
        await asyncio.sleep(5)
        if event.chat_id in last_afkb_message:  # pylint:disable=E0602
            await last_afkb_message[event.chat_id].delete()  # pylint:disable=E0602
        last_afkb_message[event.chat_id] = msg  # pylint:disable=E0602
