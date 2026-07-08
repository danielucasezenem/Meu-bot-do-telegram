from telegram import Update
from telegram.ext import ContextTypes

async def executar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return

    await update.message.reply_text(
        "👋 Olá! Seja bem-vindo ao bot!\n\n"
        "Use /help para ver todos os comandos."
    )