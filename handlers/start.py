from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from keyboards import main_menu
from utils import is_admin
from config import PLATFORM

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    admin = is_admin(message.from_user)
    platform_fa = "بله" if PLATFORM == "bale" else "تلگرام"
    text = (
        f"سلام 👋\n"
        f"به بازوی <b>لوازم‌التحریر</b> خوش آمدید.\n"
        f"پلتفرم: {platform_fa}\n\n"
        f"از منوی زیر یکی از گزینه‌ها را انتخاب کنید:"
    )
    await message.answer(text, reply_markup=main_menu(admin), parse_mode="HTML")


@router.message(Command("menu"))
@router.message(F.text == "🔙 بازگشت به منوی اصلی")
async def back_to_main(message: Message, state: FSMContext):
    await state.clear()
    admin = is_admin(message.from_user)
    await message.answer("منوی اصلی:", reply_markup=main_menu(admin))


@router.message(Command("myid"))
async def cmd_myid(message: Message):
    """نمایش آیدی عددی کاربر برای افزودن به ADMIN_IDS"""
    u = message.from_user
    await message.answer(
        f"🆔 آیدی عددی شما: <code>{u.id}</code>\n"
        f"👤 نام: {u.full_name}\n"
        f"🔗 یوزرنیم: @{u.username or '—'}\n\n"
        f"این عدد را در متغیر محیطی <code>ADMIN_IDS</code> قرار دهید "
        f"(چند آیدی را با ویرگول جدا کنید).",
        parse_mode="HTML",
    )
