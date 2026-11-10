import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from config import BOT_TOKEN, ADMIN_IDS, validate_config

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user is None or update.message is None:
        return

    role = "Administrator" if is_admin(user.id) else "Member"
    await update.message.reply_text(
        "👋 Welcome to OLA Trading Signals!\n\n"
        f"Account type: {role}\n\n"
        "This bot is currently being set up. Signal features will be added "
        "in later development stages.\n\n"
        "Use /help to see available commands."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return
    await update.message.reply_text(
        "📚 OLA Trading Signals — Help\n\n"
        "/start — Start the bot\n"
        "/help — Show this help message\n"
        "/status — Check whether the bot is running\n\n"
        "Trading signals are not active yet. Please do not make trades "
        "based on this setup bot."
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return
    user = update.effective_user
    role = "Administrator" if user and is_admin(user.id) else "Member"
    await update.message.reply_text(
        "🟢 OLA Trading Signals is online.\n"
        f"Your account: {role}\n"
        "Current stage: 1 — Foundation\n"
        "Signal engine: Not active yet"
    )


async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return
    user = update.effective_user
    if user is None or not is_admin(user.id):
        await update.message.reply_text("⛔ This command is for administrators only.")
        return
    await update.message.reply_text(
        "🔐 Admin access confirmed.\n\n"
        "The full admin dashboard will be added in a later stage."
    )


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return
    await update.message.reply_text("I don't recognize that command. Send /help.")


async def post_init(application: Application) -> None:
    me = await application.bot.get_me()
    logger.info("Bot started successfully as @%s", me.username)


def main() -> None:
    validate_config()
    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("admin", admin))
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    logger.info("Starting OLA Trading Signals bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
