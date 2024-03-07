from ZODB.FileStorage import FileStorage
from ZODB.DB import DB


def get_zodb_storage(file_name):
    storage_path = FileStorage(f"storage/{file_name}")
    db = DB(storage_path)
    connection = db.open()

    return connection.root()
