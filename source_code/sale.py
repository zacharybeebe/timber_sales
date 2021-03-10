#import arcpy
from parameters import *
import datetime as dt
from unit import Unit
from purchaser import Purchaser
#from sql_tools import  sqlt


class Sale(object):
    def __init__(self, name, auction_date, cruised=False):
        self.name = name.upper()
        self.auction = self.check_date(auction_date)
        self.fy = None
        self.update_fy()
        self.field_work_due = None
        self.update_field_work_date()
        self.acres, self.mbf, self.mbf_ac = 0, 0, 0
        self.units, self.trusts = {}, {}

        self.est_val_mbf = 0
        self.est_val = 0

        self.cruised = cruised
        self.min_bid = 0
        self.min_bid_mbf = 0
        self.min_bid_acre = 0

        self.win_bid = 0
        self.win_bid_mbf = 0
        self.win_bid_acre = 0
        self.purchasers = {}

        self.sort_id = 1000


    def check_date(self, value):
        delimiters = [',', '.', '/', '-', '_', ':', ';', '?', '|', '~', '`']
        if isinstance(value, str):
            try:
                month, day, year = value[:2], value[2:4], value[4:]
                if len(year) < 4:
                    year = f'20{year}'
                month, day, year = int(month), int(day), int(year)
                return dt.date(year, month, day)
            except:
                for i in delimiters:
                    try:
                        month, day, year = value.split(i)
                        if len(year) < 4:
                            year = f'20{year}'
                        month, day, year = int(month), int(day), int(year)
                        return dt.date(year, month, day)
                    except:
                        next
                else:
                    raise Exception('Invalid date seperator -- try */* as in MM/DD/YYYY')
        elif isinstance(value, dt.datetime):
            return dt.date(value.year, value.month, value.day)
        elif isinstance(value, dt.date):
            return value
        else:
            raise Exception('Invalid date')



    def add_unit(self, unit_or_list_of_units):
        unit = unit_or_list_of_units
        if isinstance(unit, Unit):
            self.units[unit.sort_id] = [unit.name, unit]
        elif isinstance(unit, list):
            for i, u in enumerate(unit):
                if isinstance(u, Unit):
                    self.units[u.sort_id] = [u.name, u]
                else:
                    raise 'Not valid unit at list index {}'.format(i)
        else:
            raise 'Not valid unit'
        self.calc_trusts()

    def delete_unit(self, unit):
        if unit.sort_id in self.units:
            del self.units[unit.sort_id]
        self._delete_unit_name_change()
        self.calc_trusts()

    def _delete_unit_name_change(self):
        for i, key in enumerate(self.units):
            unit = self.units[key][1]
            unit.update_name(f'U{i+1}')
        self.reorder_units()


    def add_purchaser(self, purchaser, bid, win=False, called_from_purchaser=False):
        if isinstance(purchaser, Purchaser):
            ob = bid - self.min_bid
            keys = [WIN, BID, BID_MBF, BID_ACRES, OB, OB_MBF, OB_ACRES, OB_PCT, PURCHASER]
            values = [win, bid, bid / self.mbf, bid / self.acres, ob, ob / self.mbf, ob / self.acres, ob / self.min_bid, purchaser]

            self.purchasers[purchaser.name] = {}
            for key, value in zip(keys, values):
                self.purchasers[purchaser.name][key] = value
            if not called_from_purchaser:
                purchaser.bid_sale(self, bid, win, called_from_sale=True)
            self.calc_bids()
        else:
            raise 'Not valid Purchaser'

    def calc_trusts(self):
        self.trusts = {}
        for key in self.units:
            unit = self.units[key][1]
            for trust in unit.trusts:
                if trust not in self.trusts:
                    self.trusts[trust] = {}
                    self.trusts[trust][ACRES] = unit.trusts[trust][ACRES]
                    self.trusts[trust][MBF] = unit.trusts[trust][MBF]
                else:
                    self.trusts[trust][ACRES] += unit.trusts[trust][ACRES]
                    self.trusts[trust][MBF] += unit.trusts[trust][MBF]

                self.trusts[trust][MBF_AC] = self.trusts[trust][MBF] / self.trusts[trust][ACRES]
        self.calc_sale_stats()

    def calc_sale_stats(self):
        self.acres, self.mbf, self.mbf_ac = 0, 0, 0
        for trust in self.trusts:
            self.acres += self.trusts[trust][ACRES]
            self.mbf += self.trusts[trust][MBF]
        self.mbf_ac = self.mbf / self.acres
        self.update_est_value()

    def calc_bids(self):
        for pur in self.purchasers:
            if self.purchasers[pur][WIN]:
                self.win_bid = self.purchasers[pur][BID]
                self.win_bid_mbf = self.purchasers[pur][BID_MBF]
                self.win_bid_acre = self.purchasers[pur][BID_ACRES]

    def update_min_bid(self, minimum_bid):
        self.min_bid = float(minimum_bid)
        self.min_bid_mbf = self.min_bid / self.mbf
        self.min_bid_acre = self.min_bid / self.acres

    def update_units_sort_id(self):
        temp = []
        for unit in self.units:
            self.units[unit][1].update_sort_id()
            temp.append([self.units[unit][1].sort_id, self.units[unit][1].name, self.units[unit][1]])
        self.units = {i[0]: [i[1], i[2]] for i in temp}

    def update_sort_id(self, new_id):
        self.sort_id = int(new_id)

    def update_unit(self, unit):
        del self.units[unit.sort_id]
        self.add_unit(unit)

    def update_auction_date(self, new_date):
        self.auction = self.check_date(new_date)
        self.update_fy()
        self.update_field_work_date()

    def update_est_mbf(self, new_mbf_value):
        self.est_val_mbf = self.format_from_currency(new_mbf_value)
        self.update_est_value()

    def update_est_value(self):
        self.est_val = self.est_val_mbf * self.mbf

    def update_name(self, new_name):
        self.name = new_name.upper()

    def update_fy(self):
        self.fy = self.get_fy_from_auction()

    def update_field_work_date(self):
        setbacks = {'0': 12, '-1': 11, '-2': 10, '-3': 9, '-4': 8, '-5': 7}
        month = self.auction.month - 6
        year = self.auction.year
        if str(month) in setbacks:
            month = setbacks[str(self.auction.month - 6)]
            year -= 1
        self.field_work_due = self.check_date('{}/{}/{}'.format(month, 1, year))

    def get_fy_from_auction(self):
        keep_year = [1, 2, 3, 4, 5, 6]
        if self.auction.month in keep_year:
            return self.auction.year
        else:
            return self.auction.year + 1

    def reorder_units(self):
        temp = {}
        for key in self.units:
            unit = self.units[key][1]
            temp[unit.sort_id] = [unit.name, unit]
        self.units = temp

    def format_currency(self, value):
        val_list = [i for i in str(round(value, 2))]
        if '.' not in val_list:
            add_to = ['.', '0', '0']
            for i in add_to:
                val_list.append(i)
        else:
            if len(val_list[-(len(val_list) - val_list.index('.')):]) < 3:
                val_list.append('0')
        temp = [i for i in reversed(val_list)]
        added = 0
        for i in range(3, len(val_list)):
            if i != 3 and i % 3 == 0:
                temp.insert(i+added, ',')
                added += 1
        return '${}'.format(''.join([i for i in reversed(temp)]))


    def format_from_currency(self, value):
        try:
            float(value)
            return float(value)
        except ValueError:
            rep1 = value.replace('$', '')
            return float(rep1.replace(',', ''))











