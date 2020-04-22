# (c) @UniBorg
# justgl 
""" command: .flex """
from telethon import events
import asyncio
from collections import deque


@borg.on(events.NewMessage(pattern=r"\.flex", outgoing=True))
async def _(event):
	if event.fwd_from:
		return
	deq = deque(list("❤️F🧡L💛E💚X💙B💜O🖤T"))
	for _ in range(32):
		await asyncio.sleep(0.1)
		await event.edit("".join(deq))
		deq.rotate(1)
    
