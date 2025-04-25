import os
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import Message
from telegraph import upload_file

load_dotenv()

API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not all([API_ID, API_HASH, BOT_TOKEN]):
    print("Error: API_ID, API_HASH, or BOT_TOKEN not set in .env file.")
    exit()

try:
    API_ID = int(API_ID)
except ValueError:
    print("Error: API_ID must be an integer.")
    exit()


teletips = Client(
    "MediaToTelegraphLink",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


@teletips.on_message(filters.command('start') & filters.private)
async def start(client, message):
    text = f"""
Heya {message.from_user.mention},
I am here to generate Telegraph links for your media files.

Simply send a valid media file directly to this chat.
Valid file types are 'jpeg', 'jpg', 'png', 'mp4' and 'gif'.

To generate links in group chats, add me to your supergroup and send the command /tl as a reply to a valid media file.

🏠 | [Home](https://t.me/FN7DANGER)
            """
    await teletips.send_message(message.chat.id, text, disable_web_page_preview=True)


@teletips.on_message(filters.media & filters.private)
async def get_link_private(client, message):
    try:  # ADDED try
        text = await message.reply("Processing...")

        async def progress(current, total):
            await text.edit_text(f"📥 Downloading media... {current * 100 / total:.1f}%")

        location = f"./media/private/"
        local_path = await message.download(location, progress=progress)
        await text.edit_text("📤 Uploading to Telegraph...")
        try:
            try: # wrap the call to upload_file with try/except
                upload_path = upload_file(local_path)
                print(f"Debug: upload_path = {upload_path}")  # Debug line
                await text.edit_text(f"🌐 | Telegraph Link:\n\nhttps://telegra.ph{upload_path[0]['src']}")  # THIS LINE IS LIKELY INCORRECT
                os.remove(local_path)
            except Exception as upload_error: #Catch errors related to upload_file
                print(f"upload_file error: {upload_error}")
                await text.edit_text(f"❌ | File upload to Telegraph failed.\n\nReason: {upload_error}")
                if os.path.exists(local_path): #Check if the file exists before attempting to remove
                                    os.remove(local_path)

        except Exception as e:  # ADDED EXCEPT
            print(f"get_link_private error: {e}")  # ADDED PRINT STATEMENT
            await message.reply(f"An error occurred: {e}")  # Send error message to Telegram


@teletips.on_message(filters.command('tl'))
async def get_link_group(client, message):
    try:  # ADDED TRY
        text = await message.reply("Processing...")

        async def progress(current, total):
            await text.edit_text(f"📥 Downloading media... {current * 100 / total:.1f}%")

        location = f"./media/group/"
        local_path = await message.reply_to_message.download(location, progress=progress)
        await text.edit_text("📤 Uploading to Telegraph...")
        try:
            try: # wrap the call to upload_file with try/except
                upload_path = upload_file(local_path)
                print(f"Debug: upload_path = {upload_path}")  # Debug line
                await text.edit_text(f"🌐 | Telegraph Link:\n\nhttps://telegra.ph{upload_path[0]['src']}")  # THIS LINE IS LIKELY INCORRECT
                os.remove(local_path)
            except Exception as upload_error: #Catch errors related to upload_file
                print(f"upload_file error: {upload_error}")
                await text.edit_text(f"❌ | File upload to Telegraph failed.\n\nReason: {upload_error}")
                if os.path.exists(local_path): #Check if the file exists before attempting to remove
                    os.remove(local_path)

        except Exception as e:  # ADDED EXCEPT
            print(f"get_link_group error: {e}")  # ADDED PRINT
            await message.reply(f"An error occurred: {e}")  # Send error message to Telegram


print("Bot is alive!")
teletips.run()
