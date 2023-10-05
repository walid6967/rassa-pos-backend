from flask import request, json
from database import insert, update, select, delete

def Invoice():
    access_token = request.headers.get('Authorization')
    
    utilities_result = select(
        access_token=access_token,
        table='utilities',
        cols=['value'],
        filters=[{'col': 'key', 'op': '=', 'val': 'tax_percentage'}]
    )

    if 'result' in utilities_result and utilities_result['result']:
        tax_percentage = float(utilities_result['result'][0][0])
    else:
        tax_percentage = 0.1 

    if request.method == 'POST':
        body = request.json
        if not body:
            return {'error': 'No body provided'}, 400
        type = body.get('type')
        invoice_num = body.get('invoice_num')
        contact = body.get('contact')
        date = body.get('date')
        buy = body.get('buy')
        remaining = body.get('remaining')
        total_amount = body.get('total_amount')
        discount = body.get('discount')
        invoice_items = body.get('invoice_items')

        invoice_items_json = json.dumps(invoice_items)

        # taxes = total_amount * tax_percentage
        # payable_amount = total_amount - taxes - discount

        item = []
        for item_id, item in enumerate(invoice_items):
            result = insert(
                access_token=access_token,
                table='items',
                cols=['title', 'amount', 'price', 'item_id'],
                rows=[[item['title'], item['amount'], item['price'], item_id]]  
            )
        # Include "id" field in each item of the response
        invoice_items_with_id = [{'id': item_id + 1, **item} for item_id, item in enumerate(invoice_items)]

        # Convert the modified list to JSON
        invoice_items_json = json.dumps(invoice_items_with_id)

        result = insert(
            access_token=access_token,
            table='invoices',
            cols=['type','invoice_num', 'contact', 'date', 'buy', 'remaining', 'total_amount', 'discount', 'taxes', 'payable_amount','invoice_items'],
            rows=[[type,invoice_num, contact, date, buy, remaining, total_amount, discount, taxes, payable_amount, invoice_items_json]]
        )
    elif request.method == 'PUT':
            id = request.args.get('id')
            body = request.json
            if not body:
                return {'error': 'No body provided'}, 400
            
            invoice_num = body.get('invoice_num')
            contact = body.get('contact')
            date = body.get('date')
            buy = body.get('buy')
            remaining = body.get('remaining')
            total_amount = body.get('total_amount')
            discount = body.get('discount')
            taxes = body.get('taxes')
            payable_amount = body.get('payable_amount')
            invoice_items = body.get('invoice_items')

            invoice_items_json = json.dumps(invoice_items)

            # taxes = total_amount * tax_percentage
            # payable_amount = total_amount - taxes


            result = update(
                access_token=access_token,
                table='invoices',
                cols=['invoice_num', 'contact', 'date', 'buy', 'remaining', 'total_amount', 'discount', 'taxes', 'payable_amount','invoice_items'],
                vals=[invoice_num, contact, date, buy, remaining, total_amount, discount, taxes, payable_amount, invoice_items_json],
                filters=[{'col': 'id', 'op': '=', 'val': id}]
            )
            for item in body.get('invoice_items', []):
                item_id = item.get('id')
                if item_id:
                    result = update(
                        access_token=access_token,
                        table='items',
                        cols=['title', 'amount', 'price'],
                        vals=[item['title'], item['amount'], item['price']],
                        filters=[{'col': 'id', 'op': '=', 'val': item_id}]
                    )

                
    elif request.method == 'DELETE':
        id = request.args.get('id')
        result = delete(
            access_token=access_token,
            table='invoices',
            filters=[{'col': 'id', 'op': '=', 'val': id}]
        )
        if result.get('success'):
            result_items = delete(
                access_token=access_token,
                table='items',
                filters=[{'col': 'invoice_id', 'op': '=', 'val': id}]
            )
            print(result_items)

    else:
        result = select(
            access_token=access_token,
            table='invoices',
            cols=['id', 'invoice_num', 'contact', 'date', 'buy', 'remaining', 'total_amount', 'discount', 'taxes','payable_amount','invoice_items'],
            )
        
        keys = ['id', 'invoice_num', 'contact', 'date', 'buy', 'remaining', 'total_amount', 'discount', 'taxes','payable_amount','invoice_items']
        result_mapped = convert_arr_to_map(keys, result.get('result', []))
    
        return result_mapped 
    return result

def get_invoice_by_id():
    access_token = request.headers.get('Authorization')
    id = request.args.get('id') 
    if id:
        if request.method == 'GET':
            result = select(
                access_token=access_token,
                table='invoices',
                cols=['id', 'invoice_num', 'contact', 'date', 'buy', 'remaining', 'total_amount', 'discount', 'taxes','payable_amount','invoice_items'],
                filters=[{'col': 'id', 'op': '=', 'val': id}]
            )

            if 'result' in result and result['result']:
                keys = ['id', 'invoice_num', 'contact', 'date', 'buy', 'remaining', 'total_amount', 'discount', 'taxes','payable_amount','invoice_items']
                result_mapped = convert_arr_to_map(keys, [result['result'][0]])
                return result_mapped

            return {'error': 'Invoice not found'}, 404
        return result

def convert_arr_to_map(keys, arr):
    return [{key: val for key, val in zip(keys, invoices)} for invoices in arr]