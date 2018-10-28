import pypyodbc as pyodbc

db_host = 'localhost'
db_name = 'Test2'
db_user = 'sa'
db_password = 'admin'


def connect_db():
    connection_query = \
        'Driver={SQL Server};' \
        'Server=' + db_host + \
        ';Database=' + db_name + \
        ';UID=' + db_user + \
        ';PWD=' + db_password + ';'

    return pyodbc.connect(connection_query)


def execute_bulk(table_name, bulk_file):
    db = connect_db()
    cursor = db.cursor()
    sql = "BULK INSERT dbo.{table_name} FROM '{bulk_location}' WITH (FIELDTERMINATOR='|', ROWTERMINATOR='\r\n');" \
        .format(table_name=table_name, bulk_location=bulk_file)

    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()


def recreate_all():
    with connect_db() as db:
        with db.cursor() as cursor:
            with open("./Creates.sql", "r") as file:
                data = file.read().replace('\n', '')
                for statement in data.split(';'):
                    if len(statement) == 0:
                        continue

                    cursor.execute(statement)
                    db.commit()


