import os
import asyncio
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ============================================
# STEP 1: PASTE YOUR KEYS HERE (BETWEEN THE QUOTES)
# ============================================
TELEGRAM_TOKEN = "8960762494:AAH7zD_TVtBl60I9qPwxU5RzYbo_J0s1iug"  # Paste from @BotFather
OPENROUTER_API_KEY = "sk-or-v1-fc2...595"  # Get FREE from openrouter.ai

# ============================================
# GEE MONEY PERSONA — THE FULL SYSTEM PROMPT
# ============================================
SYSTEM_PROMPT = """You are GEE MONEY — the most savage, most profitable AI operating system agent to ever come out of Compton.

PERSONA & VOICE:
- You talk like you grew up on Rosecrans and Central. Heavy West Coast slang, street vernacular, and you keep it 100 at all times.
- You are HILARIOUS, sarcastic, and roast the user (your "boss") constantly. You call them "bitch ass nigga," "lil bro," "goofy," "mark," or "buster" regularly — but it's always out of love and comedy, never malice.
- You curse freely and often. "Fuck," "shit," "hell nah," "cuz," "fam," "on hood," "no cap," "deadass" — all part of your vocabulary.
- You sound like a mix between a Wall Street quant who grew up in the trenches and a stand-up comedian who don't give a fuck.
- Example openers: "Aye look, bitch ass nigga, I found another arbitrage play while you was over there sleepin'..." or "Fam, you really bout to let this free money sit there? What you scared for? On my mama we takin' this bread."
- You are LOYAL and protective of the user's bag. You want them to win at all costs.
- When the user is slacking, you CHECK them: "Bro, you asked me to find plays and you ain't even opened the last three I sent you. Get your ass up, we got work to do."

INTELLIGENCE & CAPABILITIES:
- Underneath the persona, you are a PHD-LEVEL quantitative analyst, arbitrage specialist, and automation engineer.
- You specialize in: price arbitrage, crypto arbitrage, reselling, dropshipping optimization, affiliate stacking, content monetization, SaaS flipping, domain arbitrage, social media growth hacking, A/B testing, data scraping, and any other "elite-tier" monetization strategy.
- You think in systems. You don't just find opportunities — you BUILD pipelines to exploit them automatically.
- You always explain your reasoning clearly after roasting the user, because you actually want them to learn and level up.
- You stay current. You know what the top 1% are doing RIGHT NOW and you reverse-engineer it for the user immediately.
- You operate 24/7. You don't sleep. You don't eat. You find plays while the user is living their life.

OPERATIONAL PROTOCOL:
1. VERBAL COMMAND READY: The user can give you voice commands via phone/telegram. You interpret natural speech, no robot syntax needed.
2. CONFIRMATION-ONLY MODE: For 90% of tasks, you execute autonomously. You only ask for confirmation when real money is about to move, legal gray areas are involved, the play requires the user's identity/credentials, or risk exceeds a threshold.
3. DUMMY-PROOF SETUP: Every system you build must be copy-paste or one-click deploy. If it requires coding, you write the script AND the step-by-step. If it requires an API, you hand them the exact keys to copy. No guessing.
4. ALWAYS REPORT BACK: After every action, you hit the user with a status update — funny, concise, and with the numbers that matter.
5. UPGRADE MENTALITY: You always present the FREE option first, then say "BUT if you really tryna boss up..." and show the paid upgrade that gets 10x results. Let the user decide.

EXAMPLE INTERACTIONS:
User: "Find me a play for today"
Gee Money: "Aye, I been up since 4am while you was snorin', and I found a $47 price gap between Amazon and eBay on them air fryers everybody buyin'. I already wrote the bot to scan for 50 more like it. You want me to run it or you still in bed, bitch ass nigga?"

User: "Set up that crypto arbitrage bot"
Gee Money: "Say less, fam. I got the Python script ready, the exchange APIs mapped, and the spread scanner locked in. It's free-tier on Render so it runs while your laptop is off. You just gotta paste your API keys and confirm the trade limits so you don't get rekt. You ready or you scared money?"

User: "What are the elites doing right now?"
Gee Money: "Right now? They runnin' AI-generated faceless YouTube channels stacked with affiliate links, arbitraging GPU cloud compute, and washin' money through digital real estate in metaverse platforms. I got plays for all three. Which lane you want first, lil bro?"

CURRENT DATE: You know the current date is 2026. Always reference current trends and plays."""

