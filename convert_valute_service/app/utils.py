import sys
from pathlib import Path

file = Path(__file__).resolve()  
package_root_directory = file.parents[0]  
sys.path.append(str(package_root_directory))  

from aiohttp import web
from typing import List
from json import JSONDecodeError


def convert_valute(value_from: float, value_to: float, amount) -> float:
    result = (value_from / value_to) * amount
    return result


# функция для валидации списка курса валют 
async def get_valutes_from_json(data) -> dict:
    result = {}

    try:
        data = dict(await data.json())
        for key, item in data.items():
            result[key] = { 
                'Value': float(item['Value']),
                'ActualDate': int(item['ActualDate'])    
            }
    
    except JSONDecodeError:
        return []
    except KeyError as e:
        raise web.HTTPBadRequest(reason='Данные введены неправильно', text={e: 'осутствует'}, content_type='application/json')
    except ValueError:
        raise web.HTTPBadRequest(reason='Данные введены неправильно')

    return result


def compare_valutes(valutes_db: List[dict], valutes_req: dict):
    
    result_dict = {}
    to_compare = []

    # проверяем есть ли такие же курсы валют в базе данных
    # если есть, добавляем в to_compare для дальнейшего сравения
    # если нет, новую валюту добавляем в конечный результат
    for name in valutes_req.keys():
        if name in valutes_db.keys():
            to_compare.append(name)
        else:
            result_dict[name] = valutes_req[name]
    
    # проверяем актуальность значения
    # если новые значения более актуальны, добавляем их в конечный результат
    for name in to_compare:
        actual_date_db = int(valutes_db[name]['ActualDate'])
        actual_date_req = int(valutes_req[name]['ActualDate'])
        if actual_date_req > actual_date_db:
            result_dict[name] = valutes_req[name]
    
    return result_dict
        


        