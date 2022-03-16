import sys
from pathlib import Path

file = Path(__file__).resolve()  
package_root_directory = file.parents[1]  
sys.path.append(str(package_root_directory))  


import aioredis

from aiohttp import web

from app.routes.convert_valutes_routes import get_accessible_valutes_names, get_convert_valute
from app.routes.update_db_routes import update_db
from app.config import settings

app = web.Application()
app['db'] = aioredis.from_url(
    'redis://redis_db', 
    password=settings.DATABASE_PASS,
    decode_responses=True
)

app.router.add_get('/valutes', get_accessible_valutes_names)
app.router.add_get('/convert', get_convert_valute)
app.router.add_post('/database', update_db)


web.run_app(app)