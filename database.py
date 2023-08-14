import requests
import json

DB_CONTROLLER_URL = "https://lajward-mis.dev:3002/db/query"

def select(access_token, table, cols, filters=[]):
    payload = json.dumps({
      "query": {
        "type": "select",
        "table": f"pos___{table}",
        "cols": cols,
        "filters": filters,
        "limit": 0,
        "offset": 0,
        "order_by": []
      }
    })
    headers = {
      'Content-Type': 'application/json',
      'Authorization': access_token
    }

    response = requests.request("POST", DB_CONTROLLER_URL, headers=headers, data=payload)
    return response.json()

def insert(access_token, table, cols, rows):
    payload = json.dumps({
      "query": {
        "type": "create",
        "table": f"pos___{table}",
        "cols": cols,
        "rows": rows
      }
    })
    headers = {
      'Content-Type': 'application/json',
      'Authorization': access_token
    }

    response = requests.request("POST", DB_CONTROLLER_URL, headers=headers, data=payload)
    return response.json()

def delete(access_token, table, filters):
    payload = json.dumps({
      "query": {
        "type": "delete",
        "table": f"pos___{table}",
        "filters": filters
      }
    })
    headers = {
      'Content-Type': 'application/json',
      'Authorization': access_token
    }

    response = requests.request("POST", DB_CONTROLLER_URL, headers=headers, data=payload)
    return response.json()

def update(access_token, table, cols, vals, filters):
    payload = json.dumps({
      "query": {
        "type": "update",
        "table": f"pos___{table}",
        "cols": cols,
        "vals": vals,
        "filters": filters
      }
    })
    headers = {
      'Content-Type': 'application/json',
      'Authorization': access_token
    }

    response = requests.request("POST", DB_CONTROLLER_URL, headers=headers, data=payload)
    print(response.json())
    return response.json()

def convert_arr_to_map(keys, arr):
    return [{key: val for key, val in zip(keys, item)} for item in arr]
