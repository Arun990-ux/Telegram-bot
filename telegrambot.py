import nltk
print(nltk.data.path)
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize, sent_tokenize
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Ensure NLTK resources are downloaded
def download_nltk_resources():
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/wordnet')
        nltk.data.find('taggers/averaged_perceptron_tagger')
        nltk.data.find('corpora/omw-1.4')  # Check for OMW resource
    except LookupError:
        print("Downloading required NLTK resources...")
        nltk.download('punkt')
        nltk.download('wordnet')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('omw-1.4')  # Download OMW resource

# Download NLTK resources
download_nltk_resources()

# Your Telegram channel username (e.g., @YourChannelName)
CHANNEL_USERNAME = "@Arunbots"  # Replace with your channel username

# Function to check if a user is a member of the channel
async def is_user_member(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        print(f"User {user_id} status: {member.status}")  # Debugging
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"Error checking user membership: {e}")  # Debugging
        return False

# Start command with inline keyboard
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the /start command.
    """
    user_id = update.message.from_user.id
    print(f"User {user_id} started the bot.")  # Debugging

    # Check if the user is a member of the channel
    if await is_user_member(user_id, context):
        await update.message.reply_text(
            "Welcome! You're already a member of our channel. "
            "Send me any text, and I'll humanize it for you!"
        )
    else:
        # Show inline keyboard to join the channel
        keyboard = [
            [
                InlineKeyboardButton("Join Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")
            ],
            [
                InlineKeyboardButton("I Have Joined", callback_data="check_membership")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "👋 Welcome to the AI Humanizer Bot!\n\n"
            "To use this bot, please join our channel first. "
            "Click the button below to join, then come back and click 'I Have Joined'.",
            reply_markup=reply_markup
        )

# Callback query handler for "I Have Joined" button
async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the callback query from the inline keyboard.
    """
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()  # Acknowledge the callback query

    print(f"User {user_id} clicked 'I Have Joined'.")  # Debugging

    # Check if the user has joined the channel
    if await is_user_member(user_id, context):
        await query.edit_message_text(
            "Thank you for joining! 🎉\n\n"
            "Now you can send me any text, and I'll humanize it for you!"
        )
    else:
        # If the user hasn't joined, show the inline keyboard again
        keyboard = [
            [
                InlineKeyboardButton("Join Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")
            ],
            [
                InlineKeyboardButton("I Have Joined", callback_data="check_membership")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "❌ You haven't joined the channel yet. "
            "Please join the channel and click 'I Have Joined'.",
            reply_markup=reply_markup
        )

# Humanize text function
async def humanize_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle incoming messages and humanize the text.
    """
    user_id = update.message.from_user.id
    print(f"User {user_id} sent a message.")  # Debugging

    # Check if the user is a member of the channel
    if await is_user_member(user_id, context):
        user_text = update.message.text
        humanized_text = humanize_content(user_text)
        await update.message.reply_text(f"Humanized Text:\n{humanized_text}")
    else:
        # If the user hasn't joined, prompt them to join
        keyboard = [
            [
                InlineKeyboardButton("Join Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")
            ],
            [
                InlineKeyboardButton("I Have Joined", callback_data="check_membership")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "❌ You need to join our channel to use this bot. "
            "Please join the channel and click 'I Have Joined'.",
            reply_markup=reply_markup
        )

# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle errors.
    """
    print(f"Update {update} caused error {context.error}")

# Humanize content function (same as before)
def humanize_content(text):
    # Step 1: Simplify sentences
    text = simplify_sentence(text)

    # Step 2: Replace contractions
    text = replace_contractions(text)

    # Step 3: Replace complex words with simpler alternatives
    text = replace_with_simple_words(text)

    # Step 4: Replace words with simpler synonyms
    text = replace_with_synonyms(text)

    # Step 5: Remove repetitive phrases
    text = re.sub(r'\b(\w+)\b\s+\1\b', r'\1', text)

    return text

# Other helper functions (same as before)
def simplify_sentence(sentence):
    sentences = sent_tokenize(sentence)
    return " ".join(sentences)

def replace_contractions(text):
    contractions = {
        "cannot": "can't",
        "will not": "won't",
        "do not": "don't",
        "does not": "doesn't",
        "is not": "isn't",
        "are not": "aren't",
        "has not": "hasn't",
        "have not": "haven't",
        "had not": "hadn't",
        "would not": "wouldn't",
        "should not": "shouldn't",
        "could not": "couldn't",
        "it is": "it's",
        "I am": "I'm",
        "you are": "you're",
        "we are": "we're",
        "they are": "they're",
    }
    for formal, informal in contractions.items():
        text = text.replace(formal, informal)
    return text

def replace_with_simple_words(text):
    simple_words = {
        "revolutionizing": "changing",
        "enabling": "allowing",
        "personalized": "custom",
        "improved": "better",
        "efficiency": "productivity",
        "artificial intelligence": "AI",
        "diagnosis": "detection",
        "treatment": "care",
        "outcomes": "results",
        "reduce": "cut",
        "increase": "boost",
        "systems": "networks",
    }
    for complex_word, simple_word in simple_words.items():
        text = text.replace(complex_word, simple_word)
    return text

def replace_with_synonyms(text):
    words = word_tokenize(text)
    simplified_text = []
    for word in words:
        synonyms = wordnet.synsets(word)
        if synonyms:
            synonym = synonyms[0].lemmas()[0].name()
            if len(synonym) < len(word):
                simplified_text.append(synonym)
            else:
                simplified_text.append(word)
        else:
            simplified_text.append(word)
    return " ".join(simplified_text)

if __name__ == "__main__":
    # Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual bot token
    TOKEN = "7780854092:AAFV2r75EJ0T0krCPmdqtRL8hpjcSC4yqAk"

    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback_query))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, humanize_text))
    application.add_error_handler(error)

    # Start the bot
    print("Bot is running...")
    application.run_polling()
