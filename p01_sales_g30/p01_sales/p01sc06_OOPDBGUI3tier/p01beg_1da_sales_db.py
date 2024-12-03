# [import any other necessary module(s)]

from pathlib import Path
from datetime import date


# -------------- Data Access (SQLite) --------------------------
class SQLiteDBAccess:
    SQLITEDBPATH = Path(__file__).parent.parent / 'p01_db'

    def __init__(self):
        self._sqlite_sales_db = 'sales_db.sqlite'
        self._dbpath_sqlite_sales_db = SQLiteDBAccess.SQLITEDBPATH / self._sqlite_sales_db


    def connect(self) -> sqlite3.Connection:
        '''Connect to the SQLite database and return the connection object.'''


    def retrieve_sales_by_date_region(self, sales_date: date, region_code: str) -> Optional[Sales]:
        '''retrieve ID, amount, salesDate, adn region field from Sales table for the records that have the given salesDate and region values.'''


    def update_sales(self, sales: Sales) -> None:
        '''update amount, salesDate, and region fields of Sales table for the record with the given ID value. '''
      

    def retrieve_regions(self) -> Regions:
        '''retreive region code and name from Region table'''

