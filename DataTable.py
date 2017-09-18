import sqlite3
from config import *
# FIXME: No check for insert results!


class DataTable:
    def __init__(self):
        self.file_path = os.path.join(os.getcwd(), DATATABLE_PATH, DATATABLE_FILENAME)
        print('DataTable PATH: ', self.file_path)
        if db_test:
            con = sqlite3.connect(self.file_path)
            cur = con.cursor()
            try:
                cur.execute('SELECT * FROM Riders')
                print(cur.fetchall())
                print('database exists')
                con.close()
            except sqlite3.DatabaseError as err:
                log.error(err)
                print('database is empty...')
                con.close()
                self.create_db()

    def create_db(self):
        print('Creating database')
        con = sqlite3.connect(self.file_path)
        cur = con.cursor()
        cur.execute(
            'CREATE TABLE Riders ('
            'id INTEGER PRIMARY KEY,'
            ' firstName VARCHAR(100),'
            ' secondName VARCHAR(30),'
            ' number INTEGER,'
            ' rider_id INTEGER)')
        con.commit()
        #cur.execute(
        #    'INSERT INTO Riders (id, firstName, secondName, number, id) VALUES(NULL, "Hren", "Proedesh", 1, 066054)')
        #con.commit()
        #print(cur.lastrowid)
        cur.execute('SELECT * FROM Riders')
        print(cur.fetchall())
        con.close()

    def clear_cell_assignment(self, rider_num):
        conn = sqlite3.connect(self.file_path)
        c = conn.cursor()
        data = (rider_num,)
        try:
            c.execute('DELETE FROM Riders WHERE number=?', data)
        except sqlite3.DatabaseError as err:
                log.error(err)
        else:
            conn.commit()
            conn.close()

    def clear_all_assignments(self):
        conn = sqlite3.connect(self.file_path)
        c = conn.cursor()
        try:
            c.execute('DELETE FROM Riders')
        except sqlite3.DatabaseError as err:
            log.error(err)
        else:
            conn.commit()
            conn.close()

    #  TODO: do not delete
    def find_rider_by_assignment(self, first_name, last_name, rider_num=0):
        conn = sqlite3.connect(self.file_path)
        c = conn.cursor()
        if not rider_num:
            data = (first_name, last_name)
            c.execute('SELECT number'
                      ' FROM Riders'
                      ' WHERE firstName=?'
                      ' AND lastName=?', data)
        else:
            data = (first_name, last_name, rider_num)
            c.execute('SELECT number'
                      ' FROM Riders'
                      ' WHERE firstName=?'
                      ' AND secondName=?'
                      ' AND rider_id=?', data)
        res = c.fetchone()
        conn.close()
        if res is None:
            return None
        else:
            return res[0]


if __name__ == '__main__':
    db = DataTable()
    db.clear_all_assignments()
