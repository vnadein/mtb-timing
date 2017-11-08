import sqlite3
from config import *


class DataTable:
    def __init__(self):
        self.file_path = os.path.join(os.getcwd(), DATATABLE_PATH, DATATABLE_FILENAME)
        log.info((paint('[sys][DB]', GREEN) + ' DataTable PATH: ') + str(self.file_path))
        log.info('\n\n' + paint(' [sys][DB]', GREEN) + ' DataTable INIT...' + '\n\n')
        if db_test:
            log.info(paint('[sys][DB]', GREEN) + ' DB test is true!')
            con = sqlite3.connect(self.file_path)
            cur = con.cursor()
            try:
                cur.execute('SELECT * FROM Riders')
                print(cur.fetchall())
                log.info(paint('[sys][DB]', GREEN) + ' Database exists')
                con.close()
            except sqlite3.DatabaseError as err:
                log.error(err)
                log.warning(paint('[sys][DB]', GREEN) + ' Database is empty...')
                con.close()
                self.create_db()

    def create_db(self):
        log.info(paint('[sys][DB]', GREEN) + ' Creating database')
        con = sqlite3.connect(self.file_path)
        cur = con.cursor()
        try:
            cur.execute(
                'CREATE TABLE Riders ('
                'id INTEGER PRIMARY KEY,'
                ' firstName VARCHAR(100),'
                ' secondName VARCHAR(30),'
                ' number INTEGER,'
                ' rider_id INTEGER NOT NULL UNIQUE,'
                ' rider_time_start INTEGER,'
                ' rider_time_finish INTEGER)')
            con.commit()
            log.info(paint('[sys][DB]', GREEN) + ' Table "Riders" - Created!')
        except Exception as e:
            log.error(paint('[sys][DB][ERROR 1]', GREEN), e)
            con.close()

        try:
            cur.execute(
                'CREATE TABLE ChipList ('
                'id INTEGER PRIMARY KEY,'
                ' chip_id INTEGER NOT NULL UNIQUE,'
                ' in_use BOOLEAN)')
            con.commit()
            log.info(paint('[sys][DB]', GREEN) + ' Table "ChipList" - Created!')
        except Exception as e:
            log.error(paint('[sys][DB][ERROR 2]', RED), e)
            con.close()

        try:
            cur.execute('SELECT * FROM Riders')
            log.info(paint('[sys][DB]', GREEN) + ' Database created!')
        except Exception as e:
            log.error(paint('[sys][DB][ERROR 3]', RED), e)
            con.close()
        con.close()

    # do not delete
    def add_new_rider(self, firstName, secondName, number):
        con = sqlite3.connect(self.file_path)
        cur = con.cursor()
        try:
            cur.execute("SELECT chip_id FROM ChipList WHERE in_use=?", '0')
            chip_list = cur.fetchone()
            if chip_list:
                try:
                    cur.execute("SELECT rider_id FROM Riders WHERE rider_id=?", chip_list[0])
                    if cur.fetchone():
                        try:
                            cur.execute("DELETE FROM Riders WHERE rider_id=?", chip_list[0])
                            con.commit()
                        except Exception as e:
                            log.error(paint('[sys][DB][ERROR 4]', RED) + e)
                            con.close()
                            return False
                    else:
                        data = (firstName, secondName, number, chip_list[0])
                except Exception as e:
                    log.error(paint('[sys][DB][ERROR 5]', RED) + e)
                    con.close()
                    return False
            else:
                log.error(paint('[sys][DB][ERROR 6]', RED) + 'No chip_id are avaliable!')
                con.close()
                return False
            try:
                cur.execute("INSERT INTO Riders("
                            "firstName, "
                            "secondName, "
                            "number, "
                            "rider_id) "
                            "VALUES (?, ?, ?, ?)", data)
            except sqlite3.DatabaseError as e:
                log.error(paint('[sys][DB][ERROR 7]', RED) + str(e))
                con.close()
                return False
            else:
                con.commit()
                log.info(paint('[sys][DB] ', GREEN) + ' Rider added!')
            try:
                cur.execute("SELECT chip_id FROM ChipList")
                print('CHIPLIST! - ', cur.fetchall())
                cur.execute("UPDATE ChipList SET in_use=? WHERE chip_id=?", ('1', chip_list[0]))
                con.commit()
                log.info(paint('[sys][DB]', GREEN) + ' In_use flag added!')
            except Exception as e:
                log.error(paint('[sys][DB][ERROR 8]', RED) + e)
                con.close()
                return False
        except Exception as e:
            log.error(paint('[sys][DB][ERROR 9]', RED), e)
            if 'UNIQUE constraint failed: Riders.rider_id' in str(e):
                log.info('rider_id already exists! Try to change rider_id!')
            con.close()
            return False
        else:
            con.close()
            return True

    def add_chip(self, chip_number):
        if type(chip_number) is not int:
            log.error(paint('[sys][DB][ERROR 10]', RED) + ' Chip number must be integer!')
            return False
        con = sqlite3.connect(self.file_path)
        cur = con.cursor()
        try:
            cur.execute("INSERT INTO ChipList(chip_id, in_use) VALUES ({0}, {1})".format(chip_number, 0))
            log.info(paint('[sys][DB]', GREEN) + ' Chip added!')
        except Exception as e:
            log.error(paint('[sys][DB][ERROR 11]', RED), e)
            con.close()
            return False
        else:
            con.commit()
            con.close()
            return True

