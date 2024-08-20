from enum import StrEnum


class BotTexts(StrEnum):
    greeting_message = """
👋🏻 Привет, {username}!

🧑‍💻 Этот бот создан для того, чтобы прямо в Телеграме 
получать данные о фильмах, которые идут в Бендерах

/movies - чтобы получить список фильмов, которые идут в данный момент в кинотеатре.

Напиши @bencinembot в любом чате, чтобы получить список фильмов, не открывая бота напрямую
"""

    movie_descrption = """
**{title}**

Сеансы: {sessions}
Формат:{format}
Продолжительность:{duration}

{description}
"""