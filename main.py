from flask import Flask
from threading import Thread
import os
import g4f
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import re
import html

# Flask сервер для keep-alive
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Bot is alive!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Запускаем Flask в отдельном потоке
flask_thread = Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

# Основной код бота
BOT_TOKEN = os.getenv('BOT_TOKEN', "7236643509:AAEhGGP9CPnRcJVTHojegpBiGwk9oREXg_A")
CHANNEL_ID = "@pro_flauta"

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

class ChatStates(StatesGroup):
    chatting = State()

chat_contexts = {}

async def check_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status not in ['left', 'kicked', 'banned']
    except Exception:
        return False

def get_subscription_keyboard():
    keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="📢 Подписаться на канал")]], resize_keyboard=True)
    return keyboard

def get_main_keyboard():
    keyboard = [
        [KeyboardButton(text="🔄 Закончить беседу")],
        [KeyboardButton(text="🚀 Наши проекты"), KeyboardButton(text="🌿 Пользовательское соглашение")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def split_long_message(message, chunk_size=4096):
    return [message[i:i + chunk_size] for i in range(0, len(message), chunk_size)]

def get_user_agreement():
    return (
        "🌿 *Пользовательское соглашение для ИИ бота Neiro Flaut*\n\n"
        "📝 *1. Общие положения*\n"
        "1.1. Настоящее Пользовательское соглашение является юридически обязательным документом, который регулирует порядок использования ИИ бота Neiro Flaut.\n"
        "1.2. Используя Бота, пользователь подтверждает свое согласие с условиями данного Соглашения.\n\n"
        "🎯 *2. Предмет Соглашения*\n"
        "2.1. Бот обеспечивает взаимодействие с Пользователем на основе обработки и анализа текста с использованием нейронной сети Flaut-Fast.\n"
        "2.2. Бот предназначен для предоставления информации и помощи в различных областях.\n\n"
        "⚖️ *3. Права и обязанности сторон*\n"
        "3.1. Пользователь имеет право получать acceso к функционалу Бота и задавать вопросы.\n"
        "3.2. Пользователь обязуется не использовать Бота для распространения запрещенной информации.\n"
        "3.3. Бот имеет право прекращать доступ в случае нарушения условий Соглашения.\n\n"
        "🛡️ *4. Ограничение ответственности*\n"
        "4.1. Бот предоставляет информацию на основе доступных данных, однако не гарантирует ее точность.\n"
        "4.2. Бот не несет ответственности за последствия использования предоставленной информации.\n\n"
        "🔒 *5. Конфиденциальность*\n"
        "5.1. Все взаимодействия с Ботом могут быть записаны для улучшения качества обслуживания.\n"
        "5.2. Личные данные Пользователя не собираются и не обрабатываются.\n\n"
        "📅 *6. Заключительные положения*\n"
        "6.1. Соглашение вступает в силу с момента его акцепта Пользователем.\n"
        "6.2. В случае разногласий стороны стремятся решить их путем переговоров.\n\n"
        "*Дата последнего обновления: Август 2025 года (26.08.2025)*\n\n"
        "Использование Бота подразумевает полное согласие с условиями данного Соглашения."
    )

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    try:
        if not await check_subscription(message.from_user.id):
            await message.answer(
                "Для использования бота необходимо подписаться на мой канал @pro_flauta , я надеюсь, что это вас не отпугнет))",
                reply_markup=get_subscription_keyboard()
            )
            return
        await message.answer(
            "Привет, я Флаут, но также могу быть твоим истинным бро! Задавай любой вопрос, отвечу на всё, о чём бы ты хотел узнать. Моя база данных нейросети Flaut-Fast не даст быть никому равнодушным!) 💗\n\n"
            "Для начала общения, пожалуйста, нажмите /start , или просто задайте интересующий вопрос",
            reply_markup=get_main_keyboard()
        )
        await state.set_state(ChatStates.chatting)
        chat_contexts[message.from_user.id] = [{"role": "system",
                                                "content": "Пожалуйста, используй обычные математические символы и знаки вместо HTML-форматирования. Например, используй *, /, ^, ≤, ≥, ≠, ∑, ∏, √ и другие символы напрямую."}]
    except Exception as e:
        print(f"Error in start command: {e}")

@dp.message(lambda message: message.text == "🚀 Наши проекты")
async def show_projects(message: types.Message):
    if not await check_subscription(message.from_user.id):
        await message.answer(
            "Для использования бота необходимо подписаться на мой канал @pro_flauta , затем перезапустить бота /start. я надеюсь, что это вас не отпугнет))",
            reply_markup=get_subscription_keyboard()
        )
        return
    await message.answer(
        "Мои текущие проекты/соцсети:\n"
        "1. Телеграм канал создателя - https://t.me/travvisbot (да он школьник)\n"
        "2. Личка создателя - @poopker \n"
        "3. Сайт Флаута - https://flautgpt.yhub.net \n"
        "4. МирБезРКН - https://mirbezrkn.yhub.net \n"
    )

@dp.message(lambda message: message.text == "🌿 Пользовательское соглашение")
async def show_user_agreement(message: types.Message):
    if not await check_subscription(message.from_user.id):
        await message.answer(
            "Для использования бота необходимо подписаться на мой канал посвещенный Флауту и моим другим проектам, надеюсь, что это вас не отпугнет))",
            reply_markup=get_subscription_keyboard()
        )
        return

    agreement_text = get_user_agreement()
    split_messages = split_long_message(agreement_text)

    for msg in split_messages:
        await message.answer(msg, parse_mode="Markdown")

@dp.message(lambda message: message.text == "🔄 Закончить беседу")
async def end_chat(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in chat_contexts:
        chat_contexts.pop(user_id)
    await message.answer("Беседа завершена(( Можете начать новую беседу, просто задав вопрос, я всегда рад общению с вами!)")
    await state.set_state(ChatStates.chatting)
    chat_contexts[message.from_user.id] = [{"role": "system",
                                            "content": "Пожалуйста, используй обычные математические символы и знаки вместо HTML-форматирования. Например, используй *, /, ^, ≤, ≥, ≠, ∑, ∏, √ и другие символы напрямую."}]

@dp.message(ChatStates.chatting)
async def handle_message(message: types.Message, state: FSMContext):
    if not await check_subscription(message.from_user.id):
        await message.answer(
            "Для использования бота необходимо подписаться на наш канал!",
            reply_markup=get_subscription_keyboard()
        )
        return

    if message.text not in ["🔄 Закончить беседу", "🚀 Наши проекты", "🌿 Пользовательское соглашение"]:
        user_id = message.from_user.id
        user_input = message.text.strip()

        if user_id not in chat_contexts:
            chat_contexts[user_id] = [
                {"role": "system", "content": "Пожалуйста, ответь на вопрос пользователя четко и понятно."}]
        chat_contexts[user_id].append({"role": "user", "content": user_input})

        await message.bot.send_chat_action(message.chat.id, "typing")

        prompt = f"Пользователь спросил: '{user_input}'. Ответь четко и ясно и максимально комфортно, по дружески с искренностью и пониманием  на его вопрос."
        prompt += "\nИстория беседы:\n" + "\n".join([item["content"] for item in chat_contexts[user_id]])

        try:
            response = g4f.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
            )

            if isinstance(response, dict) and 'choices' in response:
                assistant_message = response['choices'][0]['message']['content']
            else:
                assistant_message = str(response)

        except Exception as e:
            assistant_message = f"Флаут просит прощения(( Произошла некоторая ошибка при генерации ответа: {str(e)} , пожалуйста, попробуйте позже 💔"
        
        chat_contexts[user_id].append({"role": "assistant", "content": assistant_message})
        decoded_response = html.unescape(assistant_message)
        split_messages = split_long_message(decoded_response)

        for msg in split_messages:
            await message.answer(msg, parse_mode="Markdown")

async def main():
    print("🤖 Бот Flaut запускается...")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
