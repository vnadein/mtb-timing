import sqlite3
import re
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

    #  on test
    def db_worker(self, request, mode):
        con = sqlite3.connect(self.file_path)
        cur = con.cursor()
        try:
            ret = cur.execute(request)
            if mode == 'commit':
                con.commit()
            elif mode == 'fetchall':
                ret = cur.fetchall()
            elif mode == 'fetchone':
                ret = cur.fetchone()
            con.close()
            return ret
        except Exception as e:
            log.error(paint('[sys][DB][ERROR] ', RED) + str(e))
            con.close()
            return False

    def create_db(self):
        log.info(paint('[sys][DB]', GREEN) + ' Creating database')
        try:
            request = (
                'CREATE TABLE Riders (id INTEGER PRIMARY KEY,'
                ' firstName VARCHAR(100), secondName VARCHAR(30),'
                ' number INTEGER, rider_id INTEGER NOT NULL UNIQUE,'
                ' rider_time_start INTEGER, rider_time_finish INTEGER)')
            self.db_worker(request=request, mode='commit')
            log.info(paint('[sys][DB]', GREEN) + ' Table "Riders" - Created!')
        except Exception as e:
            log.error(paint('[sys][DB][ERROR 1] ', RED) + str(e))
        try:
            request = (
                'CREATE TABLE ChipList (id INTEGER PRIMARY KEY,'
                ' chip_id INTEGER NOT NULL UNIQUE, in_use BOOLEAN)')
            self.db_worker(request=request, mode='commit')
            log.info(paint('[sys][DB]', GREEN) + ' Table "ChipList" - Created!')
        except Exception as e:
            log.error(paint('[sys][DB][ERROR 2]', RED), e)
        try:
            self.db_worker(request='SELECT * FROM Riders', mode='fetchall')
            log.info(paint('[sys][DB]', GREEN) + ' Database created!')
        except Exception as e:
            log.error(paint('[sys][DB][ERROR 3]', RED), e)

    # do not delete
    def add_new_rider(self, firstName, secondName, number):
        con = sqlite3.connect(self.file_path)
        cur = con.cursor()
        try:
            chip_list = self.db_worker(request="SELECT chip_id FROM ChipList WHERE in_use=0", mode='fetchone')
            if chip_list:
                try:
                    if self.db_worker(request="SELECT rider_id FROM Riders WHERE rider_id={}".format(chip_list[0]),
                                      mode='fetchone'):
                        try:
                            self.db_worker(request=("DELETE FROM Riders WHERE rider_id={}".format(chip_list[0])),
                                           mode='commit')
                        except Exception as e:
                            log.error(paint('[sys][DB][ERROR 4] ', RED) + str(e))
                            return False
                    else:
                        data = (firstName, secondName, number, chip_list[0])
                except Exception as e:
                    log.error(paint('[sys][DB][ERROR 5] ', RED) + str(e))
                    return False
            else:
                log.error(paint('[sys][DB][ERROR 6]', RED) + 'No chip_id are avaliable!')
                return False
            try:
                cur.execute("INSERT INTO Riders(firstName, "
                            "secondName, number, "
                            "rider_id) VALUES (?, ?, ?, ?)", data)
            except sqlite3.DatabaseError as e:
                log.error(paint('[sys][DB][ERROR 7]', RED) + str(e))
                con.close()
                return False
            else:
                con.commit()
                log.info(paint('[sys][DB] ', GREEN) + ' Rider added!')
            try:
                cur.execute("UPDATE ChipList SET in_use=? WHERE chip_id=?", ('1', chip_list[0]))
                con.commit()
                log.info(paint('[sys][DB]', GREEN) + ' In_use flag added!')
            except Exception as e:
                log.error(paint('[sys][DB][ERROR 8]', RED) + str(e))
                con.close()
                return False
        except Exception as e:
            log.error(paint('[sys][DB][ERROR 9] ', RED), e)
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
    def get_internal_riderslist(self):
        ret = self.db_worker(request="SELECT rider_id FROM Riders", mode='fetchall')
        ret_formated = re.findall(r'\d{4}', str(ret))
        print(ret)
        return ret_formated

    def set_start_time(self, start_ts, rider_id):
        con = sqlite3.connect(self.file_path)
        cur = con.cursor()
        data = (start_ts, rider_id)
        try:
            cur.execute("SELECT rider_id FROM Riders WHERE rider_id={}".format(rider_id))
            if cur.fetchone()[0] == rider_id:
                cur.execute("UPDATE Riders SET rider_time_start=? WHERE rider_id=?", data)
            else:
                log.error(paint('[sys][DB][ERROR 12]', RED) + 'Rider_id was not found!')
                con.close()
                return False
        except sqlite3.DatabaseError as err:
            log.error(paint('[sys][DB][ERROR 13]', RED) + err)
            con.close()
            return False
        else:
            log.info(paint('[sys][DB]', GREEN) + ' Rider start_ts was set!')
            con.commit()
            con.close()
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
        try:
            self.db_worker(request='DELETE FROM Riders', mode='commit')
        except sqlite3.DatabaseError as err:
            log.error(paint('[sys][DB][ERROR 16]', RED) + err)
            return False
        else:
            log.info(paint('[sys][DB]', GREEN) + ' Riders table cleared!')
            self.__clear_chip_flag()
            return True

    def __clear_chip_flag(self):
        try:
            self.db_worker(request="UPDATE ChipList SET in_use=0", mode='commit')
        except sqlite3.DatabaseError as e:
            log.error(paint('[sys][DB][ERROR 17]', RED), e)
            return False
        log.info(paint('[sys][DB]', GREEN) + ' Chip flag cleared!')
        return True

if __name__ == '__main__':
    db = DataTable()
    #db.clear_chip_flag()
    #db.add_chip(4661)
    #db.add_new_rider('r', 'a', 1)
    #db.clear_all_assignments()
