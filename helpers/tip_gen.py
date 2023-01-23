from datetime import datetime
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
        datetime.utcnow() - registration_time
    ).total_seconds() / 3600

    return 50 * (cpus + 1) * sigmoid(0.5 * delta_t + expavg_score)


def _ask_model(model, tokenizer, query):
    encoded_prompt = tokenizer.encode(
        query,
        add_special_tokens=False,
        return_tensors='pt'
    )
    output_sequences = model.generate(
        input_ids=encoded_prompt,
        max_length=20,
        top_k=5,
        top_p=0.95,
        do_sample=True
    )
    if len(output_sequences.shape) > 2:
        output_sequences.squeeze_()
    text = tokenizer.decode(
        output_sequences[0],
        clean_up_tokenization_spaces=True
    )
    return "<i>" + str(text).replace("\n", "<br>") + "</i>"


def _tip_gen_mot(db: Database, user: User) -> str:
    """Фразы-мотиваторы."""
    tips = [
        "сейчас бы решить какую-нибудь задачку",
        "давно не занимались"
    ]
    return choice(tips).capitalize()


def _tip_gen_prj(db: Database, user: User) -> str:
    """Выдержки из описания проекта."""
    total_users = db[User.__colname__].count()
    tips = [
        f"а вы знали, что у нас уже {total_users} пользователей?"
    ]
    return choice(tips).capitalize()


def _tip_gen_lab(db: Database, user: User) -> str:
    tips = [
        "так хочется ещё одну колбу",
        "скорее бы уже микроскоп"
    ]
    return choice(tips).capitalize()


def _tip_gen_avatar(db: Database, user: User) -> str:
    """Фразы научного-сотрудника."""
    tips = [
        "хочу селекционировать новый вид хищных растений",
        "надо бы доказать теорему"
    ]
    return choice(tips).capitalize()


def _tip_gen_general(db: Database, user: User) -> str:
    """Фразы научного-сотрудника."""
    tips = [
        "здравствуй!",
        "рад тебя видеть",
        "погода сегодня очень подходит для научных свершений"
    ]
    return choice(tips).capitalize()


def _tip_gen_astrology(db: Database, user: User) -> str:
    """Фразы астрологизмы."""
    tips = [
        "Хмм отрицательная производная в фазе меркурия"
        ", видимо, он ретроградный"
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


TIP_GENS = {
    "lvl": _tip_gen_lvl,
    "mot": _tip_gen_mot,
    "prj": _tip_gen_prj,
    "lab": _tip_gen_lab,
    "avatar": _tip_gen_avatar,
    "general": _tip_gen_general,
    "astrology": _tip_gen_astrology,
}


def tip_gen(
    db: Database,
    user: User,
    model,
    tokenizer
) -> UserTip:
    return UserTip(
        text=_ask_model(
            model,
            tokenizer,
            TIP_GENS[choice(list(TIP_GENS.keys()))](db, user)
        )
    )
