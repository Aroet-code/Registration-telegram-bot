import sqlite3

class myDB:
    def __init__(self, db_name="db.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
    
    def load_sql_file(self, filepath:str):
        f = open(filepath, 'r')
        script = f.read()
        f.close()
        self.cursor.executescript(script)
        self.conn.commit()
    
    def load_queries(self, filepath:str):
        f = open(filepath, 'r')
        contents = f.read()
        f.close()

        queries = {}
        current_query = []
        current_name = None

        for line in contents.split("\n"):
            if line.startswith("-- name: "):
                if current_name and current_query:
                    queries[current_name] = '\n'.join(current_query)
                current_name = line.replace('-- name;', '').strip()
                current_query = []
            elif line.strip() and not line.startswith('--'):
                current_query.append(line)
        
        
        if current_name and current_query:
            queries[current_name] = '\n'.join(current_query)
        
        return queries
    
    def debug_database(self):
        print("== Debugging database... ==")
        print(f"Connection: {"open" if self.conn else "closed"}")

        self.cursor.execute("SELECT * FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()
        print(f"Tables: {[t[0] for t in tables]}")

        for t in tables:
            self.cursor.execute(("SELECT COUNT(*) FROM " + t[1] + ";"))
            count = self.cursor.fetchone()[0]
            print(f"{t[0]}: {count} rows")

class Ticket():
    def __init__(self, ticket=None) -> None:
        if ticket == None:
            self.bio = None
            self.phone_number = None
            self.date = None
            self.time = None
            self.reason = None
        else:
            self.bio = ticket.get_bio()
            self.phone_number = ticket.get_phone_number()
            self.date = ticket.get_date()
            self.time = ticket.get_time()
            self.reason = ticket.get_reason()
    
    def set_bio(self, bio):
        self.bio = bio
    
    def set_phone_number(self, phone_number):
        self.phone_number = phone_number
    
    def set_date(self, date):
        self.date = date
    
    def set_time(self, time):
        self.time = time
    
    def set_reason(self, reason):
        self.reason = reason
    
    def get_bio(self):
        return self.bio
    
    def get_phone_number(self):
        return self.phone_number
    
    def get_date(self):
        return self.date
    
    def get_time(self):
        return self.time
    
    def get_reason(self):
        return self.reason