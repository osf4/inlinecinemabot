from aiogram.filters.callback_data import CallbackData


class MovieCallback(CallbackData, prefix = 'mov'):
    movie_index: int


class RemoveDescriptionCallback(CallbackData, prefix = 'rem_mov'):
    pass