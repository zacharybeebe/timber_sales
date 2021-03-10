class Purchaser(object):
    def __init__(self, name):
        self.name = name.upper()
        self.sales_bid = {}


    def bid_sale(self, sale, bid, win = False, called_from_sale = False):
        if not called_from_sale:
            sale.add_purchaser(self, bid, win, called_from_purchaser=True)
        self.sales_bid[sale.name] = sale
        self.update_database()


    def update_database(self):
        pass
