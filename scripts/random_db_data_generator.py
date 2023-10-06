import pandas as pd
import re
import random
import os
from faker import Faker
from datetime import datetime
from db_controller import db_controller
from gpt_interface import initial_conversation, ask_to_create_data, ask_to_create_table_data
from helpful_functions import create_data_df

how_many_inserts = {
    'events': 30,
    'lift_schedules': 100,
    'lifts': 50,
    'parkings': 20,
    'resorts': 10,
    'restaurants': 40,
    'reviews': 110,
    'route_status': 120,
    'routes': 60,
    'users': 60,
    'weather': 200,
    'webcams': 30
}

faker_classes = [
    'name', 'address', 'phone_number', 'email', 'image_url',
    'date', 'time', 'date_time', 'url', 'user_name', 'sentence'
]

data_types = {
    'integer': 'integer',
    'character varying': 'varchar',
    'time without time zone': 'timestamp',
    'text': 'varchar',
    'numeric': 'numeric',
    'decimal': 'decimal',
    'double precision': 'double precision',
    'timestamp without time zone': 'timestamp',
    'date': 'date'
}
basepath = os.join(os.path.dirname(os.path.abspath(os.path.dirname(__name__))), 'csv')
dbc = db_controller()
insertion_sorted_tables = dbc.get_insertion_sorted_tables()
db_schema = dbc.get_db_schema()
db_tables = {}

init_conv_response, init_conversation_context = initial_conversation()
init_conversation_context.append({
    'role': 'system',
    'content': init_conv_response
})
print("INIT CONTEXT")
print(init_conversation_context)

# data_conversation_context = init_conversation_context
for table in insertion_sorted_tables:
    # translation of datatypes
    # print(list(db_schema[table].values()))
    table_datatypes = []
    for dt_tuple in list(db_schema[table].values()):
        if dt_tuple[1] is not None:
            table_datatypes.append(f'{data_types[dt_tuple[0]]} {dt_tuple[1]}')
        else:
            table_datatypes.append(f'{data_types[dt_tuple[0]]}')

    data_response, data_conversation_context = ask_to_create_table_data(
        [table, list(db_schema[table].keys()), table_datatypes, how_many_inserts[table]],
        init_conversation_context)
    data_df = create_data_df(data_response, filepath=os.path.join(basepath, f'{table}.csv'))
