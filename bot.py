import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("TOKEN")


async def mostrar_menu(chat):
    teclado = [
        [InlineKeyboardButton("🌐 Realizar atendimento pelo site", callback_data="site")],
        [InlineKeyboardButton("💬 Realizar atendimento pelo WhatsApp", callback_data="whatsapp")],
    ]

    await chat.send_message(
        text=(
            "Oi amore, aqui é a Lia do Cartomancias. 💜\n\n"
            "Por aqui não aceitamos consultas ainda, mas você pode nos chamar "
            "pelo nosso site ou pelo WhatsApp que vamos te atender rapidinho!"
        ),
        reply_markup=InlineKeyboardMarkup(teclado),
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await mostrar_menu(update.effective_chat)


async def mensagens(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await mostrar_menu(update.effective_chat)


async def botoes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "site":
        await query.message.reply_text(
            "Perfeito! 😊\n\n"
            "É só clicar no link abaixo e entrar em contato pelo chat que vamos te ajudar no que for preciso!\n\n"
            "https://www.cartomancias.com.br"
        )

    elif query.data == "whatsapp":
        await query.message.reply_text(
            "Perfeito! 😊\n\n"
            "É só nos chamar pelo WhatsApp que já vamos realizar a sua consulta!\n\n"
            "https://wa.me/5511937656368"
        )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(botoes))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensagens))

print("Bot iniciado!")

app.run_polling()