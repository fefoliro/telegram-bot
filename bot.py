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


async def menu_teclado():
    teclado = [
        [
            InlineKeyboardButton(
                "🌐 Realizar atendimento pelo site",
                callback_data="site"
            )
        ],
        [
            InlineKeyboardButton(
                "💬 Realizar atendimento pelo WhatsApp",
                callback_data="whatsapp"
            )
        ],
    ]

    return InlineKeyboardMarkup(teclado)


async def enviar_menu(chat):
    await chat.send_message(
        text=(
            "Oi amore, aqui é a assistente virtual do Cartomancias. 💜\n\n"
            "Por aqui não aceitamos consultas ainda, mas você pode nos chamar "
            "pelo nosso site ou pelo WhatsApp que vamos te atender rapidinho!\n\n"
            "Nosso horário de funcionamento é das 10:00 às 00:00 "
            "de segunda à sexta-feira."
        ),
        reply_markup=await menu_teclado(),
    )


# Usuários falando diretamente com o bot
async def mensagens(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat:
        await enviar_menu(update.effective_chat)


# Usuários falando com sua conta Telegram Business
async def mensagens_business(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.business_message:
        await update.business_message.reply_text(
            text=(
                "Oi amore, aqui é a assistente virtual do Cartomancias. 💜\n\n"
                "Como posso ajudar?"
            ),
            reply_markup=await menu_teclado(),
        )


# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat:
        await enviar_menu(update.effective_chat)


# Botões
async def botoes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    if query.data == "site":
        await query.message.reply_text(
            "Perfeito! 😊\n\n"
            "Acesse nosso site:\n\n"
            "https://www.cartomancias.com.br"
        )

    elif query.data == "whatsapp":
        await query.message.reply_text(
            "Perfeito! 😊\n\n"
            "Nosso WhatsApp:\n\n"
            "https://wa.me/5511937656368"
        )


def main():
    if not TOKEN:
        raise ValueError(
            "TOKEN não encontrado. Configure a variável TOKEN no Render."
        )

    app = Application.builder().token(TOKEN).build()

    # Bot normal
    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            mensagens
        )
    )

    # Telegram Business
    app.add_handler(
        MessageHandler(
            filters.UpdateType.BUSINESS_MESSAGE,
            mensagens_business
        )
    )

    # Botões
    app.add_handler(
        CallbackQueryHandler(botoes)
    )

    print("Bot iniciado com sucesso!")

    app.run_polling()


if __name__ == "__main__":
    main()
