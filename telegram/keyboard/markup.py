from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from models.movie import Movie
from .callbacks import MovieCallback, RemoveDescriptionCallback


remove_description_button = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(
            text = 'Убрать',
            callback_data = RemoveDescriptionCallback().pack()
            ),
        ],
    ]
)


def movies_markup(movies: list[Movie]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    for i, movie in enumerate(movies):
        kb.row(
            InlineKeyboardButton(
                text = movie.title,
                callback_data = MovieCallback(movie_index = i).pack()
            )
        )

    return kb.as_markup()