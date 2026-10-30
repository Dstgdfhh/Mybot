from telethon import TelegramClient, events

# Укажите ваши данные с my.telegram.org
api_id =37006913 # Ваш API ID (число)
api_hash = 'f020a5489ed5f1f62b4
810ac4a842aed' # Ваш API Hash (в кавычках)

client = TelegramClient('session_render', api_id, api_hash)

# Кэш для сообщений: {msg_id: event_message}
message_cache = {}

@client.on(events.NewMessage(incoming=True))
async def cache_incoming(event):
    # Сохраняем входящие сообщения (текст, голосовые, видео)
    message_cache[event.id] = event.message

@client.on(events.NewMessage(outgoing=True))
async def handle_reply(event):
    # Проверяем, если вы отвечаете (Reply) на одноразовое фото/видео или любое другое медиа
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        if reply_msg and reply_msg.media:
            # Сохраняем медиафайл к себе в Избранное
            await client.send_message(
                'me',
                "💾 **Сохранен медиафайл из ответа (включая одноразовое):**",
                file=reply_msg.media
            )

@client.on(events.MessageDeleted())
async def detect_deleted(event):
    # Ловим удаление текстовых, голосовых и видеосообщений
    for msg_id in event.deleted_ids:
        if msg_id in message_cache:
            saved_msg = message_cache[msg_id]
            
            # Если было удалено медиа (голосовое, видео, круглые видео, фото)
            if saved_msg.media:
                await client.send_message(
                    'me',
                    f"🗑 **Удалено медиасообщение от {saved_msg.sender_id}:**",
                    file=saved_msg.media
                )
            # Если был удален обычный текст
            elif saved_msg.text:
                await client.send_message(
                    'me',
                    f"🗑 **Удалено текст от {saved_msg.sender_id}:**\n\n{saved_msg.text}"
                )
            
            del message_cache[msg_id]

print("Бот запущен и готов к работе...")
client.start()
client.run_until_disconnected()
