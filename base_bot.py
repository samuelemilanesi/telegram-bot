import time
import datetime
import os
from telethon import TelegramClient, events
from secrets import BOT_TOKEN, API_ID, API_HASH, PHONE, SESSION_FILE

# from AIMAGICROBODIMARTINO import responder


# ================== SESSION VARIABLES ======================
START_TIME = {"HOUR": 6, "MINUTE": 30}
STOP_TIME = {"HOUR": 18, "MINUTE": 30}

STOP_TIME_STRING = "18:30"
# ============================================================

# if __name__ == '__main__':
# Create the client and connect
# use sequential_updates=True to respond to messages one at a time
client = TelegramClient('bot',API_ID, API_HASH).start(bot_token=BOT_TOKEN)


# fromDict = {}

server_start_time = datetime.datetime.now()
start_time_dt = server_start_time.replace(
    hour=START_TIME["HOUR"], minute=START_TIME["MINUTE"], second=0
)
stop_time_dt = server_start_time.replace(
    hour=STOP_TIME["HOUR"], minute=STOP_TIME["MINUTE"], second=0
)


def responder(mes):
    return mes


incoming_message_text = "empty"


def run():
    print(">>> BOT STARTED")

    @client.on(events.NewMessage(incoming=True))
    async def handle_new_message(event):
        incoming_message_text = event.message.message
        if (
            datetime.datetime.now() > stop_time_dt
            or datetime.datetime.now() < start_time_dt
        ):
            print(">>> BOT STOPPED: out of time range")
            await client.disconnect()

        if event.is_private:  # only auto-reply to private chats
            time.sleep(1)  # pause for 1 second to rate-limit automatic replies
            await event.respond(responder(incoming_message_text))
            print(
                f">>> {time.asctime()} -- auto-replying to message:\n {incoming_message_text}"
            )

    client.start(PHONE)

    client.run_until_disconnected()


run()
print(f"{time.asctime()} -- BOT STOPPED BY THE USER")
