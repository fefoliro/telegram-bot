```python
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


async def mostrar_menu(chat, responder=False):
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

    texto = (
        "Oi amore, aqui é a assistente virtual do Cartomancias. 💜\n\n"
        "Por aqui não aceitamos consultas ainda, mas você pode nos chamar "
        "pelo nosso site ou pelo WhatsApp que vamos te atender rapidinho!\n\n"
        "Nosso horário de funcionamento é das 10:00 às 00:00 "
        "de segunda à sexta-feira."
    )

    if responder:
        await chat.reply_text(
            text=texto,
            reply_markup=InlineKeyboardMarkup(teclado),
        )
    else:
        await chat.send_message(
            text=texto,
            reply_markup=InlineKeyboardMarkup(teclado),
        )


# Mensagem enviada diretamente para o bot
async def mensagens(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await mostrar_menu(update.effective_chat, responder=True)


# Mensagem recebida pela conta Telegram Business conectada
async def mensagens_business(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.business_message:
        await update.business_message.reply_text(
            "Oi amore, aqui é a assistente virtual do Cartomancias. 💜\n\n"
            "Vou te ajudar com o atendimento. Escolha uma opção abaixo:",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🌐 Site",
                            callback_data="site"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "💬 WhatsApp",
                            callback_data="whatsapp"
                        )
                    ],
                ]
            ),
        )


# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await mostrar_menu(update.effective_chat, responder=False)


# Botões
async def botoes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "site":
        await query.message.reply_text(
            "Perfeito! 😊\n\n"
            "É só clicar no link abaixo e entrar em contato pelo chat:\n\n"
            "https://www.cartomancias.com.br"
        )

    elif query.data == "whatsapp":
        await query.message.reply_text(
            "Perfeito! 😊\n\n"
            "Chame pelo WhatsApp para realizar sua consulta:\n\n"
            "https://wa.me/5511937656368"
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


print("Bot iniciado...")

app.run_polling()
```
