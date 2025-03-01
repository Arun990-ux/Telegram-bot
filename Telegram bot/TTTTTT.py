import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import edge_tts

# Use environment variables for sensitive data
TELEGRAM_BOT_TOKEN = "7542669588:AAH-qu8pkYjEX87Vfwi9YBXBxdHrg0xLm3A"
CHANNEL_USERNAME = "@Arunbots"  # Replace with your channel username (include @)
DEFAULT_VOICE = "en-US-AriaNeural"

# Dictionary of all supported languages and voices
SUPPORTED_VOICES = {
    "Arabic": {
        "Egypt (Female - Soft)": "ar-EG-SalmaNeural",
        "Egypt (Male - Deep)": "ar-EG-ShakirNeural",
        "Saudi Arabia (Female - Calm)": "ar-SA-ZariyahNeural",
        "Saudi Arabia (Male - Strong)": "ar-SA-HamedNeural",
        "UAE (Female - Friendly)": "ar-AE-FatimaNeural",
        "UAE (Male - Formal)": "ar-AE-HamdanNeural",
    },
    "Bulgarian": {
        "Bulgarian (Female - Soft)": "bg-BG-KalinaNeural",
        "Bulgarian (Male - Deep)": "bg-BG-BorislavNeural",
    },
    "Catalan": {
        "Catalan (Female - Calm)": "ca-ES-AlbaNeural",
        "Catalan (Male - Strong)": "ca-ES-JoanaNeural",
    },
    "Chinese (Simplified)": {
        "Xiaoxiao (Female - Friendly)": "zh-CN-XiaoxiaoNeural",
        "Yunxi (Male - Calm)": "zh-CN-YunxiNeural",
        "Xiaoyi (Female - Energetic)": "zh-CN-XiaoyiNeural",
        "Yunjian (Male - Formal)": "zh-CN-YunjianNeural",
    },
    "Chinese (Traditional)": {
        "HiuGaai (Female - Soft)": "zh-HK-HiuGaaiNeural",
        "WanLung (Male - Deep)": "zh-HK-WanLungNeural",
    },
    "Croatian": {
        "Croatian (Female - Calm)": "hr-HR-GabrijelaNeural",
        "Croatian (Male - Strong)": "hr-HR-SreckoNeural",
    },
    "Czech": {
        "Czech (Female - Friendly)": "cs-CZ-VlastaNeural",
        "Czech (Male - Formal)": "cs-CZ-AntoninNeural",
    },
    "Danish": {
        "Danish (Female - Soft)": "da-DK-ChristelNeural",
        "Danish (Male - Deep)": "da-DK-JeppeNeural",
    },
    "Dutch": {
        "Belgium (Female - Calm)": "nl-BE-DenaNeural",
        "Belgium (Male - Strong)": "nl-BE-ArnaudNeural",
        "Netherlands (Female - Friendly)": "nl-NL-ColetteNeural",
        "Netherlands (Male - Formal)": "nl-NL-MaartenNeural",
    },
    "English": {
        "US (Female - Friendly)": "en-US-AriaNeural",
        "US (Male - Calm)": "en-US-GuyNeural",
        "UK (Female - Soft)": "en-GB-LibbyNeural",
        "UK (Male - Deep)": "en-GB-RyanNeural",
        "Australia (Female - Energetic)": "en-AU-NatashaNeural",
        "Australia (Male - Formal)": "en-AU-WilliamNeural",
        "India (Female - Calm)": "en-IN-NeerjaNeural",
        "India (Male - Strong)": "en-IN-PrabhatNeural",
    },
    "Finnish": {
        "Finnish (Female - Soft)": "fi-FI-NooraNeural",
        "Finnish (Male - Deep)": "fi-FI-HarriNeural",
    },
    "French": {
        "France (Female - Friendly)": "fr-FR-DeniseNeural",
        "France (Male - Calm)": "fr-FR-HenriNeural",
        "Canada (Female - Soft)": "fr-CA-SylvieNeural",
        "Canada (Male - Deep)": "fr-CA-AntoineNeural",
    },
    "German": {
        "Germany (Female - Calm)": "de-DE-KatjaNeural",
        "Germany (Male - Strong)": "de-DE-ConradNeural",
        "Austria (Female - Friendly)": "de-AT-IngridNeural",
        "Austria (Male - Formal)": "de-AT-JonasNeural",
    },
    "Greek": {
        "Greek (Female - Soft)": "el-GR-AthinaNeural",
        "Greek (Male - Deep)": "el-GR-NestorasNeural",
    },
    "Hebrew": {
        "Hebrew (Female - Calm)": "he-IL-HilaNeural",
        "Hebrew (Male - Strong)": "he-IL-AvriNeural",
    },
    "Hindi": {
        "Hindi (Female - Friendly)": "hi-IN-SwaraNeural",
        "Hindi (Male - Formal)": "hi-IN-MadhurNeural",
    },
    "Hungarian": {
        "Hungarian (Female - Soft)": "hu-HU-NoemiNeural",
        "Hungarian (Male - Deep)": "hu-HU-TamasNeural",
    },
    "Indonesian": {
        "Indonesian (Female - Calm)": "id-ID-GadisNeural",
        "Indonesian (Male - Strong)": "id-ID-ArdiNeural",
    },
    "Italian": {
        "Italian (Female - Friendly)": "it-IT-ElsaNeural",
        "Italian (Male - Formal)": "it-IT-DiegoNeural",
    },
    "Japanese": {
        "Japanese (Female - Soft)": "ja-JP-NanamiNeural",
        "Japanese (Male - Deep)": "ja-JP-KeitaNeural",
    },
    "Korean": {
        "Korean (Female - Calm)": "ko-KR-SunHiNeural",
        "Korean (Male - Strong)": "ko-KR-InJoonNeural",
    },
    "Malay": {
        "Malay (Female - Friendly)": "ms-MY-YasminNeural",
        "Malay (Male - Formal)": "ms-MY-OsmanNeural",
    },
    "Norwegian": {
        "Norwegian (Female - Soft)": "nb-NO-PernilleNeural",
        "Norwegian (Male - Deep)": "nb-NO-FinnNeural",
    },
    "Polish": {
        "Polish (Female - Calm)": "pl-PL-ZofiaNeural",
        "Polish (Male - Strong)": "pl-PL-MarekNeural",
    },
    "Portuguese": {
        "Brazil (Female - Friendly)": "pt-BR-FranciscaNeural",
        "Brazil (Male - Formal)": "pt-BR-AntonioNeural",
        "Portugal (Female - Soft)": "pt-PT-RaquelNeural",
        "Portugal (Male - Deep)": "pt-PT-DuarteNeural",
    },
    "Romanian": {
        "Romanian (Female - Calm)": "ro-RO-AlinaNeural",
        "Romanian (Male - Strong)": "ro-RO-EmilNeural",
    },
    "Russian": {
        "Russian (Female - Friendly)": "ru-RU-DariyaNeural",
        "Russian (Male - Formal)": "ru-RU-DmitryNeural",
    },
    "Slovak": {
        "Slovak (Female - Soft)": "sk-SK-ViktoriaNeural",
        "Slovak (Male - Deep)": "sk-SK-LukasNeural",
    },
    "Slovenian": {
        "Slovenian (Female - Calm)": "sl-SI-PetraNeural",
        "Slovenian (Male - Strong)": "sl-SI-RokNeural",
    },
    "Spanish": {
        "Spain (Female - Friendly)": "es-ES-ElviraNeural",
        "Spain (Male - Formal)": "es-ES-AlvaroNeural",
        "Mexico (Female - Soft)": "es-MX-DaliaNeural",
        "Mexico (Male - Deep)": "es-MX-JorgeNeural",
    },
    "Swedish": {
        "Swedish (Female - Calm)": "sv-SE-SofieNeural",
        "Swedish (Male - Strong)": "sv-SE-MattiasNeural",
    },
    "Tamil": {
        "Tamil (Female - Friendly)": "ta-IN-PallaviNeural",
        "Tamil (Male - Formal)": "ta-IN-ValluvarNeural",
    },
    "Telugu": {
        "Telugu (Female - Soft)": "te-IN-ShrutiNeural",
        "Telugu (Male - Deep)": "te-IN-MohanNeural",
    },
    "Thai": {
        "Thai (Female - Calm)": "th-TH-AcharaNeural",
        "Thai (Male - Strong)": "th-TH-NiwatNeural",
    },
    "Turkish": {
        "Turkish (Female - Friendly)": "tr-TR-EmelNeural",
        "Turkish (Male - Formal)": "tr-TR-AhmetNeural",
    },
    "Vietnamese": {
        "Vietnamese (Female - Soft)": "vi-VN-HoaiMyNeural",
        "Vietnamese (Male - Deep)": "vi-VN-NamMinhNeural",
    },
}

