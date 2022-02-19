from bigquery import get_client


global client
global dataset
global table


def init(key_management_path, json_key_file, work_dataset, work_table):
    global client
    global dataset
    global table

    json_key = key_management_path + json_key_file

    client = get_client(json_key_file=json_key, readonly=False)
    dataset = work_dataset
    table = work_table


def create_if_not_exists_table(schema):
    global client
    global dataset
    global table

    exists = client.check_table(dataset, table)

    if not exists:
        client.create_table(dataset, table, schema)


def try_insert_rows_table(rows):
    global client
    global dataset
    global table

    exists = client.check_table(dataset, table)

    if exists:
        client.push_rows(dataset, table, rows,)



