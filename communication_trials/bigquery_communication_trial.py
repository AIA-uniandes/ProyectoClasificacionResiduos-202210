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
    {'name': 'foo', 'type': 'STRING', 'mode': 'nullable'},
    {'name': 'bar', 'type': 'FLOAT', 'mode': 'nullable'}
]

dataset = 'FIRST_TESTS_DS'
table = 'TEST_TABLE'

exists = client.check_table(dataset, table)
print('Check exists: ', exists)

if exists:
    created = client.create_table(dataset, table, schema)

# Delete an existing table.
deleted = client.delete_table(dataset, table)

exists = client.check_table(dataset, table)
print('Check exists: ', exists)
