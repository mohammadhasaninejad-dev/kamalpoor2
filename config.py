import os
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# پلتفرم: telegram  یا  bale
# ---------------------------------------------------------------------------
PLATFORM = os.getenv("PLATFORM", "telegram").strip().lower()
if PLATFORM not in ("telegram", "bale"):
    raise RuntimeError(f"PLATFORM must be 'telegram' or 'bale', got: {PLATFORM!r}")

BOT_TOKEN = os.getenv("BOT_TOKEN")

# آدرس پایهٔ API
# telegram → https://api.telegram.org
# bale     → https://tapi.bale.ai
_API_BASES = {
    "telegram": "https://api.telegram.org",
    "bale": "https://tapi.bale.ai",
}
API_BASE = os.getenv("API_BASE", _API_BASES[PLATFORM]).rstrip("/")

ADMINS = [
    # یوزرنیم‌ها (بدون @) — اختیاری؛ ترجیحاً از ADMIN_IDS استفاده کنید
    "mhasaninejad",
    "hamedkamalpour",
]

# آیدی عددی ادمین‌ها (در بله و تلگرام جدا هستند)
# برای گرفتن آیدی: داخل بات دستور /myid را بزنید
ADMIN_IDS = [
    int(x.strip())
    for x in os.getenv("ADMIN_IDS", "69947192,98546496").split(",")
    if x.strip().isdigit()
]

WEBAPP_URL = os.getenv("WEBAPP_URL", "https://your-app.up.railway.app")

# ⚠️ روی Railway حتماً Volume دائمی بسازید و مسیر را به آن بدهید
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/products.db")

PAGE_SIZE = int(os.getenv("PAGE_SIZE", "10"))
