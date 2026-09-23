from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from src.keyboards import keybord_main, inline
from db.tasks import create_task, mark_task_as_done, get_user_tasks, delete_task, get_tasks_stats
from db.users import register_user


router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    user = message.from_user
    username = user.username
    register_user(username, user.id)
    
    await message.answer(
        f"Привет, {user.first_name}!\n"
        "Я твой бот-менеджер задач.\n"
        "Используй кнопки ниже для управления:",
        reply_markup=keybord_main
    )

class TaskStates(StatesGroup):
    waiting_for_task_title = State()
    waiting_for_task_id_done = State()
    waiting_for_task_id_delete = State()

@router.message(Command("add"))
async def cmd_add(message: Message, state: FSMContext):
    await state.set_state(TaskStates.waiting_for_task_title)
    await message.answer("Введи название новой задачи:")

@router.message(TaskStates.waiting_for_task_title)
async def process_task_title(message: Message, state: FSMContext):
    title = message.text
    user_id = message.from_user.id
    
    create_task(user_id, title)
    await state.clear()
    await message.answer(f"Задача «{title}» успешно добавлена!", reply_markup=keybord_main)


@router.message(Command("tasks"))
async def cmd_tasks(message: Message):
    user_id = message.from_user.id
    tasks = get_user_tasks(user_id)    
    if not tasks:
        await message.answer("У тебя пока нет задач. Используй /add, чтобы добавить.", reply_markup=keybord_main)
        return

    text = " Твои задачи:  \n\n"
    for index, task in enumerate(tasks, start=1):
        # Поддержка словарей, которые возвращает get_user_tasks
        title = task["title"]
        is_done = task["is_done"]
        status_name = "Выполнена" if is_done else "Не выполнена"
        text += f"{index}. {status_name} — {title}\n"

    text += "\nВведи команду /done, чтобы отметить задачу по номеру."
    await message.answer(text, reply_markup=keybord_main)


@router.callback_query(F.data.startswith("task_done_"))
async def process_task_done_callback(callback: CallbackQuery):
    task_id = int(callback.data.split("_")[2])
    user_id = callback.from_user.id

    mark_task_as_done(task_id, user_id)
    await callback.answer("Задача отмечена как выполненная!", show_alert=True)
    await callback.message.edit_text("Задача успешно выполнена!", reply_markup=None)

@router.callback_query(F.data == "task_back")
async def process_task_back_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Вы вернулись назад. Отправьте /tasks для просмотра списка.")


@router.message(Command("done"))
async def cmd_done_start(message: Message, state: FSMContext):
    await state.set_state(TaskStates.waiting_for_task_id_done)
    await message.answer("Введи номер задачи, которую нужно отметить как выполненную:")


@router.message(TaskStates.waiting_for_task_id_done)
async def process_done_id(message: Message, state: FSMContext):
    user_id = message.from_user.id
    
    if not message.text.isdigit():
        await message.answer("Пожалуйста введи число (номер задачи).")
        return

    tasks = get_user_tasks(user_id)
    index = int(message.text)
    
    if index < 1 or index > len(tasks):
        await message.answer("Ошибка: задача с таким номером не найдена.", reply_markup=keybord_main)
        await state.clear()
        return

    task_id = tasks[index - 1]["id"]

    mark_task_as_done(task_id, user_id)
    await state.clear()
    await message.answer(f"Задача №{index} отмечена как выполненная!", reply_markup=keybord_main)


@router.message(Command("delete"))
async def cmd_delete(message: Message, state: FSMContext):
    await state.set_state(TaskStates.waiting_for_task_id_delete)
    await message.answer("Введи номер задачи, которую нужно удалить:")


@router.message(TaskStates.waiting_for_task_id_delete)
async def process_delete_id(message: Message, state: FSMContext):
    user_id = message.from_user.id
    
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введи число.")
        return

    tasks = get_user_tasks(user_id)
    index = int(message.text)

    if index < 1 or index > len(tasks):
        await message.answer("Ошибка: задача с таким номером не найдена.", reply_markup=keybord_main)
        await state.clear()
        return

    task_id = tasks[index - 1]["id"]

    delete_task(task_id, user_id)
    await state.clear()
    await message.answer(f"Задача №{index} успешно удалена.", reply_markup=keybord_main)


@router.message(Command("stats"))
async def cmd_stats(message: Message):
    user_id = message.from_user.id
    stats = get_tasks_stats(user_id)
    
    # Обработка в зависимости от формата возврата stats (словарь или список)
    if isinstance(stats, list):
        stats = stats[0]

    await message.answer(
        f"📊 **Твоя статистика:**\n\n"
        f"📌 Всего задач: {stats.get('total', 0)}\n"
        f"✅ Выполнено: {stats.get('completed', 0)}\n"
        f"⬜ Не выполнено: {stats.get('uncompleted', 0)}",
        reply_markup=keybord_main,
    )