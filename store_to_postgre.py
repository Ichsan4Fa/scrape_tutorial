from sqlalchemy import create_engine

def store_to_postgre(data, table_name, connection_string):
    try:
        engine = create_engine(connection_string)
        with engine.connect() as connection:
            data.to_sql(table_name, con=engine, if_exists='replace', index=False)
            print(f"Data stored in PostgreSQL table: {table_name}")
    except Exception as e:
        print(f"Error creating PostgreSQL engine: {e}")