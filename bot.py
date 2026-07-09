import os
import logging

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

# --------------------------------------------------
# LOGS
# --------------------------------------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --------------------------------------------------
# TEXTO PADRÃO
# --------------------------------------------------
TEXTO_MENU = (
    "Oi amore, aqui é a assistente virtual do Cartomancias. 💜\n\n"
    "Por aqui não aceitamos consultas ainda, mas você pode nos chamar "
    "pelo nosso site ou pelo WhatsApp que vamos te atender rapidinho!\n\n"
    "Nosso horário de funcionamento é das 10:00 às 00:00 "
    "de segunda à sexta-feira."
)

# --------------------------------------------------
# MENU COM BOTÕES
# --------------------------------------------------
def menu_teclado() -> InlineKeyboardMarkup:
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

# --------------------------------------------------
# ENVIO DE MENU
# --------------------------------------------------
async def enviar_menu_chat(chat):
    """Envia o menu em chats normais do bot."""
    await chat.send_message(
        text=TEXTO_MENU,
        reply_markup=menu_teclado(),
    )

async def enviar_menu_business(update: Update):
    """Envia o menu em conversas Telegram Business."""
    if not update.business_message:
        logger.warning("Tentativa de enviar menu business sem update.business_message")
        return

    await update.business_message.reply_text(
        text=TEXTO_MENU,
        reply_markup=menu_teclado(),
    )

# --------------------------------------------------
# /START
# --------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        logger.info("START recebido: %s", update.to_dict())

        # Se por algum motivo /start vier em business, ignora aqui
        if update.business_message:
            logger.info("START ignorado porque veio como business_message.")
            return

        if update.effective_chat:
            await enviar_menu_chat(update.effective_chat)

    except Exception:
        logger.exception("Erro no handler /start")

# --------------------------------------------------
# MENSAGENS BUSINESS
# --------------------------------------------------
async def mensagens_business(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        logger.info("BUSINESS update recebido: %s", update.to_dict())

        if not update.business_message:
            logger.warning("Handler business chamado sem update.business_message")
            return

        # Evita loop caso o próprio bot apareça como remetente
        if (
            update.business_message.from_user
            and update.business_message.from_user.is_bot
        ):
            logger.info("Mensagem business enviada por bot; ignorando.")
            return

        await enviar_menu_business(update)

    except Exception:
        logger.exception("Erro no handler de mensagens business")

# --------------------------------------------------
# MENSAGENS NORMAIS DO BOT
# --------------------------------------------------
async def mensagens(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        logger.info("NORMAL update recebido: %s", update.to_dict())

        # Se for business, deixa o handler business cuidar disso
        if update.business_message:
            logger.info("Mensagem caiu no handler normal, mas era business. Ignorando.")
            return

        if update.effective_chat:
            await enviar_menu_chat(update.effective_chat)

    except Exception:
        logger.exception("Erro no handler de mensagens normais")

# --------------------------------------------------
# BOTÕES
# --------------------------------------------------
async def botoes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        if not query:
            return

        logger.info("Callback recebido: %s", update.to_dict())

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

    except Exception:
        logger.exception("Erro no handler de botões")

# --------------------------------------------------
# ERRO GLOBAL
# --------------------------------------------------
async def erro(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.exception("Erro global no bot. Update: %s", update, exc_info=context.error)

# --------------------------------------------------
# MAIN
# --------------------------------------------------
def main():
    if not TOKEN:
        raise ValueError("TOKEN não encontrado. Configure a variável TOKEN no Render.")

    app = Application.builder().token(TOKEN).build()

    # Comando /start
    app.add_handler(CommandHandler("start", start))

    # IMPORTANTE: handler business vem antes do normal
    app.add_handler(
        MessageHandler(
            filters.UpdateType.BUSINESS_MESSAGE,
            mensagens_business
        )
    )

    # Mensagens normais do bot
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            mensagens
        )
    )

    # Botões
    app.add_handler(CallbackQueryHandler(botoes))

    # Erro global
    app.add_error_handler(erro)

    logger.info("Bot iniciado com sucesso!")

    # Importante para receber updates Business
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
