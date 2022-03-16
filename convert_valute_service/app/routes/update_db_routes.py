import sys
from pathlib import Path

file = Path(__file__).resolve()  
package_root_directory = file.parents[1]  
sys.path.append(str(package_root_directory))  


from aiohttp import web

from app.redis_utils import get_valutes_data, get_valutes_names, set_new_valutes
from app.utils import compare_valutes, get_valutes_from_json


async def update_db(request):
    """
    Добавляем новые данные в бд
    на вход получаем 
    {
        "ValuteName_1": {
            "Value": "FLOAT",
            "ActualDate": "TIMESTAMP"
        },
        "ValuteName_2": {
            "Value": "FLOAT",
            "ActualDate": "TIMESTAMP"
        }
    }
    и параметр запроса merge
    """
    # получаем доступ к бд
    redis = request.app['db']
    
    # получим данные из запроса
    data = await get_valutes_from_json(request)
    
    # достаем merge
    try:
        merge = request.rel_url.query['merge']
    except KeyError:
        raise web.HTTPBadRequest(reason='Необходим параметр merge')

    # если merge == 0, то полностью очищаем базу и добавляем новые данные
    # если merge == 1, добавляем отсутсвующие валюты и более новые
    if merge == '0':
        # очищаем базу данных
        valutes_names_db = await get_valutes_names(redis)
        for name in valutes_names_db:
            await redis.delete(name)
        await redis.delete('ValutesNames')
        # добавим новые валюты в бд
        if data != []:
            await set_new_valutes(data, redis=redis)
        
        return web.Response(status=200)

    elif merge == '1':
        # получаем курсы валют из бд
        valutes_names_db = await get_valutes_names(redis)
                
        # добавляем новые курсы валют с заменой
        if data != [] and valutes_names_db != []:
            # в список valutes_to_db попадут только те валюты, которые отсутсвуют в базе данных 
            # или с более новым значением
            valutes_data_db = await get_valutes_data(*valutes_names_db, redis=redis)
            valutes_to_db = compare_valutes(
                valutes_data_db, 
                data
            )

            await set_new_valutes(valutes_to_db, redis)

            return web.Response(status=200)
        elif data != []: 
            await set_new_valutes(data, redis=redis)
            return web.Response(status=200)