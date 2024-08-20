from aiogram import Router
from aiogram.types import (InlineQuery, InlineQueryResultArticle,
                           InputTextMessageContent, LinkPreviewOptions)

from aiogram.enums.parse_mode import ParseMode

from models.movie import Movie
from movies_cacher.default_cacher import DefaultMoviesCacher

router = Router()

@router.inline_query()
async def inline_query_handler(inline_query: InlineQuery,
                               cacher: DefaultMoviesCacher):
    
    movies = await cacher.get_movies()
    
    articles = [
        InlineQueryResultArticle(
            id = movie.title,
            title = movie.title,
            description =  __format_tiny_movie_description(movie),
            thumbnail_url = movie.preview_url,
            input_message_content = InputTextMessageContent(
                message_text = __format_full_movie_description(movie),
                parse_mode = ParseMode.MARKDOWN,
                link_preview_options = LinkPreviewOptions(show_above_text = True,
                                                          prefer_large_media = True),
                disable_web_page_preview = False,
            ),
        ) for movie in movies
    ]
    
    await inline_query.answer(articles, is_personal = True)


def __format_tiny_movie_description(movie: Movie) -> str:
    '14.30, 16.30, 3D, 89 min / 1.30 hour'
    return f'{movie.sessions}\n{movie.format} {movie.duration}'


def __format_full_movie_description(movie: Movie) -> str:
    return f"""
[{movie.title}]({movie.preview_url})

Формат: *{movie.format}*
Продолжительность: *{movie.duration}*

{movie.description}
"""