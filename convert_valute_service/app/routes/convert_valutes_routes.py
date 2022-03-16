import sys
from pathlib import Path

file = Path(__file__).resolve()  
package_root_directory = file.parents[1]  
sys.path.append(str(package_root_directory))  


from aiohttp import web
from pydantic import ValidationError

from app.schemas import ConvertFromTo
from app.redis_utils import get_valutes_values_or_404, get_valutes_names
from app.utils import convert_valute


async def get_convert_valute(request):
    """ 
    Конвертируем валюту 
    На вход получаем параметры запроса from, to, amount
    """

    # получаем доступ к бд
    redis = request.app['db']

    # получаем даные из параметров запроса
    query_params = request.rel_url.query
    try:
        data = ConvertFromTo(
            valute_from=query_params['from'],
            valute_to=query_params['to'],
            amount=float(query_params['amount'])
        )
    except (KeyError, ValidationError) as e :
        raise web.HTTPBadRequest(body=f'{query_params}')

    # получаем значение курса каждой валюты из базы данных
    # если такой валюты не будет в бд, то выйдет ошибка ValidationError
    # так как не будет данных для класса Valute
    try: 
        value_from, value_to = await get_valutes_values_or_404(
            data.valute_from,
            data.valute_to,
            redis                                            
        )
    except (ValidationError, KeyError) as e:
        raise web.HTTPNotFound(reason='Данные об этих валютах отсутвуют')

    # конвертируем сумму
    converted_amount = convert_valute(value_from, value_to, data.amount)

    response = {
        'ConvertedAmount': converted_amount
    }

    return web.json_response(response)


# async def get_accessible_valutes_names(request):
#     """
#     Получаем доступные для конвертации валюты
#     """

#     # получаем доступ к бд
#     redis = request.app['db']

#     valutes_name = await get_valutes_names(redis=redis)
    
#     return web.json_response(data=valutes_name)
