from django.core.management import BaseCommand
import pyodbc
from config.settings import DATABASE, USER, PASSWORD, HOST

class Command(BaseCommand):

    def handle(self, *args, **options):
        ConnectionString = f'''DRIVER={{ODBC Driver 17 for SQL Server}};
                                        SERVER={HOST};
                                        DATABASE={DATABASE};
                                        UID={USER};
                                        PWD={PASSWORD}'''
        try:
            conn = pyodbc.connect(ConnectionString)
            conn.autocommit = True
            conn.execute(fr"CREATE DATABASE Shelter320;")
        except pyodbc.ProgrammingError as ex:
            print(ex)
        else:
            print("База данных DogKennel;")
        finally:
            conn.close()
