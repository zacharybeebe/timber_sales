from parameters import *

class Unit(object):
    def __init__(self, sale, name, harvest_type, trust_acres_mbf_list):
        self.sale = sale
        self.name = name.upper()
        self.harvest = harvest_type.upper()
        self.trusts = {i[0]: {ACRES: i[1], MBF: i[2], MBF_AC: i[2] / i[1]} for i in trust_acres_mbf_list}
        self.acres, self.mbf, self.mbf_ac = 0, 0, 0
        self.unit_added = False
        self.sort_id = None

        self.update_sort_id()
        self.calc_unit_stats()
        self.sale.add_unit(self)
        self.unit_added = True

    def calc_unit_stats(self):
        self.acres = 0
        self.mbf = 0
        for trust in self.trusts:
            self.acres += self.trusts[trust][ACRES]
            self.mbf += self.trusts[trust][MBF]
        self.mbf_ac = self.mbf / self.acres
        if self.unit_added:
            self.sale.calc_trusts()

    def update_trust_acres(self, trust, acres):
        if trust not in self.trusts:
            self.trusts[trust] = {}
        self.trusts[trust][ACRES] = float(acres)
        try:
            self.trusts[trust][MBF_AC] = self.trusts[trust][MBF] / self.trusts[trust][ACRES]
        except KeyError or ZeroDivisionError:
            pass

    def update_trust_mbf(self, trust, mbf):
        if trust not in self.trusts:
            self.trusts[trust] = {}
        self.trusts[trust][MBF] = float(mbf)
        try:
            self.trusts[trust][MBF_AC] = self.trusts[trust][MBF] / self.trusts[trust][ACRES]
        except KeyError or ZeroDivisionError:
            pass

    def update_name(self, new_name):
        self.name = new_name.upper()
        self.update_sort_id()

    def update_sort_id(self):
        id_string = ''
        for i in self.name:
            if i.isnumeric():
                id_string += str(i)
        self.sort_id = int(id_string)

    def update_harvest(self, new_harvest):
        self.harvest = new_harvest.upper()

    def delete_trust(self, trust):
        if trust in self.trusts:
            del self.trusts[trust]
            self.calc_unit_stats()


