import psycopg2

class db_controller:
    def __init__(self):
        self.host = ""
        self.database = "skiresortapp"
        self.user = ""
        self.password = ""
        self.cursor = None
        self.conn = None
        self.tables = None
        self.db_desc = None
        self.db_data_types = None
        self.primary_keys = {}
        self.primary_keys_rev = {}
        self.insertion_sorted_tables = []
        self.connect()
        self.get_primary_keys()
        self.description()

    def connect(self):
        self.conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )
        self.cursor = self.conn.cursor()

    def insert(self):
        self.cursor.execute()

    def select(self):
        self.cursor.execute()
        self.cursor.fetchall()

    def close_conn(self):
        self.conn.close()

    def get_primary_keys(self):
        if not self.tables:
            self.cursor.execute \
                ("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            self.tables = [table[0] for table in self.cursor.fetchall()]
        for table in self.tables:
            table_desc = {}
            self.cursor.execute(f"SELECT column_name "
                                f" FROM information_schema.columns "
                                f"WHERE table_name = '{table}'")
            columns = self.cursor.fetchall()
            columns = [column[0] for column in columns]
            for column in columns:
                self.cursor.execute(f"""
                    SELECT
                        tc.table_name, kcu.column_name
                    FROM 
                        information_schema.table_constraints tc
                        JOIN information_schema.key_column_usage kcu
                        ON tc.constraint_name = kcu.constraint_name
                        AND tc.table_name = kcu.table_name
                    WHERE 
                        tc.constraint_type = 'PRIMARY KEY'
                        AND tc.table_name = '{table}'
                        AND kcu.column_name = '{column}';""")
                result = self.cursor.fetchone()
                if result:
                    self.primary_keys[result[0]] = result[1]
                    self.primary_keys_rev[result[1]] = result[0]

    def description(self):
        if not self.tables:
            self.cursor.execute\
                ("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            self.tables = [table[0] for table in self.cursor.fetchall()]
        self.db_desc = {}
        self.db_data_types = {}
        for table in self.tables:
            table_desc = {}
            self.cursor.execute(f"SELECT column_name, "
                                f"data_type, character_maximum_length FROM information_schema.columns "
                                f"WHERE table_name = '{table}'")
            columns = self.cursor.fetchall()
            for column in columns:
                table_desc[column[0]] = (column[1], column[2])
            self.db_desc[table] = table_desc
        self.sort_tables_in_insertion_order()

    def sort_tables_in_insertion_order(self):
        assert self.db_desc
        while len(self.insertion_sorted_tables) != len(self.db_desc.keys()):
            for table, columns in self.db_desc.items():
                cnt = 1
                for column_name in list(columns.keys())[1:]:
                    if (column_name not in self.primary_keys.values() or \
                            (column_name in self.primary_keys.values() and \
                            self.primary_keys_rev[column_name] in self.insertion_sorted_tables)):
                        cnt += 1
                if cnt == len(columns.keys()) and table not in self.insertion_sorted_tables:
                    self.insertion_sorted_tables.append(table)

    def get_insertion_sorted_tables(self):
        assert self.insertion_sorted_tables
        return self.insertion_sorted_tables

    def get_db_schema(self):
        assert self.db_desc
        return self.db_desc


# dbc = db_controller()
# db_desc = dbc.description()


# # Initialize Faker for generating fake data
# fake = Faker()
#
# # Define the number of random inserts you want to generate
# num_inserts = 100
#
# # Generate and insert random data for the Resorts table
# for _ in range(num_inserts):
#     name = fake.company()
#     location = fake.city()
#     description = fake.text()
#     website = fake.url()
#     contact_number = fake.phone_number()
#     email = fake.email()
#
#     cursor.execute(
#         """
#         INSERT INTO Resorts (name, location, description, website, contact_number, email)
#         VALUES (%s, %s, %s, %s, %s, %s)
#         """,
#         (name, location, description, website, contact_number, email)
#     )
#
# # Generate and insert random data for the Routes table
# for _ in range(num_inserts):
#     resort_id = random.randint(1, num_inserts)
#     name = fake.word()
#     difficulty = random.choice(['easy', 'intermediate', 'advanced'])
#     length = random.uniform(100, 10000)  # Adjust range as needed
#     vertical_drop = random.uniform(10, 500)  # Adjust range as needed
#     description = fake.text()
#
#     cursor.execute(
#         """
#         INSERT INTO Routes (resort_id, name, difficulty, length, vertical_drop, description)
#         VALUES (%s, %s, %s, %s, %s, %s)
#         """,
#         (resort_id, name, difficulty, length, vertical_drop, description)
#     )
#
# # Repeat similar steps for other tables (Restaurants, Parkings, Lifts, etc.)
#
# # Commit the changes and close the connection
# conn.commit()
# conn.close()