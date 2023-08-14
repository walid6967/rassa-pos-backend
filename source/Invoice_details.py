from flask import request, json
from database import insert, update, select, delete


def Invoice():
    access_token = request.headers.get('Authorization')
    if request.method == 'POST':
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

        result = insert(
            access_token=access_token,
            table='invoices',
            cols=['invoice_num', 'contact', 'date', 'buy', 'remaining', 'total_amount', 'discount', 'taxes', 'payable_amount','invoice_items'],
            rows=[[invoice_num, contact, date, buy, remaining, total_amount, discount, taxes, payable_amount, invoice_items_json]]
        )
        invoice_id = "edf0fbc3-09fb-44bf-a93e-af995ee7505c"
        for i in invoice_items:
            result = insert(
                access_token=access_token,
                table='items',
                cols=['invoice_id', 'title', 'amount', 'price'],
                rows=[[invoice_id, i['title'], i['amount'], i['price']]]  
            )
            print(result)

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

            result = update(
                access_token=access_token,
                table='invoices',
                cols=['invoice_num', 'contact', 'date', 'buy', 'remaining', 'total_amount', 'discount', 'taxes', 'payable_amount','invoice_items'],
                vals=[invoice_num, contact, date, buy, remaining, total_amount, discount, taxes, payable_amount, invoice_items_json],
                filters=[{'col': 'id', 'op': '=', 'val': id}]
            )
            invoice_id = id 
            for i in invoice_items:
                result = update(
                    access_token=access_token,
                    table='items',
                    cols=['title', 'amount', 'price'],
                    vals=[i['title'], i['amount'], i['price']],
                    filters=[{'col': 'invoice_id', 'op': '=', 'val': invoice_id}]
        )
            print("Update Item Result:", result)
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

    return result