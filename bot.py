import telebot
import re

TOKEN = "8254386547:AAH_IZvLCcZ-5Z_fKt8EDvphWswoi9EjDbI"
bot = telebot.TeleBot(TOKEN)

MCI = 4325  # 1 МРП на 2026 год


# ---------------- VALIDATION ----------------

def is_valid_plate(text):
    text = text.lower().strip()

    # формат 232abu04
    pattern = r"^[0-9]{3}[a-z]{3}[0-9]{2}$"
    if not re.match(pattern, text):
        return False

    digits = text[:3]
    region = int(text[6:8])

    # запрещаем 000
    if digits == "000":
        return False

    # регионы 01–20
    if region < 1 or region > 20:
        return False

    return True


# ---------------- PRICE LOGIC ----------------

def is_same_letters(letters):
    return letters[0] == letters[1] == letters[2]


def calculate_price(number):
    number = number.upper().replace(" ", "")

    digits = number[0:3]
    letters = number[3:6]

    d = int(digits)
    same_letters = is_same_letters(letters)

    special_010 = [10,20,30,40,50,60,70,77,80,90,707]

    aba = [
        101,121,131,141,151,161,171,181,191,
        202,212,232,242,252,262,272,282,292,
        303,313,323,343,353,363,373,383,393,
        404,414,424,434,454,464,474,484,494,
        505,515,525,535,545,565,575,585,595,
        606,616,626,636,646,656,676,686,696,
        717,727,737,747,757,767,787,797,
        808,818,828,838,848,858,868,878,898,
        909,919,929,939,949,959,969,979,989
    ]

    extreme = [1,2,3,4,5,6,7,8,9,777]
    hundreds = [100,111,200,222,300,333,400,444,500,555,600,666,700,800,888,900,999]

    # 🔥 Самые дорогие
    if d in extreme and same_letters:
        return 285 * MCI
    if d in extreme:
        return 228 * MCI

    if d in hundreds and same_letters:
        return 194 * MCI
    if d in hundreds:
        return 137 * MCI

    if d in special_010 and same_letters:
        return 114 * MCI
    if d in special_010:
        return 57 * MCI

    if d in aba and same_letters:
        return 72 * MCI
    if d in aba:
        return 15 * MCI

    if same_letters:
        return 57 * MCI

    return 10 * MCI


# ---------------- TELEGRAM ----------------

@bot.message_handler(commands=["start"])
def start(msg):
    bot.send_message(
        msg.chat.id,
        "🚗 Отправь госномер в формате:\n\n232abu04\n\nЯ покажу его стоимость."
    )


@bot.message_handler(func=lambda m: True)
def handle(msg):
    text = msg.text.lower().replace(" ", "")

    if not is_valid_plate(text):
        bot.send_message(
            msg.chat.id,
            "❌ Неверный формат\n\nПример: 111xxx01\n• 3 цифры (не 000)\n• 3 буквы\n• регион 01–20"
        )
        return

    price = calculate_price(text)

    bot.send_message(
        msg.chat.id,
        f"🚘 Номер: {text.upper()}\n💰 Стоимость: {price:,} ₸"
    )


bot.infinity_polling()
