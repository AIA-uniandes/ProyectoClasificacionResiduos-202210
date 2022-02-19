import datetime

from bigquery import get_client

# BigQuery project id as listed in the Google Developers Console.
project_id = 'aia-thesis-project-v1'

# Service account email address as listed in the Google Developers Console.
service_account = 'aia-tests-angel@aia-thesis-project-v1.iam.gserviceaccount.com'


# JSON key provided by Google
json_key = '../API_KEY_MANAGEMENT/aia-thesis-project-v1-a69cdd9b9882.json'


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


