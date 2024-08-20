from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, URLInputFile

from movies_cacher.base_cacher import BaseMoviesCacher

from .keyboard.markup import movies_markup, remove_description_button
from .keyboard.callbacks import MovieCallback, RemoveDescriptionCallback
from .texts import BotTexts

router = Router(name = __name__)


@router.message(CommandStart())
async def handle_start(msg: Message):
    await msg.answer(BotTexts.greeting_message.format(
        username = msg.from_user.first_name,
    ))


@router.message(Command('movies'))
async def handle_movies(msg: Message, cacher: BaseMoviesCacher):
    movies = await cacher.get_movies()

    await msg.answer('В городе Бендеры на текущий момент идут следующие фильмы:',
                     reply_markup = movies_markup(movies))
    

@router.callback_query(MovieCallback.filter())
async def handle_movie_callback(query: CallbackQuery, 
                                callback_data: MovieCallback,
                                cacher: BaseMoviesCacher):
    
    movie = await cacher.get_movie_by_index(callback_data.movie_index)

    preview = URLInputFile(movie.preview_url)
    await query.message.answer_photo(
        photo = preview,
        caption = BotTexts.movie_descrption.format(
            title = movie.title,
            sessions = movie.sessions,
            format = movie.format,
            duration = movie.duration,
            description = movie.description,
        ),

        reply_markup = remove_description_button,
    )


@router.callback_query(RemoveDescriptionCallback.filter())
async def handle_remove_description(query: CallbackQuery):
    await query.message.delete()