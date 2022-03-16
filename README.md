### GET /convert?from=str&to=str&amount=int
response = {
    'ConvertedAmount': converted_amount
}

#### Exeptions 

HTTPBadRequest
400: 'Параметры запроса неправильны'

HTTPNotFound
404: 'Данные об этих валютах отсутвуют'


### POST /database?merge=int
Если merge == 0, то старые данные инвалидируются
Если merge == 1, то новые данные перетирают старые, но старые все еще акутальны, если не перетерты

json_request = {
    "ValuteName_1": {
        "Value": float,
        "ActualDate": timestamp
    },
    "ValuteName_2": {
        "Value": float,
        "ActualDate": timestamp
    },
    ...
}

Значение валюты в рублях

#### Exeptions

HTTPBadRequest
400: 'Необходим параметр merge'

### GET /valutes
response = ['valute1', 'valute2']
