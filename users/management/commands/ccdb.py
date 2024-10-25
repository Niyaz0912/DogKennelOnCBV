from django.core.management import BaseCommand
import pyodbc
from config.settings import DATABASE, USER, PASSWORD, HOST


class Command(BaseCommand):

    def handle(self, *args, **options):
        global conn
        ConnectionString = f'''DRIVER={{ODBC Driver 17 for SQL Server}};
                                        SERVER={HOST};
                                        DATABASE="Dog kennel"
                                        DATABASE={DATABASE};
                                        UID={USER};
                                        PWD={PASSWORD}'''
        try:
            conn = pyodbc.connect(ConnectionString)
            conn.autocommit = True
            conn.execute(fr"CREATE DATABASE {DATABASE};")
        except pyodbc.ProgrammingError as ex:
            print(ex)
        else:
            print("База данных DogKennel успешно создана;")
        finally:
            conn.close()

