from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton,
                           InlineKeyboardButton,
                           InlineKeyboardMarkup)
from db.queries import SELECT_USER_TASKS

keybord_main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="/add"), KeyboardButton(text="/tasks")],
    [KeyboardButton(text="/done"), KeyboardButton(text="/delete")],
    [KeyboardButton(text="/stats")]
    ]
)


inline = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text="Сделано", callback_data="task_done"),
                InlineKeyboardButton(text="Назад", callback_data="task_back")
            ]
        ]
    )