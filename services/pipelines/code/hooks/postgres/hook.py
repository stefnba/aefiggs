import psycopg
from psycopg.sql import SQL, Identifier
from pydantic import BaseModel


psycopg.Connection

class PostgresConnection(BaseModel):
    host: str = "localhost"
    port: int = 5432
    dbname: str
    user: str
    password: str


def copy_to_db(connection: PostgresConnection, table: str, columns: list[str], records: list[tuple]) -> None:
    """
    Copy records to the database and adding ON CONFLICT feature.
    """

    with psycopg.connect(f"host={connection.host} port={connection.port} dbname={connection.dbname} user={connection.user} password={connection.password}") as conn:
        with conn.cursor() as cursor:
            with conn.transaction():
                cursor.execute(
                    SQL("""
                    CREATE TEMP TABLE tmp_table 
                    (LIKE {table} INCLUDING DEFAULTS)
                    ON COMMIT DROP; 
                    """).format(table=Identifier(table))
                )

                with cursor.copy(SQL(
                    """COPY tmp_table ({columns}) FROM STDIN;
                    """).format(columns=SQL(', ').join(map(Identifier, columns)))) as copy:
                    for record in records:
                        copy.write_row(record)

                cursor.execute(
                    SQL("""
                        INSERT INTO {table}
                        SELECT *
                        FROM tmp_table
                        ON CONFLICT DO NOTHING;
                    """).format(table=Identifier(table))
                )