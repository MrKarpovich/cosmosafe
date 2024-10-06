import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware

# Токен вашего бота
API_TOKEN = '8045308638:AAF6hsOSj2A6kl1QwjY4umj-8ltq_Q_GW4g'

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Пример базы данных ингредиентов (можно заменить на подключение к реальной БД)
ingredient_data = {
    "Water": {"safety": "Безопасно", "comment": "Основной компонент большинства продуктов."},
    "Glycerin": {"safety": "Безопасно", "comment": "Увлажняющий агент, подходит для всех типов кожи."},
    "Fragrance": {"safety": "Осторожно", "comment": "Может вызвать аллергию или раздражение у чувствительной кожи."},
    "Dimethicone": {"safety": "Безопасно", "comment": "Часто используется как увлажнитель, безопасен в нормальных концентрациях."},
    "Paraben": {"safety": "Опасно", "comment": "Связан с возможными рисками для здоровья при длительном использовании."}
}

# Обработчик для команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправь мне состав косметики, и я подскажу, насколько он безопасен.")

# Обработчик для анализа состава
@dp.message_handler()
async def analyze_ingredients(message: types.Message):
    # Разделяем строку с ингредиентами на отдельные компоненты и приводим к нижнему регистру
    ingredients = [ingredient.strip().lower() for ingredient in message.text.split(",")]

    response = "Вот информация по каждому ингредиенту:\n\n"

    for ingredient in ingredients:
        # Поиск ингредиента в базе данных (также приводим ключи к нижнему регистру)
        data = ingredient_data.get(ingredient.capitalize())
        if data:
            safety = data["safety"]
            comment = data["comment"]
            response += f"**{ingredient.capitalize()}**: {safety}\nКомментарий: {comment}\n\n"
        else:
            response += f"**{ingredient.capitalize()}**: Информация отсутствует в базе данных.\n\n"

    await message.reply(response)


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
