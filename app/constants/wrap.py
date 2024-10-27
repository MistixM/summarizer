# Links to social media, docs, groups, etc
FEATURES_LINK = "https://teletype.in/@mdevv/r1huS__Og1m"
SUPPORT_LINK = "https://t.me/+GVq4lXRADWM4MWRi"
USER_AGREEMENT_LINK = "https://teletype.in/@mdevv/cux9bGLs_vi"

# Menu buttons
SUBSCRIPTION_BUTTON = '⭐ Subscription'
FAQ_BUTTON = '❓ FAQ'
SUPPORT_BUTTON = '🤝 Get in Touch'
INSTALLATION_BUTTON = '⚙️ Installation'
POST_BUTTON = '📣 Post'
DEBUG_BUTTON = 'ℹ️ Debug'

# Bot settings
ADMIN = 1266917712
LOCAL_TEST = False
SUBSCRIPTION_PRICE = 320
SUBSCRIPTION_PRICE_DOLLAR = 4.99
ENCRYPTION_KEY = b'Rdai_1bI7z8_a6rmHKvqinVLpO88NKmjgHkFMf8g-ho='
VIP_FOLDER = 'vip_chats'

# Group messages
GROUP_START = f"✅ Hi everyone! Thanks for adding me here, I'm so happy to be part of your chat! 😊\n\nMy name's Summarizer. I'm here to help you to summarize messages in the chat, so you can understand what's going on here. Talk to each other and then use /sum [message limit] command to begin.\n\n🗂 <a href='{FEATURES_LINK}'>Read about my features and commands</a>\n<a href='{SUPPORT_LINK}'>📣 Support channel</a>"
NO_MESSAGE_SUMMARIZE = "👀 There's no message to summarize.. Let's talk!"
BOT_COOLDOWN = "🤔 Please wait some time before continuing"

# DM messages
DM_START = f"👨‍💻 Hey there! My name's Summarizer. I'm here to help you to summarize messages in the chat, so you can understand what's going on there.\n\n✅ To continue, please add me to the chat with admin rights. You can do this by using /install command or by hand.\n\n🗂 <a href='{FEATURES_LINK}'>Read about my features and commands</a>\n📣 <a href='{SUPPORT_LINK}'>Support channel</a>\n📑<a href='{USER_AGREEMENT_LINK}'> User Agreement</a>"
FOUR_O_FOUR = f"👀 Lost? Sorry, you cannot continue.\n\nContact: {SUPPORT_LINK}"
SUPPORT_MESSAGE = f"🤔 If you have any questions or problems, please do not hesitate to contact us!\n\nChat: {SUPPORT_LINK}"
INSTALLATION_MESSAGE = f"⚙️ To install the bot in your chat, use the button below. \n\n<b>IMPORTANT: Don't forget to give the bot admin rights to set it up properly. Otherwise it won't work!</b>"

# Subscription messages
SUBSCRIPTION_DESCRIPTION = f"⭐ <b>Make your chat more free with a monthly subscription!</b>\n\nThis subscription offers: \n- 1 minute cooldown, instead of 10 (<a href='https://teletype.in/@mdevv/r1huS__Og1m#k099:~:text=Why%20bot%20has,towards%20the%20bot'>about cooldowns</a>)\n- Message Memorize (<a href='https://teletype.in/@mdevv/cux9bGLs_vi#:~:text=13.%20Privacy%20and,such%20as%20OpenAI.'>about message storing</a>)\n\n👀 <b>And all for just {SUBSCRIPTION_PRICE} Stars ({SUBSCRIPTION_PRICE_DOLLAR}$)</b>"
SUBSCRIPTION_SUCCESS = "🥳 Congratulations! You're all set.\n\nVIP status will expire: "
SUBSCRIOTION_HAVE = "✅ You already have VIP status. Expiration date: "

# FAQ
FAQS = {
    "Why the bot is not responding?": "Sometimes the bot may not respond due to a problem on the server side. Please wait a while and try again later.",
    "Why bot has delay limitations?": "Bot restrictions have been added to prevent possible spam requests to the OpenAI API and harmful user behavior towards the bot.",
    "Does the bot remember all the messages in the chat?": "By default, no (they are reset after each server restart), but if you are a premium user, the bot will save all messages (read about saving messages <a href='https://teletype.in/@mdevv/cux9bGLs_vi#:~:text=13.%20Privacy%20and,such%20as%20OpenAI'>here</a>)",
    "My bot responds in incorrect language": f"Please describe your problem here: {SUPPORT_LINK}",
}