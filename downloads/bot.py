from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8688045222:AAGy37EWiT-PDt5rMHAajPybmQsTjmfNQws"

# لیست کشورها و نوع‌شان
EUROPE = ["روسیه🇷🇺", "المان🇩🇪", "فرانسه 🇲🇫"]
ASIA = ["ترکیه🇹🇷", "عراق🇮🇶", "چین🇨🇳", "امارات🇦🇪", "هند🇮🇳", "اسیای مرکزی", "تایلند 🇹🇭", "عمان 🇴🇲"]

# ذخیره وضعیت کاربران
user_state = {}
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user_state[chat_id] = "country"

    text = (
        "سلام به کنوانسیون تجارت ایران خوش اومدین 🌺\n"
        "لطفا گروه معاملاتی کشور خودتون رو انتخاب کنید:\n\n"
        "۱. روسیه🇷🇺\n"
        "۲. المان🇩🇪\n"
        "۳. ترکیه🇹🇷\n"
        "۴. عراق🇮🇶\n"
        "۵. چین🇨🇳\n"
        "۶. امارات🇦🇪\n"
        "۷. هند🇮🇳\n"
        "۸. اسیای مرکزی\n"
        "۹. فرانسه 🇲🇫\n"
        "۱۰. تایلند 🇹🇭\n"
        "۱۱. عمان 🇴🇲"
    )

    await update.message.reply_text(text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    text = update.message.text.strip()

    # مرحله انتخاب کشور
    if user_state.get(chat_id) == "country":
        user_data[chat_id] = {"country": text}
        user_state[chat_id] = "name"
        await update.message.reply_text("لطفا نام و نام خانوادگی خودتون رو وارد کنید")
        return

    # مرحله نام
    if user_state.get(chat_id) == "name":
        user_data[chat_id]["name"] = text
        user_state[chat_id] = "activity"
        await update.message.reply_text("لطفا زمینه فعالیت خودتون رو وارد کنید (مثلا تولید کننده پوشاک👕 یا ساختمان سازی 🏗)")
        return

    # مرحله فعالیت
    if user_state.get(chat_id) == "activity":
        user_data[chat_id]["activity"] = text
        country = user_data[chat_id]["country"]

        # تعیین قیمت‌ها
        if country in EUROPE:
            golden = "یک میلیون و نهصد هزار تومان"
            diamond = "دو میلیون و چهارصد هزار تومان"
        else:
            golden = "یک میلیون و چهارصد هزار تومان"
            diamond = "یک میلیون و هشتصد هزار تومان"

        msg = (
            f"۱. هزینه عضویت در گروه گلدن🪙 ({country}) : {golden}\n"
            f"۲. هزینه عضویت در گروه دایموند💎 ({country}) : {diamond}"
        )

        user_state[chat_id] = "final"
        await update.message.reply_text(msg)
        return

    # مرحله نهایی
    if user_state.get(chat_id) == "final":
        await update.message.reply_text(
            "لطفا پرداخت خودتون رو به این شماره کارت انجام بدید و رسید واریزی را "
            "در پشتیبانی @dornatejarat ارسال کنید.\n\n"
            "شماره کارت:\n۵۰۲۲.۲۹۱۵.۹۳۵۷.۰۰۴۵\n"
            "به نام: آقای سلیمانی"
        )
        user_state[chat_id] = None
        return


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("ربات روشن شد ...")
    app.run_polling()
