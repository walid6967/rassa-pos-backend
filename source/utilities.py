from flask import request
from database import insert, update, select, delete

def utilities():
    access_token = request.headers.get('Authorization')

    if request.method == 'POST':
        body = request.json
        if not body:
            return {'error': 'No body provided'}, 400
        
        title = body.get('title')
        key = body.get('key')
        value = body.get('value')

        result = insert(
            access_token=access_token,
            table='utilities',
            cols=['title', 'key', 'value'],
            rows=[[title, key, value]]
        )

    elif request.method == 'PUT':
        id = request.args.get('id')
        body = request.json
        if not body:
            return {'error': 'No body provided'}, 400
        
        title = body.get('title')
        key = body.get('key')
        value = body.get('value')

        result = update(
            access_token=access_token,
            table='utilities',
            cols=['title', 'key', 'value'],
            vals=[title, key, value],
            filters=[{'col': 'id', 'op': '=', 'val': id}]
        )

    elif request.method == 'DELETE':
        id = request.args.get('id')

        result = delete(
            access_token=access_token,
            table='utilities',
            filters=[{'col': 'id', 'op': '=', 'val': id}]
        )

    else:
        result = select(
            access_token=access_token,
            table='utilities',
            cols=['id','title', 'key', 'value']
        )

    return result