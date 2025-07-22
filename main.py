from keep_alive import keep_alive
import json


import discord
import os
import random
from dotenv import load_dotenv
load_dotenv(dotenv_path="menu_bot_token.env")

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

import json

MENU_FILE = "menu.json"

# 메뉴 불러오기
def load_menu():
    try:
        with open(MENU_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

# 메뉴 저장하기
def save_menu():
    with open(MENU_FILE, "w", encoding="utf-8") as f:
        json.dump(menu_list, f, ensure_ascii=False, indent=2)

menu_list = load_menu()


@client.event
async def on_ready():
    print(f"✅ 봇 로그인됨: {client.user}")

@client.event
async def on_message(message):
    try:
        if message.author == client.user:
            return

        content = message.content.strip()

        if content.startswith('!추가'):
            parts = content.split(maxsplit=1)
            if len(parts) == 2:
                menu = parts[1].strip()
                if menu:
                    menu_list.append(menu)
                    save_menu()
                    await message.channel.send(f'✅ 메뉴 "{menu}" 추가됨!')
                else:
                    await message.channel.send('⚠️ 메뉴 이름을 입력해 주세요. 예: `!추가 치킨`')
            else:
                await message.channel.send('⚠️ 메뉴 이름을 입력해 주세요. 예: `!추가 치킨`')

        elif content == '!목록':
            if menu_list:
                menu_text = "\n".join(f"{i+1}. {m}" for i, m in enumerate(menu_list))
                await message.channel.send(f'🍽️ 현재 메뉴 목록:\n{menu_text}')
            else:
                await message.channel.send("⚠️ 아직 메뉴가 없어요!")

        elif content == '!추천':
            if menu_list:
                menu = random.choice(menu_list)
                await message.channel.send(f'🥁 오늘의 추천 메뉴는... **{menu}**!')
            else:
                await message.channel.send("⚠️ 추천할 메뉴가 없어요!")

        elif content.startswith('!삭제'):
            parts = content.split(maxsplit=1)
            if len(parts) == 2:
                menu_to_delete = parts[1].strip()
                if menu_to_delete in menu_list:
                    menu_list.remove(menu_to_delete)
                    save_menu() 
                    await message.channel.send(f'🗑️ 메뉴 "{menu_to_delete}"가 삭제되었습니다.')
                else:
                    await message.channel.send(f'⚠️ 메뉴 "{menu_to_delete}"가 목록에 없어요.')
            else:
                await message.channel.send('⚠️ 삭제할 메뉴 이름을 입력해 주세요. 예: `!삭제 치킨`')
    except Exception as e:
        print(f"오류 발생: {e}")

keep_alive()
client.run(TOKEN)
