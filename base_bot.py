import time
import datetime
import os
from telethon import TelegramClient, events
from secrets import API_ID, API_HASH


# ================== SESSION VARIABLES ======================
STOP_TIME = {"HOUR": 18, "MINUTE": 30}

STOP_TIME_STRING = "18:30"
# ============================================================


# or use your own
api_id = os.environ.get("API_ID")
api_hash = os.environ.get("API_HASH")

# fill in your own details here
phone = os.environ.get("PHONE")
session_file = os.environ.get("SESSION_FILE")  # use your username if unsure

# content of the automatic reply
messages = [
    "👩‍💼 Ciao sono Daria, la BotSegretaria di Samuele.\n\nAl momento Samuele sta lavorando ad un importante progetto governativo segreto e non può rispondere.\n\nIn caso di urgenze, chiamalo al cellulare. Tornerà comunque disponibile dalle ore "
    + STOP_TIME_STRING
    + ".\n\n Buona giornata 🌱",
    "👩‍💼 Ciao come ti ho già detto sono Daria, la BotSegretaria.\n\nAl momento Samuele sta lavorando a una roba che se mo' te la spiego mi arriva in casa la polizia e mi fa un casino. Ti posso solo dire che ora NON può rispondere.\n\nNel caso di urgenze, comunque, chiamalo al cellulare. Tornerà disponibile alle ore "
    + STOP_TIME_STRING
    + ".",
    "👩‍💼 Ao' ti ho già spiegato che Samuele non può rispondere, prova a chiamarlo sul cellulare o aspetta le "
    + STOP_TIME_STRING
    + ".\n\nMo' basta non ti rispondo più che sto giocando a Candy Crush e mi fai perdere la concentrazione!",
]

# if __name__ == '__main__':
# Create the client and connect
# use sequential_updates=True to respond to messages one at a time
client = TelegramClient(session_file, api_id, api_hash, sequential_updates=True)


fromDict = {}
server_start_time = datetime.datetime.now()
daria_start_time = server_start_time.replace(hour=6, minute=0, second=0)
daria_end_time = server_start_time.replace(
    hour=STOP_TIME["HOUR"], minute=STOP_TIME["MINUTE"], second=0
)


def run():
    print("STO RUNANNDOOO")

    @client.on(events.NewMessage(incoming=True))
    async def handle_new_message(event):

        global fromDict

        if (
            datetime.datetime.now() > daria_end_time
            or datetime.datetime.now() < daria_start_time
        ):
            print("Time is over")
            await client.disconnect()

        if event.is_private:  # only auto-reply to private chats
            from_ = await event.client.get_entity(
                event.from_id
            )  # this lookup will be cached by telethon
            id = event.from_id.stringify()
            if fromDict.get(id) != None:
                fromDict[id] += 1
                print("aggiorno", fromDict)
            else:
                fromDict[id] = 0

            nResp = fromDict.get(id)

            if not from_.bot:  # don't auto-reply to bots
                time.sleep(5)  # pause for 1 second to rate-limit automatic replies

                if nResp < 3:
                    await event.respond(messages[nResp])

    print(time.asctime(), "-", "Auto-replying...")

    client.start(phone)
    # if server_start_time > daria_start_time and daria_end_time > server_start_time:
    client.run_until_disconnected()


run()
print(time.asctime(), "-", "Stopped!")