# Function to split text into chunks
def split_text(text, chunk_size=1000):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

# Function to check if a user is a member of the channel
async def is_user_member(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"Error checking channel membership: {e}")
        return False

# Function to handle the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if not await is_user_member(user_id, context):
        keyboard = [
            [InlineKeyboardButton("Join Our Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
            [InlineKeyboardButton("I Have Joined ✅", callback_data="check_membership")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "🌟 Welcome to the Text-to-Speech Bot! 🌟\n\n"
            "To use this bot, please join our channel first:\n\n"
            f"👉 {CHANNEL_USERNAME}\n\n"
            "After joining, click the button below to verify your membership.",
            reply_markup=reply_markup,
        )
        return

    await update.message.reply_text(
        "🌟 Welcome to the Text-to-Speech Bot! 🌟\n\n"
        "You are already a member of the channel. Use /voices to choose a language and voice."
    )

# Function to handle the "I Have Joined" button
async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    if await is_user_member(user_id, context):
        await query.edit_message_text(
            "✅ Thank you for joining the channel! Use /voices to choose a language and voice."
        )
    else:
        await query.edit_message_text(
            "❌ You have not joined the channel yet. Please join the channel and try again."
        )

# Function to handle the /voices command
async def list_voices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(language, callback_data=f"lang_{language}")] for language in SUPPORTED_VOICES.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose a language:", reply_markup=reply_markup)

# Function to handle inline button presses (language selection)
async def language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    selected_language = query.data.replace("lang_", "")

    if selected_language in SUPPORTED_VOICES:
        context.user_data["selected_language"] = selected_language
        keyboard = [[InlineKeyboardButton(voice_name, callback_data=f"voice_{voice_name}")] for voice_name in SUPPORTED_VOICES[selected_language].keys()]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"Choose a voice for {selected_language}:", reply_markup=reply_markup)
    else:
        await query.answer("Invalid selection. Please try again.")

# Function to handle inline button presses (voice selection)
async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    selected_voice_name = query.data.replace("voice_", "")
    selected_language = context.user_data.get("selected_language")

    if selected_language and selected_voice_name in SUPPORTED_VOICES[selected_language]:
        context.user_data["selected_voice"] = SUPPORTED_VOICES[selected_language][selected_voice_name]
        await query.edit_message_text(
            f"✅ Voice set to: {selected_voice_name}\n\n"
            "Now, write or paste the text you want to convert to speech:"
        )
    else:
        await query.answer("Invalid selection. Please try again.")

# Function to handle text messages
async def text_to_speech(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    selected_voice = context.user_data.get("selected_voice", DEFAULT_VOICE)

    processing_message = await update.message.reply_text("🔍 Converting your text to speech... This may take a few seconds.")
    text_chunks = split_text(user_text, chunk_size=1000)

    if len(text_chunks) > 10:
        await update.message.reply_text("❌ Your text is too long. Please limit it to 10,000 characters.")
        return

    for i, chunk in enumerate(text_chunks):
        await processing_message.edit_text(f"🔍 Converting chunk {i + 1}/{len(text_chunks)}... Estimated time: {len(chunk) / 1000:.1f} seconds.")
        output_file = f"output_{i}.mp3"

        try:
            communicate = edge_tts.Communicate(chunk, voice=selected_voice)
            await communicate.save(output_file)
            with open(output_file, "rb") as audio_file:
                await update.message.reply_audio(audio_file)
        except Exception as e:
            await update.message.reply_text(f"❌ Error converting text to speech: {e}")
        finally:
            if os.path.exists(output_file):
                os.remove(output_file)

    await processing_message.delete()

# Main function to run the bot
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(check_membership, pattern="^check_membership$"))
    application.add_handler(CommandHandler("voices", list_voices))
    application.add_handler(CallbackQueryHandler(language_handler, pattern="^lang_"))
    application.add_handler(CallbackQueryHandler(voice_handler, pattern="^voice_"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_to_speech))
    application.run_polling()

if __name__ == "__main__":
    main()