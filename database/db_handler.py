import sqlite3

class DBHandler:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)
        self.connection.execute("PRAGMA foreign_keys = ON;")
        self.connection.row_factory = sqlite3.Row


    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query, params=None):
        if not self.connection:
            raise Exception("Database connection is not established.")
        
        cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        self.connection.commit()
        return cursor
 
    def fetch_all(self, query, params=None):
        cursor = self.execute_query(query, params)
        return cursor.fetchall()

    def fetch_one(self, query, params=None):
        cursor = self.execute_query(query, params)
        return cursor.fetchone()
    
    def create_tables(self):
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS Ingredients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            );
        """)

        self.execute_query("""
            CREATE TABLE IF NOT EXISTS Recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                instructions TEXT
            );
        """)

        self.execute_query("""
            CREATE TABLE IF NOT EXISTS RecipeIngredients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_id INTEGER NOT NULL,
                ingredient_id INTEGER NOT NULL,
                quantity REAL NOT NULL,
                unit TEXT,
                UNIQUE(recipe_id, ingredient_id),
                FOREIGN KEY (recipe_id) REFERENCES Recipes(id) ON DELETE CASCADE,
                FOREIGN KEY (ingredient_id) REFERENCES Ingredients(id)
            );  
        """)

        self.execute_query("""
            CREATE TABLE IF NOT EXISTS Pantry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ingredient_id INTEGER NOT NULL UNIQUE,
                quantity REAL NOT NULL,
                unit TEXT,
                FOREIGN KEY (ingredient_id) REFERENCES Ingredients(id)
            );
        """)

        self.execute_query("""
            CREATE TABLE IF NOT EXISTS ShoppingList (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ingredient_id INTEGER NOT NULL UNIQUE,
                quantity REAL NOT NULL,
                unit TEXT,
                FOREIGN KEY (ingredient_id) REFERENCES Ingredients(id)
            );
        """)