#  TODO: do not delete
    # не доделано
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

    # internal functions
    def set_start_time(self, start_ts, rider_id):
        conn = sqlite3.connect(self.file_path)
        cur = conn.cursor()
        data = (start_ts, rider_id)
        try:
            cur.execute("SELECT rider_id FROM Riders WHERE rider_id={}".format(rider_id))
            if cur.fetchone()[0] == rider_id:
                cur.execute("UPDATE Riders SET rider_time_start=? WHERE rider_id=?", data)
            else:
                log.error(paint('[sys][DB][ERROR 12]', RED) + 'Rider_id was not found!')
                conn.close()
                return False
        except sqlite3.DatabaseError as err:
            log.error(paint('[sys][DB][ERROR 13]', RED) + err)
            conn.close()
            return False
        else:
            log.info(paint('[sys][DB]', GREEN) + ' Rider start_ts was set!')
            conn.commit()
            conn.close()
            return True

    def set_finish_ts(self, finish_ts, rider_id):
        conn = sqlite3.connect(self.file_path)
        cur = conn.cursor()
        data = (finish_ts, rider_id)
        try:
            cur.execute("SELECT rider_id FROM Riders WHERE rider_id={}".format(rider_id))
            if cur.fetchone()[0] == rider_id:
                cur.execute("UPDATE Riders SET rider_time_finish=? WHERE rider_id=?", data)
            else:
                log.error(paint('[sys][DB][ERROR 14]', RED) + 'Rider_id was not found!')
                conn.close()
                return False
        except sqlite3.DatabaseError as err:
            log.error(paint('[sys][DB][ERROR 15]', RED) + err)
            conn.close()
            return False
        else:
            log.info(paint('[sys][DB]', GREEN) + ' Rider finish_ts was set!')
            conn.commit()
            conn.close()
            return True

    # clearing functions
    def clear_all_riders(self):
        conn = sqlite3.connect(self.file_path)
        cur = conn.cursor()
        try:
            cur.execute('DELETE FROM Riders')
        except sqlite3.DatabaseError as err:
            log.error(paint('[sys][DB][ERROR 16]', RED) + err)
            conn.close()
            return False
        else:
            log.info(paint('[sys][DB]', GREEN) + ' Riders table cleared!')
            conn.commit()
            conn.close()
            return True

    def clear_chip_flag(self):
        conn = sqlite3.connect(self.file_path)
        cur = conn.cursor()
        try:
            cur.execute("UPDATE ChipList SET in_use=?", '0')
        except sqlite3.DatabaseError as e:
            log.error(paint('[sys][DB][ERROR 17]', RED), e)
            conn.close()
            return False
        else:
            log.info(paint('[sys][DB]', GREEN) + ' Chip flag cleared!')
            conn.commit()
            conn.close()
            return True

if __name__ == '__main__':
    db = DataTable()
    #db.clear_chip_flag()
    #db.add_chip(4661)
    db.add_new_rider('r', 'a', 1, 1111)
    #db.clear_all_assignments()