if __name__ == ('__main__'):
    crown = Sale('TEST_SALE', 2022, '10:26:2021')

    u_list = [Unit(crown, 'U1', 'VRH', [['03', 45.2, 1040], ['77', 40.3, 927]]),
              Unit(crown, 'U2', 'VRH', [['03', 96.7, 2030], ['77', 2.6, 52]]),
              Unit(crown, 'U3', 'VDT', [['03', 15.7, 177]])]

    crown.add_unit(u_list)

    crown.est_val_mbf = 350
    crown.update_est_value()
    cestmbf = crown.format_currency(crown.est_val_mbf)
    cest = crown.format_currency(crown.est_val)
    print('F-estvalmbf: {}'.format(cestmbf))
    print('F-estval: {}'.format(cest))
    print('BCK-estvalmbf: {}'.format(crown.format_from_currency(cestmbf)))
    print('BCK-estvalmbf: {}'.format(crown.format_from_currency(cest)))

    for i in range(3):
        if i == 1:
            crown.units['U1'].modify_trust('03', 56.5, 1340)
        elif i == 2:
            crown.units['U2'].add_trust('07', 22.2, 405)

        print('{}:'.format(crown.name))
        print('AUCTION: {}/{}/{}'.format(crown.auction.month, crown.auction.day, crown.auction.year))
        print('FIELD WORK: {}/{}/{}'.format(crown.field_work_due.month, crown.field_work_due.day, crown.field_work_due.year))
        print('{}: {}'.format(ACRES, crown.acres))
        print('{}: {}'.format(MBF, crown.mbf))
        print('{}: {}'.format(MBF_AC, crown.mbf_ac))
        for trust in crown.trusts:
            print('{key}: {data}'.format(key=trust, data=crown.trusts[trust]))
        print('')







