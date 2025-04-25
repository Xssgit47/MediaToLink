from pyrogram import Client, filters
from pyrogram.types import Message
from telegraph import upload_file
import os

teletips = Client(
    "MediaToTelegraphLink",
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"],
    bot_token=os.environ["BOT_TOKEN"]
)

@teletips.on_message(filters.command('start') & filters.private)
async def start(client, message):
    text = f"""
Heya {message.from_user.mention},
I am here to generate Telegraph links for your media files.

Simply send a valid media file directly to this chat.
Valid file types are 'jpeg', 'jpg', 'png', 'mp4' and 'gif'.

To generate links in **group chats**, add me to your supergroup and send the command <code>/tl</code> as a reply to a valid media file.

🏠 | [Home](https://t.me/teletipsofficialchannel)
            """
    await teletips.send_message(message.chat.id, text, disable_web_page_preview=True)


@teletips.on_message(filters.media & filters.private)
async def get_link_private(client, message):
    try:
        text = await message.reply("Processing...")
        async def progress(current, total):
            await text.edit_text(f"📥 Downloading media... {current * 100 / total:.1f}%")
        try:
            location = f"./media/private/"
            local_path = await message.download(location, progress=progress)
            await text.edit_text("📤 Uploading to Telegraph...")
            upload_path = upload_file(local_path)

            # Debugging: Log the upload_file return value
            print(f"DEBUG: upload_file returned: {upload_path} (Type: {type(upload_path)})")

            # Handle the return value properly
            if isinstance(upload_path, list) and len(upload_path) > 0:
                link = upload_path[0]
            elif isinstance(upload_path, str):
                link = upload_path
            else:
                raise ValueError(f"Unexpected return type from upload_file: {type(upload_path)}")

            await text.edit_text(f"**🌐 | Telegraph Link**:\n\n<code>https://telegra.ph{link}</code>")
            os.remove(local_path)
        except Exception as e:
            await text.edit_text(f"**❌ | File upload failed**\n\n<i>**Reason**: {e}</i>")
            if os.path.exists(local_path):
                os.remove(local_path)
            return
    except Exception as e:
        await message.reply(f"An unexpected error occurred: {e}")


@teletips.on_message(filters.command('tl'))
async def get_link_group(client, message):
    try:
        text = await message.reply("Processing...")
        async def progress(current, total):
            await text.edit_text(f"📥 Downloading media... {current * 100 / total:.1f}%")
        try:
            location = f"./media/group/"
            local_path = await message.reply_to_message.download(location, progress=progress)
            await text.edit_text("📤 Uploading to Telegraph...")
            upload_path = upload_file(local_path)

            # Debugging: Log the upload_file return value
            print(f"DEBUG: upload_file returned: {upload_path} (Type: {type(upload_path)})")

            # Handle the return value properly
            if isinstance(upload_path, list) and len(upload_path) > 0:
                link = upload_path[0]
            elif isinstance(upload_path, str):
                link = upload_path
            else:
                raise ValueError(f"Unexpected return type from upload_file: {type(upload_path)}")

            await text.edit_text(f"**🌐 | Telegraph Link**:\n\n<code>https://telegra.ph{link}</code>")
            os.remove(local_path)
        except Exception as e:
            await text.edit_text(f"**❌ | File upload failed**\n\n<i>**Reason**: {e}</i>")
            if os.path.exists(local_path):
                os.remove(local_path)
            return
    except Exception as e:
        await message.reply(f"An unexpected error occurred: {e}")

print("Bot is alive!")

teletips.run()
