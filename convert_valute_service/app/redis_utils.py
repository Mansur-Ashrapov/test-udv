import sys
from pathlib import Path

file = Path(__file__).resolve()  
package_root_directory = file.parents[1]  
sys.path.append(str(package_root_directory))  


import aioredis

from aiohttp import web
from typing import List

from app.schemas import Valute


# возвращаем полный список валют
async def get_valutes_names(redis: aioredis.Redis):
    valutes_names = await redis.lrange('ValutesNames', 0, -1)
    return valutes_names


# получаем список классов Valute
async def get_valutes_data(*args, redis: aioredis.Redis) -> List[Valute]:
    valutes_list = []
    for name in args:
        valute_info = await redis.hgetall(name)
        valutes_list.append(Valute(
            name=name,
            value=valute_info['Value'],
            actual_date=valute_info['ActualDate']
        ))
    return valutes_list

# добавляем новые данные
async def set_new_valutes(valutes_dict, redis: aioredis.Redis): 
    
    for valute_name, item in valutes_dict.items():
        # добавляем название валюты в список названий 
        await redis.lpush('ValutesNames', valute_name)
        # добавляем валюту 
        await redis.hmset(valute_name, item)

# достаем значения курсов валют
async def get_valutes_values_or_404(valute_from: str, valute_to: str, redis: aioredis.Redis) -> List[float]:
    valutes = await get_valutes_data(valute_from, valute_to, redis=redis)
    
    value_from = valutes[0].value
    value_to = valutes[1].value

    return [float(value_from), float(value_to)]
