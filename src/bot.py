import db
from config import TOKEN, get_message
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    original = message.reply_to_message

    target = original.from_user
    uid = target.id

    if not db.exists(uid):
        await update.message.reply_text(get_message("not-verified"))
        return

    value = db.get(uid)
    message = get_message("user-verified").format(value)
    await update.message.reply_text(message)

async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    uid = message.from_user.id

    if not db.is_authorized(uid):
        return
    
    args = context.args
    if args is None:
        await message.reply_text(get_message("reason-required"))
        return
        
    target_uid = message.reply_to_message.from_user.id
    value = " ".join(args)
        
    db.update(target_uid, value)

    msg = get_message("verified").format(target_uid, value)
    await message.reply_text(msg)

# revoke verified
async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    uid = message.from_user.id

    if not db.is_authorized(uid):
        return
    
    target_uid = message.reply_to_message.from_user.id
    db.clear(target_uid)

    msg = get_message("cleared").format(uid)
    await message.reply_text(msg)

async def authorize(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    chat_id = message.chat_id
    uid = message.from_user.id

    chat_member = await context.bot.get_chat_member(chat_id, uid)
    if chat_member.status not in ["administrator", "creator"]:
        return
    
    target_uid = message.reply_to_message.from_user.id
    db.authorize(target_uid)

    msg = get_message("authorized").format(uid)
    await message.reply_text(msg)

async def revoke(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    chat_id = message.chat_id
    uid = message.from_user.id

    chat_member = await context.bot.get_chat_member(chat_id, uid)
    if chat_member.status not in ["administrator", "creator"]:
        return
    
    target_uid = message.reply_to_message.from_user.id
    db.revoke(target_uid)

    msg = get_message("revoked").format(uid)
    await message.reply_text(msg)

bot = ApplicationBuilder().token(TOKEN).build()

# check whether a user is verified or not
bot.add_handler(CommandHandler("status", status))
# verify a user (user must be authorized)
bot.add_handler(CommandHandler("verify", verify))
# clear a user of verifications
bot.add_handler(CommandHandler("clear", clear))
# authorize a user to verify (requires admin)
bot.add_handler(CommandHandler("authorize", authorize))
# revoke a user's ability to verify (requires admin)
bot.add_handler(CommandHandler("revoke", revoke))

bot.run_polling()

