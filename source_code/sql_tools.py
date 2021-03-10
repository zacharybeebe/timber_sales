import sqlite3 as sq
import pickle
#from parameters import *
from purchaser import Purchaser
from sale import Sale
from unit import Unit
#import math
import datetime as dt




SALE_COLS = ['SORT_ID', 'SALE', 'FISCAL_YEAR', 'AUCTION_DATE', 'FIELD_WORK_DUE', 'object']
SALE_SQL = ', '.join([i for i in SALE_COLS])

PURCHASER_COLS = ['PURCHASER', 'object']
PURCHASER_SQL = ', '.join([i for i in PURCHASER_COLS])

class sqlt(object):
    def connect_db(database):
        conn = sq.connect(database)
        return conn, conn.cursor()

    def create_table(database, table_name, cols_val_list):
        conn, cur = sqlt.connect_db(database)
        sql = 'CREATE TABLE {} ({});'.format(table_name, ', '.join(['{} {}'.format(vals[0], vals[1]) for vals in cols_val_list]))
        cur.execute(sql)
        conn.commit()
        conn.close()

    def select_obj_col(database, table):
        conn, cur = sqlt.connect_db(database)

        sql = "SELECT object FROM {table}".format(table=table)
        cur.execute(sql)
        temp_list = [pickle.loads(i[0]) for i in cur.fetchall()]
        conn.close()
        return temp_list

    def select_data_col(database, table, col_name):
        conn, cur = sqlt.connect_db(database)

        sql = "SELECT {col} FROM {table}".format(table=table, col=col_name)
        cur.execute(sql)
        temp_list = [i[0] for i in cur.fetchall()]
        conn.close()
        return temp_list

    def check_sale_sort_id(database, sale_class, return_class=False):
        sales = [sale_class] + [i for i in sqlt.select_obj_col(database, 'SALES') if i.sort_id != sale_class.sort_id]
        def sort_key(sale):
            return sale.auction
        sales_sorted = sorted(sales, key=sort_key)

        for i, sale in enumerate(sales_sorted):
            sale.sort_id = i + 1
            sqlt.update_sale(database, sale, from_sort=True)

        if return_class:
            return sale_class

    def insert_sale(database, sale_class):
        if isinstance(sale_class, Sale):
            checked_sale = sqlt.check_sale_sort_id(database, sale_class, return_class=True)
            pickled_sale = pickle.dumps(checked_sale)
            vals = [checked_sale.sort_id, checked_sale.name, checked_sale.fy,
                    f'{checked_sale.auction.month}/{checked_sale.auction.day}/{checked_sale.auction.year}',
                    f'{checked_sale.field_work_due.month}/{checked_sale.field_work_due.day}/{checked_sale.field_work_due.year}',
                    pickled_sale]
            conn, cur = sqlt.connect_db(database)

            sql = 'INSERT INTO SALES ({}) VALUES ({})'.format(SALE_SQL, ', '.join(['?' for i in range(len(vals))]))

            cur.execute(sql, vals)
            conn.commit()
            conn.close()
        else:
            raise 'Not a Sale Class'

    def delete_sale(database, sale_class):
        if isinstance(sale_class, Sale):
            sql = 'DELETE FROM SALES WHERE SALE=?;'
            conn, cur = sqlt.connect_db(database)
            cur.execute(sql, [sale_class.name])
            conn.commit()
            conn.close()

    def update_sale(database, sale_class, from_sort=False):
        if isinstance(sale_class, Sale):
            if not from_sort:
                checked_sale = sqlt.check_sale_sort_id(database, sale_class, return_class=True)
            else:
                checked_sale = sale_class
            pickled_sale = pickle.dumps(checked_sale)
            vals = [checked_sale.sort_id, checked_sale.name, checked_sale.fy,
                    f'{checked_sale.auction.month}/{checked_sale.auction.day}/{checked_sale.auction.year}',
                    f'{checked_sale.field_work_due.month}/{checked_sale.field_work_due.day}/{checked_sale.field_work_due.year}',
                    pickled_sale]
            sub_sql = ', '.join(['?' for i in range(len(vals))])

            conn, cur = sqlt.connect_db(database)

            sql = f"UPDATE SALES SET ({SALE_SQL}) = ({sub_sql}) WHERE SORT_ID = '{checked_sale.sort_id}';"

            cur.execute(sql, vals)
            conn.commit()
            conn.close()
        else:
            raise 'Not a Sale Class'

    def select_sale_object(database, name=None, sort_id=None):
        if name is None and sort_id is None:
            raise 'Name and Sort_ID cannot both be None'
        else:
            conn, cur = sqlt.connect_db(database)

            if name is not None:
                sql = "SELECT object FROM SALES WHERE SALE = '{name}'".format(name=name)
            else:
                sql = "SELECT object FROM SALES WHERE SORT_ID = '{sort_id}'".format(sort_id=sort_id)

            cur.execute(sql)
            obj = pickle.loads(cur.fetchone()[0])
            conn.close()
            return obj

    def select_sale_sort_id(database, sale_name):
        conn, cur = sqlt.connect_db(database)
        sql = "SELECT SORT_ID FROM SALES WHERE SALE = '{sale_name}'".format(sale_name=sale_name)
        cur.execute(sql)
        id = cur.fetchone()[0]
        conn.close()
        return id

    def check_sale(database, sale_name):
        conn, cur = sqlt.connect_db(database)
        sql = f"SELECT SALE SALES WHERE SALE = '{sale_name}'"
        cur.execute(sql)
        try:
            cur.fetchone()[0]
            conn.close
            return True
        except TypeError:
            conn.close()
            return False

    def insert_purchaser(database, purchaser_class):
        if isinstance(purchaser_class, Purchaser):
            pickled_purchaser = pickle.dumps(purchaser_class)
            vals = [purchaser_class.name, pickled_purchaser]

            conn, cur = sqlt.connect_db(database)
            sql = 'INSERT INTO PURCHASERS ({}) VALUES ({})'.format(PURCHASER_SQL, ', '.join(['?' for i in range(len(vals))]))
            cur.execute(sql, vals)
            conn.commit()
            conn.close()
        else:
            raise 'Not a Purchaser Class'

    def check_purchaser(database, purchaser_name):
        conn, cur = sqlt.connect_db(database)
        sql = f"SELECT PURCHASER FROM PURCHASERS WHERE PURCHASER = '{purchaser_name}'"
        cur.execute(sql)
        try:
            cur.fetchone()[0]
            conn.close()
            return True
        except TypeError:
            conn.close()
            return False


if __name__ == ('__main__'):
    pass