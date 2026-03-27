import asyncio
import os
import re
from pathlib import Path

import telebot
from dotenv import load_dotenv

from ouo_bypass import bypass_many
from ouo_bypass import unique_ouo_urls


URL_PATTERN = re.compile(
    r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
)

load_dotenv(Path(__file__).with_name(".env"))

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not API_TOKEN:
    raise RuntimeError(
        "Missing TELEGRAM_BOT_TOKEN environment variable. "
        "Set it before starting the bot."
    )

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(
        message,
        "Send me one or more ouo.io / ouo.press links and I will try to bypass them.",
    )

@bot.message_handler(func=lambda message: True, content_types=['text','photo'])
def echo_all(message):
    urls = extract_urls(message)
    if urls:
        urls = unique_ouo_urls(urls)
        if not urls:
            bot.reply_to(
                message,
                'I found URLs, but none are ouo.io / ouo.press links that I can process.',
            )
            return
        bot.reply_to(message,f"⏳ Processing {len(urls)} URLs...")
        asyncio.run(process_urls(message, urls))


def extract_urls(message):
    if message.content_type == 'photo':
        return extract_urls_from_caption_entities(message)
    return URL_PATTERN.findall(message.html_text or '')


def extract_urls_from_caption_entities(message):
    urls = []
    if not message.caption_entities:
        return urls

    for entity in message.caption_entities:
        if entity.type in {'url', 'text_link', 'text_mention'}:
            entity_url = getattr(entity, 'url', None)
            if entity_url:
                urls.append(entity_url)
    return urls

async def process_urls(message, urls):
    msg = ""
    results = await bypass_many(urls)
    
    for result in results:
        if isinstance(result, Exception):
            msg += f"Error processing URL: {str(result)}\n\n"
        else:
            bypassed_link = result.get('bypassed_link')
            if bypassed_link:
                msg += f"{bypassed_link}\n"
            else:
                msg += f"Failed to bypass: {result.get('original_link', 'unknown URL')}\n"
    
    bot.reply_to(message, msg)

if __name__ == "__main__":
    bot.infinity_polling(none_stop=True)
