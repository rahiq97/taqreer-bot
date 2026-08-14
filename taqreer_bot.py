# -*- coding: utf-8 -*-
"""
بوت تقرير بلس - يستقبل طلبات التقارير ويرد تلقائي بالسعر
"""

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

# ============ عدّلي هالمعلومات بس ============
BOT_TOKEN = "8849001117:AAFEqPD0g_o9UYhXkm-TK_CSMQn1pRFQ52k"
PAYMENT_NUMBER = "3250745712"   # <-- حطي رقم بطاقة كي كارد
ADMIN_CHAT_ID = 5228198744   # آيدي حسابچ - يوصلچ إشعار بكل طلب
DELIVERY_DAYS = "2-3 أيام"        # <-- عدّلي مدة التسليم إذا تريدين
FIXED_PRICE = 10000               # السعر الثابت بالدينار
# ==============================================

# مراحل المحادثة
CHOOSING_TYPE, ASKING_DETAILS = range(2)

REPORT_TYPES = ["📚 بحث علمي", "🧪 تقرير مختبر", "📄 واجب دراسي", "🖥️ عرض تقديمي", "✏️ غيره"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[t] for t in REPORT_TYPES]
    await update.message.reply_text(
        "مرحباً بيك 👋 بوت تقرير بلس بخدمتك\n\n"
        "نساعدك تسوي تقاريرك الجامعية بسرعة واحترافية 🎓\n\n"
        "شنو نوع التقرير المطلوب؟",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    return CHOOSING_TYPE


async def choose_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["report_type"] = update.message.text
    await update.message.reply_text(
        "زين ✅\n\n"
        "هسه اكتبلي بنفس الرسالة:\n"
        "📚 اسم المادة/التخصص\n"
        "🏫 القسم\n"
        "🎓 المرحلة الدراسية\n"
        "📄 عدد الصفحات المطلوبة\n"
        "📅 تاريخ التسليم (شنو آخر موعد؟)\n\n"
        "📷 وإذا تريدين شعار جامعتج بالغلاف، أرسليه كصورة بعد هذي الرسالة",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ASKING_DETAILS


async def receive_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    details = update.message.text
    report_type = context.user_data.get("report_type", "غير محدد")

    summary = (
        f"استلمت طلبك 👌\n\n"
        f"📌 نوع التقرير: {report_type}\n"
        f"📌 التفاصيل: {details}\n\n"
        f"💰 السعر: {FIXED_PRICE:,} دينار عراقي\n"
        f"⏳ مدة التسليم: {DELIVERY_DAYS}\n\n"
        f"طريقة الدفع:\n"
        f"◆ بطاقة كي كارد: {PAYMENT_NUMBER}\n"
        f"   • إذا عدج حساب كي: حولي مباشرة لهذا الرقم\n"
        f"   • أو روحي لأقرب مكتب كي كارد وحولي المبلغ لنفس الرقم\n\n"
        f"✅ بعد إرسال إشعار الدفع (سكرين شوت) نبدأ فوراً بشغلك\n\n"
        f"لطلب جديد اكتب /start"
    )
    await update.message.reply_text(summary)
    admin_msg =(
        f"🔔 طلب جديد!\n\n"
        f"👤 الاسم: {update.effective_user.first_name}\n"
        f"🆔 يوزر: @{update.effective_user.username}\n"
        f"🔢 آيدي: {update.effective_user.id}\n"
        f"📌 نوع التقرير: {report_type}\n"
        f"📌 التفاصيل: {details}"
    )
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_msg)
    return ConversationHandler.END

async def deliver_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_CHAT_ID:
        return
    if not update.message.caption:
        await update.message.reply_text("لازم تكتبين آيدي الزبون بالوصف (caption) وياه الملف")
        return
    try:
        target_id = int(update.message.caption.strip())
    except ValueError:
        await update.message.reply_text("آيدي غير صحيح، أكتبي رقم بس")
        return

    if update.message.document:
        await context.bot.send_document(chat_id=target_id, document=update.message.document.file_id, caption="📎 تقريرج جاهز، نتمنالك التوفيق ✅")
    elif update.message.photo:
        await context.bot.send_photo(chat_id=target_id, photo=update.message.photo[-1].file_id, caption="📎 تقريرج جاهز، نتمنالك التوفيق ✅")
    await update.message.reply_text("✅ تم إرسال الملف للزبون")
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("تم إلغاء الطلب. لو حاب تبدأ من جديد اكتب /start", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📝 تقرير بلس\n\n"
        "نسوي تقارير جامعية لكل التخصصات بجودة عالية وتنسيق احترافي.\n\n"
        f"✅ سعر ثابت: {FIXED_PRICE:,} دينار عراقي\n"
        f"✅ مدة التسليم: {DELIVERY_DAYS}\n"
        "✅ مراجعة وتعديل حسب الحاجة\n\n"
        "للطلب اكتب /start"
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_type)],
            ASKING_DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_details)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("about", about))
   app.add_handler(MessageHandler((filters.Document.ALL | filters.PHOTO) & filters.User(ADMIN_CHAT_ID), deliver_file)) 

    print("البوت شغال... اتركي هالنافذة مفتوحة")
    app.run_polling()


if __name__ == "__main__":
    main()
