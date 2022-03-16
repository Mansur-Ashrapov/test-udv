import sys
from pathlib import Path

file = Path(__file__).resolve()  
package_root_directory = file.parents[1]  
sys.path.append(str(package_root_directory))  


import aioredis

from typing import List


# возвращаем полный список валют
async def get_valutes_names(redis: aioredis.Redis):
    valutes_names = await redis.lrange('ValutesNames', 0, -1)
    return valutes_names


# получаем список классов Valute
async def get_valutes_data(*args, redis: aioredis.Redis):
    result = {}
    for name in args:
        valute_info = await redis.hgetall(name)
        result[name] = { 
            'Value': float(valute_info['Value']),
            'ActualDate': int(valute_info['ActualDate'])    
        }
    return result

# добавляем новые данные
async def set_new_valutes(valutes_dict, redis: aioredis.Redis): 
    db_valutes_names = await get_valutes_names(redis)
    
    for valute_name, item in valutes_dict.items():
        # добавляем название валюты в список названий
        # чтобы не дублировать название в списке названий валют, проверим наличие в бд
        if valute_name in db_valutes_names:
            continue
        else:    
            await redis.lpush('ValutesNames', valute_name)
        # добавляем валюту 
        await redis.hmset(valute_name, item)

# достаем значения курсов валют
async def get_valutes_values(valute_from: str, valute_to: str, redis: aioredis.Redis) -> List[float]:
    valutes = await get_valutes_data(valute_from, valute_to, redis=redis)
    
    value_from = valutes[valute_from]['Value']
    value_to = valutes[valute_to]['Value']

    return [float(value_from), float(value_to)]
