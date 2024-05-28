from sqlalchemy import create_engine, MetaData
from sqlalchemy.dialects.postgresql import insert
from settings import db_config

from contextlib import contextmanager

@contextmanager
def get_raw_db_conn():
    # Initialize and yield the raw database connection
    db_engine = initialize_raw_db_conn()
    try:
        yield db_engine
    finally:
        # Close the connection when exiting the context
        db_engine.dispose()


def insert_dict_sample(dict_sample, table_name, db_engine, return_creation_id=False, upsert=False):
    metadata = MetaData()
    metadata.reflect(bind=db_engine, schema='app')
    table = metadata.tables[table_name]
    stmt = insert(table).values(**dict_sample)
    if upsert:
        stmt = stmt.on_conflict_do_update(
            index_elements=table.primary_key.columns.keys(),
            set_=dict_sample
        )
    with db_engine.connect() as cursor:
        output = cursor.execute(stmt)
        cursor.commit()
    if return_creation_id:
        return output.inserted_primary_key[0]


def get_database_uri():
    return f"postgresql://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"

def initialize_raw_db_conn():
    db_engine = create_engine(get_database_uri())
    return db_engine

def delete_rows(db_engine, table_name, row_ids):
    metadata = MetaData()
    metadata.reflect(bind=db_engine, schema='app')
    table = metadata.tables[table_name]
    for row_id in row_ids:
        stmt = table.delete().where(table.c.get(table.primary_key.columns.keys()[0])==row_id)
        with db_engine.connect() as cursor:
            output = cursor.execute(stmt)
            cursor.commit()
        
