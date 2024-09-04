from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, BotCommand
from config import token
import requests, time, asyncio, aioschedule, schedule, logging
import json

bot = Bot(token=token)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

monitoring = False
chat_id = None

async def get_pogoda():
    url = 'https://api.openweathermap.org/data/2.5/weather?q=Osh&appid=7ae9895ce71d3ad63f3c713fd0e2bab9&units=metric'
    response = requests.get(url=url).json()
    temp = response['main']['temp']
    if temp:
        return f'сейчас погода на Оше: {temp}градус'
    else:
        return f'Не удалось получить прогноз'

    

    
async def pogoda_osh():
    while monitoring:
        message = await get_pogoda()
        await bot.send_message(chat_id, message)
      
        #await asyncio.sleep(1)
        logging.info("идет информации о текущей pogoda")
        

        
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.full_name}\nкоманда: /pogoda\nкоманда: /stop')
    logging.info("КОМАНДА START АКТИВНА")

@dp.message(Command('pogoda'))
async def pogoda(message: Message):
    global chat_id, monitoring
    chat_id = message.chat.id
    monitoring = True
    await message.answer("Начало мониторинга")
    try:
        await pogoda_osh()
    except:
        await message.answer('сервер не дает отчет')

    logging.info("КОМАНДА BTC АКТИВНА") 


    
    
@dp.message(Command('stop'))
async def stop(message: Message):
    global monitoring
    monitoring = False
    await message.answer("Мониторинг цены остановлен")
    
async def on():
    await bot.set_my_commands([
        BotCommand(command="/start", description='Start bot'),
        BotCommand(command="/pogoda", description='Start Pogoda monitoring'),        
        BotCommand(command="/stop", description='Stop Pogoda monitoring'),
    ])
    logging.info("БОТ ЗАПУЩЕН")
    #schedule.every(3).seconds.do(pogoda_osh)
  


    
async def main():
    dp.startup.register(on)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())
    

    

  
    
