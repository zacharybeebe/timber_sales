import tkinter as t
from tkinter import ttk, filedialog, messagebox
from parameters import *
from sql_tools import sqlt
from sale import Sale
from unit import Unit


class New_Sale(object):
    def __init__(self, program):
        self.p = program
        self.label_width = 130
        self.run()

    def run(self):
        self.top = t.Toplevel(self.p.root)
        self.top.geometry("+{}+{}".format(SCREEN_POS_RIGHT + 250, SCREEN_POS_DOWN + 150))
        self.top.transient(self.p.root)

        self.frame = t.Frame(self.top, bg=SEAGREEN, height=SALE_UHEIGHT * 5, width=800)
        self.frame.pack()
        head = t.Label(self.frame, bg=SEAGREEN, font=font10Cb, text='ADD NEW SALE')
        head.place(x=0, y=0, width=100, height=SALE_UHEIGHT)

        self._inputs()

    def _inputs(self):
        labels = ['NAME', 'AUCTION DATE', '# OF UNITS']
        entries = []
        x = 0
        for i, lab in enumerate(labels):
            if i == 0:
                insert = '*NEW SALE*'
            else:
                insert = ''
            label = t.Label(self.frame, bg=SEAGREEN, font=font10Cb, text=lab)
            label.place(x=x, y=SALE_UHEIGHT, width=self.label_width, height=SALE_UHEIGHT)
            entry = t.Entry(self.frame, font=font10Cb)
            entry.place(x=x, y=SALE_UHEIGHT * 2, width=self.label_width, height=SALE_UHEIGHT)
            entry.insert('end', insert)
            entries.append(entry)
            x += self.label_width
            self.top.update()

        submit_button = t.Button(self.frame, font=font10Cb, text='Submit')
        submit_button['command'] = lambda e=entries: self._submit(e)
        submit_button.place(x=0, y=SALE_UHEIGHT * 4, width=self.label_width, height=SALE_UHEIGHT)

    def _submit(self, entries):
        vals = [i.get() for i in entries]
        name, auction, num_units = vals
        trust_list = [['01', 1, 1]]
        sale = Sale(name, auction)
        for i in range(int(num_units)):
            Unit(sale, f'U{i+1}', 'VRH', trust_list)

        sqlt.insert_sale(self.p.db, sale)

        self.p.post_commit_updates(from_sale_tools=True)
        self.top.destroy()



class Delete_Sale(object):
    def __init__(self, program):
        self.p = program
        self.label_width = 130
        self.run()

    def run(self):
        self.top = t.Toplevel(self.p.root)
        self.top.geometry("+{}+{}".format(SCREEN_POS_RIGHT + 250, SCREEN_POS_DOWN + 150))
        self.top.transient(self.p.root)

        self.frame = t.Frame(self.top, bg=SEAGREEN, height=SALE_UHEIGHT * 5, width=400)
        self.frame.pack()
        head = t.Label(self.frame, bg=SEAGREEN, font=font10Cb, text='DELETE SALE')
        head.place(x=0, y=0, width=100, height=SALE_UHEIGHT)

        menu_list = [i for i in self.p.sale_names_frames]
        menu_head = t.StringVar()
        menu_head.set("Select Sale")
        menu = t.OptionMenu(self.frame, menu_head, (*menu_list), command=self._delete_button)
        menu.place(x=0, y=SALE_UHEIGHT*2, width=self.label_width, height=SALE_UHEIGHT * 2)

    def _delete_button(self, selection):
        button = t.Button(self.frame, font=font10Cb, bg=RED, text='DELETE')
        button['command'] = lambda s=selection: self._delete(s)
        button.place(x=int(self.label_width*1.25), y=SALE_UHEIGHT * 2, width=self.label_width, height=SALE_UHEIGHT*2)

    def _delete(self, selection):
        q = messagebox.askyesno('Delete Sale', f'Deleted sales cannot be retrieved\nWould you like to permanently delete {selection}?',
                                parent=self.top)
        if q:
            sale = self.p.sale_names_frames[selection].sale
            sqlt.delete_sale(self.p.db, sale)
            self.p.post_commit_updates(from_sale_tools=True)
        self.top.destroy()
