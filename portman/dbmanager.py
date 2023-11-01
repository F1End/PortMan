import os
import sqlite3


class DatabaseManager:
    def __init__(self, db_path=None, db_name=None, init=True):
        """

        :param db_path: Where database file is to be located (defaults to script directory)
        :param db_name: Database name (defaults to "portman.db")
        :param init: If true, DatabaseManager will check the existence of the db file and tables, and if missing
        creates them when the instance is initiated
        """
        default_db = "portman.db"
        self.db_name = default_db if not db_name else str(db_name)
        self.db_path = self.db_name if not db_path else str(db_path) + str(self.db_name)  # ->imp: os independent
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.default_tables = ["sec_details", "fx_rates", "prices", "trades", "positions", "agg_data", "portfolios"]
        self.table_definitions = {"sec_details": "isin TEXT PRIMARY KEY, "
                                                 "short_name TEXT, "
                                                 "full_name TEXT, "
                                                 "type TEXT, "
                                                 "Subtype TEXT, "
                                                 "Currency TEXT",
                                  "fx_rates": "date TEXT, "
                                              "currency_1 TEXT, "
                                              "currency_2 TEXT, "
                                              "rate REAL",
                                  "prices": "date TEXT, "
                                            "isin TEXT, "
                                            "price REAL,"
                                            "source TEXT",
                                  "trades": "date TEXT, "
                                            "isin TEXT, "
                                            "transaction_type TEXT, "
                                            "quantity INTEGER, "
                                            "average_price REAL",
                                  "positions": "port_id INTEGER, "
                                               "isin TEXT, "
                                               "quantity INTEGER, "
                                               "start_date TEXT"
                                               "end_date TEXT",
                                  "portfolios": "port_id INTEGER, "
                                                "port_name TEXT, "
                                                "broker TEXT, "
                                                "type TEXT"
                                                "remark TEXT",
                                  "agg_data": "date TEXT, "
                                              "port_name TEXT, "
                                              "isin TEXT, "
                                              "type TEXT, "
                                              "subtype TEXT, "
                                              "quantity INTEGER, "
                                              "price REAL, "
                                              "local_currency TEXT,"
                                              "mkt_val_local REAL, "
                                              "global_curr_1 TEXT, "
                                              "mkt_val_global_1 REAL, "
                                              "global_curr_2 TEXT, "
                                              "mkt_val_global_2 REAL"}

        if init:
            self.default_init()

    def default_init(self):
        print("Checking databfile availability...")
        result = self.check_database()
        match result:
            case (True, *rest):
                print("Database check completed.\nExpected tables available.")
            case (False, missing_tables) if type(missing_tables) == list:
                self.init_tables(missing_tables)
            case (False, e) if type(e) == sqlite3.Error:
                raise e

    def create_table_query(self, table_name):
        query_string = """CREATE TABLE IF NOT EXISTS """ + table_name + " (" + self.table_definitions[table_name] + ")"
        return query_string

    def init_tables(self, table_names):
        for table in table_names:
            query = self.create_table_query(table)
            print(f"Creating table {table}...")
            self.cursor.execute(query)
        self.conn.commit()

    def check_database(self):
        if not os.path.exists(self.db_path):
            raise Exception(f"Error: Specified db path {self.db_path} does not exist!\nShutting down...")
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
            db_tables = self.cursor.fetchall()
            db_tables = [table[0] for table in db_tables]
            missing_tables = []
            for table in self.default_tables:
                if table not in db_tables:
                    missing_tables.append(table)
            if missing_tables:
                return False, missing_tables
            else:
                return True, None
        except sqlite3.Error as e:
            return False, e

    def create_database(self):
        # Create database if not exists
        print(f"Creating database file {self.db_path}")
        self.cursor.execute(f"""CREATE DATABASE IF NOT EXISTS {self.db_path}""")
        self.conn.commit()

    def insert_into_table(self, table_name, values):
        # Insert values into specified table
        placeholders = ', '.join(['?'] * len(values))
        query = f'INSERT INTO {table_name} VALUES ({placeholders})'
        self.cursor.execute(query, values)
        self.conn.commit()

    def close_connection(self):
        # Close the database connection
        self.conn.close()
