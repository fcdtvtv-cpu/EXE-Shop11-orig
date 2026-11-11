from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton,
)

# --- Главное меню (внизу экрана) ---
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛒 Каталог товаров")],
        [KeyboardButton(text="📦 Заказать услугу")],
        [KeyboardButton(text="🔒 Безопасная сделка")],
        [KeyboardButton(text="💸 Возврат средств")],
        [KeyboardButton(text="⭐ Отзывы и сделки")],
        [KeyboardButton(text="🛠 Техподдержка")],
        [KeyboardButton(text="❓ Справка")],
    ],
    resize_keyboard=True,
)

# --- Категории каталога ---
categories = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🎮 Игры", callback_data="cat:games")],
    [InlineKeyboardButton(text="💻 IT-разработка", callback_data="cat:it")],
    [InlineKeyboardButton(text="🤖 AI-услуги", callback_data="cat:ai")],
    [InlineKeyboardButton(text="🌐 Хостинг", callback_data="cat:hosting")],
    [InlineKeyboardButton(text="⚙️ Макросы / автоматизация", callback_data="cat:macros")],
])

# --- Список всех товаров по категориям ---
PRODUCTS = {
    "games": [
        ("🎮 Игровые аккаунты и буст", "games:1"),
        ("💰 Игровая валюта и предметы", "games:2"),
        ("🛡 Античит / Обходы", "games:3"),
    ],
    "it": [
        ("🕷 Парсинг данных (Сбор баз)", "it:1"),
        ("🤖 Telegram-боты на заказ", "it:2"),
        ("📊 Автоматизация Excel / Google Sheets", "it:3"),
        ("🌐 Создание сайтов / Визиток", "it:4"),
    ],
    "ai": [
        ("🧠 AI-автоответчик (ChatGPT)", "ai:1"),
        ("✍️ Промпты для нейросетей", "ai:2"),
        ("🔑 Доступ к ChatGPT / Midjourney", "ai:3"),
    ],
    "hosting": [
        ("🖥 Аренда серверов (Minecraft/CS)", "hosting:1"),
        ("🛡 Прокси и VPN", "hosting:2"),
    ],
    "macros": [
        ("📢 Автопостинг контента", "macros:1"),
        ("⚙️ Скрипты для автоматизации рутины", "macros:2"),
        ("🎯 Макросы для игр", "macros:3"),
    ],
}

# --- Генератор кнопок для товаров ---
def products_kb(cat: str) -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(text=name, callback_data=f"prod:{cb}")]
            for name, cb in PRODUCTS.get(cat, [])]
    rows.append([InlineKeyboardButton(text="↩️ Назад", callback_data="back:cats")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

# --- Кнопки действий под конкретным товаром ---
def product_actions_kb(cb: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Оставить заявку", callback_data=f"order:{cb}")],
        [InlineKeyboardButton(text="🔒 Безопасная сделка", callback_data="safe:menu")],
        [InlineKeyboardButton(text="↩️ Назад", callback_data="back:cats")],
    ])

# --- Меню безопасной сделки ---
safe_deal_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔹 Playerok (Play Rock)", callback_data="safe:playerok")],
    [InlineKeyboardButton(text="🔹 Kwork", callback_data="safe:kwork")],
    [InlineKeyboardButton(text="🔹 GG Sell", callback_data="safe:gg")],
    [InlineKeyboardButton(text="↩️ Назад", callback_data="back:main")],
])

# --- Кнопка перехода на сайт ---
def link_kb(url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Перейти на сайт", url=url)],
        [InlineKeyboardButton(text="↩️ Назад", callback_data="safe:menu")],
    ])

# --- Меню возврата средств ---
refund_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔄 Оформить возврат в боте", callback_data="refund:bot")],
    [InlineKeyboardButton(text="🛠 Возврат через техподдержку", callback_data="refund:support")],
    [InlineKeyboardButton(text="↩️ Назад", callback_data="back:main")]
])

# --- Оценка + кнопка возврата (приходит после оплаты) ---
rating_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=str(i), callback_data=f"rate:{i}") for i in range(0, 6)],
    [InlineKeyboardButton(text="💸 Оформить возврат средств", callback_data="refund:bot")]
])