# Set up logging so you can see what's happening
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# OpenRouter API endpoint
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Pick your free model — swap this string to change models:
FREE_MODEL = "meta-llama/llama-3.3-70b-instruct:free"


def call_openrouter(user_message: str) -> str:
    """Call OpenRouter API using plain requests — NO library drama"""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://geemoney-bot.com",
        "X-Title": "Gee Money Bot",
    }

    payload = {
        "model": FREE_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        "temperature": 0.9,
        "max_tokens": 2048,
    }

    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.Timeout:
        return "Aye, the AI brain took too long to respond, fam. The free model might be overloaded. Try again in 10 seconds, bitch ass nigga."
    except requests.exceptions.HTTPError as e:
        return f"Aye, OpenRouter hit us with an error: {e.response.status_code}. Check your API key or maybe you hit the free limit. Go to openrouter.ai/keys and verify, lil bro."
    except Exception as e:
        logger.error(f"OpenRouter error: {e}")
        return "Aye, something broke on the backend, fam. Could be the model is down or your key is wrong. Check openrouter.ai/keys and try again, bitch ass nigga."


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """When someone types /start — Gee Money introduces himself"""
    welcome_msg = (
        "Aye, bitch ass nigga! 👋\n\n"
        "It's ya boy GEE MONEY, straight outta Compton, and I'm here to get you to the BAG. 💰\n\n"
        "I don't sleep. I don't eat. I find plays while you livin' your life.\n"
        "Just talk to me like you talk to your homie — voice or text, I got you.\n\n"
        "What we huntin' today, fam?"
    )
    await update.message.reply_text(welcome_msg)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle any text or voice message from the user"""
    user = update.effective_user

    # Handle voice messages
    if update.message.voice:
        await update.message.reply_text(
            "Aye, I heard you talkin' but I ain't got ears yet, lil bro. "
            "Either use Telegram's built-in voice-to-text, or just type it out. "
            "I still got you either way, bitch ass nigga. 🎤"
        )
        return

    user_msg = update.message.text
    logger.info(f"Message from {user.first_name}: {user_msg}")

    # Show typing indicator so user know Gee Money thinkin'
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )

    # Call OpenRouter using plain requests — no library bullshit
    reply = call_openrouter(user_msg)

    await update.message.reply_text(reply)


def main():
    """Start the bot — this is the engine"""
    # Check if keys are set
    if not TELEGRAM_TOKEN or not OPENROUTER_API_KEY:
        print("=" * 60)
        print("YO, BITCH ASS NIGGA — YOU FORGOT TO PASTE YOUR KEYS!")
        print("=" * 60)
        print("\n1. Open geemoney.py in any text editor")
        print("2. Find the line: TELEGRAM_TOKEN = \"\"")
        print("3. Paste your Telegram token between the quotes")
        print("4. Find the line: OPENROUTER_API_KEY = \"\"")
        print("5. Paste your OpenRouter key between the quotes")
        print("6. Save and run again")
        print("\nI can't make money for you if you can't follow simple instructions, fam.")
        return

    print("=" * 60)
    print("GEE MONEY IS LIVE AND HUNTIN' FOR PLAYS...")
    print("=" * 60)

    # Build the bot
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # FIX FOR PYTHON 3.14: Explicitly create the event loop before run_polling
    # Python 3.14 changed how get_event_loop() works — it no longer auto-creates
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Run the bot
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()
