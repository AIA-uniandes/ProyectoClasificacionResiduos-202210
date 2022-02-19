import datetime

from bigquery import get_client


# JSON key provided by Google
key_management_path = '../API_KEY_MANAGEMENT/'
json_key = key_management_path + 'aia-thesis-project-v1-a69cdd9b9882.json'


client = get_client(json_key_file=json_key, readonly=False)


# Create a new table.
schema = [
    {'name': 'RFID', 'type': 'STRING', 'mode': 'required'},
    {'name': 'BAG_COLOR', 'type': 'STRING', 'mode': 'required'},
    {'name': 'BAG_COUNT', 'type': 'INTEGER', 'mode': 'required'},
    {'name': 'DATE_REGISTERED', 'type': 'DATETIME', 'mode': 'required'},
]

dataset = 'FIRST_TESTS_DS'
table = 'TRIAL_FOR_IOT_ARCH'

exists = client.check_table(dataset, table)
print('Check exists: ', exists)

if exists:
    deleted = client.delete_table(dataset, table)
else:
    created = client.create_table(dataset, table, schema)


exists = client.check_table(dataset, table)
print('Check exists: ', exists)

if not exists:
    created = client.create_table(dataset, table, schema)

rows = [
    {'RFID': 'ABCD1234', 'BAG_COLOR': 'black', 'BAG_COUNT': 0, 'DATE_REGISTERED': datetime.datetime.now().isoformat()},
    {'RFID': 'ABCD1234', 'BAG_COLOR': 'white', 'BAG_COUNT': 0, 'DATE_REGISTERED': datetime.datetime.now().isoformat()},
    {'RFID': 'ABCD1234', 'BAG_COLOR': 'green', 'BAG_COUNT': 0, 'DATE_REGISTERED': datetime.datetime.now().isoformat()},
]

inserted = client.push_rows(dataset, table, rows,)
print('inserted: ', inserted)


