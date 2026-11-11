import aiosqlite
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMIN_ID, SUPPORT_URL, DB_PATH
from keyboards import refund_menu

router = Router()

class RefundForm(StatesGroup):
    waiting_product = State()
    waiting_reason = State()
    waiting_requisites = State()

@router.message(F.text == "💸 Возврат средств")
async def open_refund(message: Message):
    await message.answer(
        "💸 <b>Возврат средств</b>\n\n"
        "Обратите внимание: не все товары подлежат возврату. "
        "Если товар был выдан и соответствует описанию, возврат невозможен.\n\n"
        "Выберите способ оформления:",
        reply_markup=refund_menu,
        parse_mode="HTML"
    )

@router.callback_query(F.data == "refund:support")
async def refund_support(call: CallbackQuery):
    await call.message.edit_text(
        f"🛠 Для оформления возврата напрямую обратитесь в техподдержку:\n{SUPPORT_URL}",
        disable_web_page_preview=True
    )

@router.callback_query(F.data == "refund:bot")
async def refund_bot(call: CallbackQuery, state: FSMContext):
    await state.set_state(RefundForm.waiting_product)
    await call.message.edit_text(
        "Шаг 1 из 3.\n\nНапишите, какой именно товар или услуга вам не подошли:"
    )

@router.message(RefundForm.waiting_product)
async def refund_product(message: Message, state: FSMContext):
    await state.update_data(product=message.text)
    await state.set_state(RefundForm.waiting_reason)
    await message.answer(
        "Шаг 2 из 3.\n\n"
        "Опишите причину возврата.\n"
        "<i>Если товар не был выдан, обязательно прикрепите фото/скриншот доказательства.</i>",
        parse_mode="HTML"
    )

@router.message(RefundForm.waiting_reason)
async def refund_reason(message: Message, state: FSMContext):
    # Сохраняем текст причины
    reason_text = message.text or "Без текста"
    photo_id = None
    
    # Если клиент прикрепил фото
    if message.photo:
        photo_id = message.photo[-1].file_id
        if not message.caption:
            reason_text = "Фото-доказательство"

    await state.update_data(reason=reason_text, photo=photo_id)
    
    data = await state.get_data()
    product = data['product']
    
    # Отправляем заявку тебе (Админу)
    admin_text = (
        f"🚨 <b>Новая заявка на возврат!</b>\n\n"
        f"👤 Клиент: @{message.from_user.username or '—'} (ID: {message.from_user.id})\n"
        f"📦 Товар: {product}\n"
        f"📝 Причина: {reason_text}"
    )
    
    if photo_id:
        await message.bot.send_photo(ADMIN_ID, photo_id, caption=admin_text, parse_mode="HTML")
    else:
        await message.bot.send_message(ADMIN_ID, admin_text, parse_mode="HTML")

    # Переходим к шагу 3
    await state.set_state(RefundForm.waiting_requisites)
    await message.answer(
        "✅ Ваша заявка отправлена техподдержке.\n\n"
        "Если товар/услуга действительно не была выдана/указана, возврат средств будет оформлен.\n\n"
        "Шаг 3 из 3. Оставьте реквизиты для возврата (Номер карты/телефона, Банк, ФИО):"
    )

@router.message(RefundForm.waiting_requisites)
async def refund_requisites(message: Message, state: FSMContext):
    data = await state.get_data()
    product = data['product']
    
    # Отправляем реквизиты тебе
    await message.bot.send_message(
        ADMIN_ID,
        f"💳 <b>Реквизиты для возврата!</b>\n\n"
        f"👤 Клиент: @{message.from_user.username or '—'}\n"
        f"📦 Товар: {product}\n"
        f"🏦 Реквизиты:\n{message.text}",
        parse_mode="HTML"
    )
    
    await message.answer(
        "🙏 Спасибо! Реквизиты переданы. Ожидайте ответа техподдержки.",
    )
    await state.clear()
