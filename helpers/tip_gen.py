from datetime import datetime, timezone
import math
from random import choice
from typing import Optional, List

from mongo import Database

from models.users import User, UserTip
from helpers.rules import get_rule_level_by_level


def calc_score(
    expavg_score: float,
    cpus: int,
    registration_time: datetime,
):
    """Calculate the score."""
    def sigmoid(x: float) -> float:
        return 1 / (1 + math.exp(-x))

    delta_t = (
        datetime.now(timezone.utc) - registration_time
    ).total_seconds() / (3600 * 24)

    return 50 * (cpus + 1) * sigmoid(0.01 * (delta_t + expavg_score))


def _ask_model(model, tokenizer, query):
    encoded_prompt = tokenizer.encode(
        query,
        add_special_tokens=False,
        return_tensors='pt'
    )
    output_sequences = model.generate(
        input_ids=encoded_prompt,
        max_length=40,
        top_k=5,
        top_p=0.95,
        do_sample=True,

    )
    if len(output_sequences.shape) > 2:
        output_sequences.squeeze_()
    text = tokenizer.decode(
        output_sequences[0],
        clean_up_tokenization_spaces=True
    )
    return str(text)


def _tip_gen_mot(db: Database, user: User) -> str:
    """Фразы-мотиваторы."""
    tips = [
        "сейчас бы решить какую-нибудь задачку!",
        "давно не занимались!"
    ]
    return choice(tips).capitalize()


def _tip_gen_prj(db: Database, user: User) -> str:
    """Выдержки из описания проекта."""
    total_users = db[User.__colname__].count({})
    tips = [
        f"а вы знали, что у нас уже {total_users} пользователей?"
    ]
    return choice(tips).capitalize()


def _tip_gen_lab(db: Database, user: User) -> str:
    tips = [
        "так хочется ещё одну колбу...",
        "скорее бы уже микроскоп..."
    ]
    return choice(tips).capitalize()


def _tip_gen_avatar(db: Database, user: User) -> str:
    """Фразы научного-сотрудника."""
    tips = [
        "хочу селекционировать новый вид хищных растений.",
        "надо бы доказать теорему."
    ]
    return choice(tips).capitalize()


def _tip_gen_general(db: Database, user: User) -> str:
    """Фразы научного-сотрудника."""
    tips = [
        "здравствуй!",
        "рад тебя видеть!",
        "погода сегодня очень подходит для научных свершений!"
    ]
    return choice(tips).capitalize()


def _tip_gen_astrology(db: Database, user: User) -> str:
    """Фразы астрологизмы."""
    tips = [
        "Хмм отрицательная производная в фазе меркурия"
        ", видимо, он ретроградный..."
    ]
    return choice(tips).capitalize()


def _tip_gen_lvl(db: Database, user: User) -> str:
    tip = "<b>Совет дня:</b> не програмируйте на PHP"
    next_level = get_rule_level_by_level(db, user.level + 1)
    if next_level:
        left = next_level.exp_gte - user.total_exp
        tip = (
            f"<b>Совет дня:</b> до следующего уровня осталось всего {left}"
            " очков!"
        )
    return tip


TIPS_HELLO = [
    "general",
]

TIPS_LAZY = [
    "mot",
    "lab",
    "avatar",
    "astrology",
]

TIPS_BUSY = [
    "mot",
    "avatar",
    "astrology",
]

TIP_GENS = {
    "general": _tip_gen_general,
    "mot": _tip_gen_mot,
    "lab": _tip_gen_lab,
    "avatar": _tip_gen_avatar,
    "astrology": _tip_gen_astrology,
    # "lvl": _tip_gen_lvl,
    # "prj": _tip_gen_prj,
}


def tip_gen(
    db: Database,
    user: User,
    expavg_score: float,
    model,
    tokenizer
) -> UserTip:
    now = datetime.now(timezone.utc)
    onl = user.last_online
    if now.date() != onl.date():
        return UserTip(
            text=_ask_model(
                model,
                tokenizer,
                TIP_GENS[choice(TIPS_HELLO)](db, user)
            )
        )
    if expavg_score > 0.5:
        return UserTip(
            text=_ask_model(
                model,
                tokenizer,
                TIP_GENS[choice(TIPS_BUSY)](db, user)
            )
        )

    text: str = _ask_model(
        model,
        tokenizer,
        TIP_GENS[choice(TIPS_LAZY)](db, user)
    )
    for _ in range(10):
        text = text.replace("\n\n\n", "\n\n")
    text = text.strip()

    text = text\
        .split("0")[0]\
        .split("1")[0]\
        .split("2")[0]\
        .split("3")[0]\
        .split("4")[0]\
        .split("5")[0]\
        .split("6")[0]\
        .split("7")[0]\
        .split("8")[0]\
        .split("9")[0]

    text = ".".join(text.split(".")[:-1])
    if len(text.split("\n")) > 2:
        text = "\n".join(text.split("\n")[:-1])

    text = "<i>" + text.replace("\n", "<br>") + "</i>"

    return UserTip(
        text=text
    )
