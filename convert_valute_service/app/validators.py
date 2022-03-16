import sys
from pathlib import Path

file = Path(__file__).resolve()  
package_root_directory = file.parents[1]  
sys.path.append(str(package_root_directory))  


from json import JSONDecodeError
from pydantic import ValidationError

from app.utils import get_valutes_from_json


async def post_valutes_validator(request): 
    # валидация данных
    try:
        data = dict(await request.json())
        get_valutes_from_json(data)
        return data
    except (ValidationError, KeyError, JSONDecodeError) as e:
        return []