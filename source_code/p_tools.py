import tkinter as t
from tkinter import ttk, filedialog, messagebox
from sql_tools import sqlt
from parameters import *




class Unit_LRM_MBF(object):
    """Gets desired MBF for the sale (to be submitted in LRM) and calculates the desired unit MBF from the proportion of
       current unit MBF to the current total sale MBF. Splits desired unit MBF amounts further, for user-defined
       Conifer and Hardwood percentages"""

    def __init__(self, program):
        self.p = program
        self.run()

    def run(self):
        self.top = t.Toplevel(self.p.root)
        self.top.geometry("+{}+{}".format(SCREEN_POS_RIGHT + 250, SCREEN_POS_DOWN + 150))
        self.top.transient(self.p.root)

        self.frame = t.Frame(self.top, bg=SEAGREEN, height=SALE_UHEIGHT * 15, width=600)
        self.frame.compiled_labels = []
        self.frame.pack()

        head = t.Label(self.frame, bg=SEAGREEN, font=font10Cb, text='UNIT LRM MBF')
        head.place(x=0, y=0, width=100, height=SALE_UHEIGHT)

        menu_head = t.StringVar()
        menu_head.set("Select Sale")
        menu = t.OptionMenu(self.frame, menu_head, (*self.p.sale_names_frames), command=self._stand_info)
        menu.place(x=0, y=SALE_UHEIGHT, width=150, height=SALE_UHEIGHT*2)

    def _stand_info(self, selection):
        if len(self.frame.compiled_labels) > 0:
            for i in range(len(self.frame.compiled_labels)):
                self.frame.compiled_labels.pop(0).destroy()

        cur_mbf_lab = t.Label(self.frame, bg=SEAGREEN, font=font10Cb, text='Current MBF:', justify='left')
        cur_mbf_lab.place(x=0, y=SALE_UHEIGHT*3, width=75, height=SALE_UHEIGHT)
        self.top.update()
        cur_mbf = t.Label(self.frame, bg=SEAGREEN, font=font10Cb,
                          text=int(round(self.p.sale_names_frames[selection].sale.mbf, 0)))
        cur_mbf.place(x=cur_mbf_lab.winfo_width()+10, y=SALE_UHEIGHT * 3, width=75, height=SALE_UHEIGHT)
        self.top.update()

        entry_labs = [['LRM MBF:', ''], ['Conifer %', '90'], ['Hardwood %', '10']]
        entries = []
        y = SALE_UHEIGHT * 4
        for i in entry_labs:
            label = t.Label(self.frame, bg=SEAGREEN, font=font10Cb, justify='left', text=i[0])
            label.place(x=0, y=y, width=75, height=SALE_UHEIGHT)
            self.top.update()
            entry = t.Entry(self.frame,font=font10Cb)
            entry.insert('end', i[1])
            entry.place(x=label.winfo_width()+10, y=y, width=75, height=SALE_UHEIGHT)
            entries.append(entry)
            self.top.update()
            y += SALE_UHEIGHT

        submit = t.Button(self.frame, font=font10Cb, text='Calculate',
                          command=lambda s=selection, e=entries: self._compile(s, e))
        submit.place(x=0, y=y+10, width=75, height=SALE_UHEIGHT)

    def _compile(self, selection, entries):
        heads = ['UNIT', 'CONIFER MBF', 'HARDWOOD MBF']
        x = 150
        placement = []
        for i in heads:
            label = t.Label(self.frame, bg=SEAGREEN, font=font10Cb, text=i)
            label.coords = [x, 0, 120, SALE_UHEIGHT]
            label.place(x=label.coords[0], y=label.coords[1], width=label.coords[2], height=label.coords[3])
            self.frame.compiled_labels.append(label)
            placement.append(label.coords)
            x += label.coords[2]

        sorted_units, value_list, totals_list = self._calculate(selection, entries)
        self._labels(placement, sorted_units, value_list, totals_list)

    def _calculate(self, selection, entries):
        des_mbf, con, hwd = float(entries[0].get()), float(entries[1].get()) / 100, float(entries[2].get()) / 100
        cur_mbf = self.p.sale_names_frames[selection].sale.mbf
        units = self.p.sale_names_frames[selection].sale.units
        sorted_units = sorted(list(units))

        totals_list = ['TOTALS', 0, 0]
        val_list = []
        for unit in sorted_units:
            mbf_pct = units[unit][1].mbf / cur_mbf
            con_mbf = int(round(con * mbf_pct * des_mbf,0))
            hwd_mbf = int(round(hwd * mbf_pct * des_mbf,0))
            totals_list[1] += con_mbf
            totals_list[2] += hwd_mbf
            val_list.append([units[unit][0], con_mbf, hwd_mbf])

        if sum(totals_list[1:]) != int(des_mbf // 1):
            difference = sum(totals_list[1:]) - int(des_mbf // 1)
            if difference % 2 == 0:
                changecon = difference // 2
                changehwd = difference // 2
            else:
                changecon = difference // 2
                changehwd = difference - changecon
            totals_list[1] -= changecon
            totals_list[2] -= changehwd
            val_list[0][1] -= changecon
            val_list[0][2] -= changehwd
        return sorted_units, val_list, totals_list

    def _labels(self, placement, sorted_units, value_list, totals_list):
        y = 1
        for i, unit in enumerate(sorted_units):
            for j in range(3):
                label = t.Label(self.frame, bg=SEAGREEN, font=font10Cb, text=value_list[i][j])
                label.place(x=placement[j][0], y=placement[j][1]+(y*SALE_UHEIGHT), width=placement[j][2], height=placement[j][3])
                self.frame.compiled_labels.append(label)
            y += 1

        for i in range(3):
            label = t.Label(self.frame, bg=SEAGREEN, font=font10Cb, text=totals_list[i])
            label.place(x=placement[i][0], y=placement[i][1] + (y * SALE_UHEIGHT), width=placement[i][2], height=placement[i][3])
            self.frame.compiled_labels.append(label)



class Swap_Sales(object):
    """Swaps two sales by their auction dates"""

    def __init__(self, program):
        self.p = program
        self.run()

    def run(self):
        self.top = t.Toplevel(self.p.root)
        self.top.geometry("+{}+{}".format(SCREEN_POS_RIGHT + 250, SCREEN_POS_DOWN + 150))
        self.top.transient(self.p.root)

        self.frame = t.Frame(self.top, bg=SEAGREEN, height=SALE_UHEIGHT * 15, width=600)
        self.frame.pack()

        head = t.Label(self.frame, bg=SEAGREEN, font=font10Cb, text='SWAP SALES BY AUCTION DATE')
        head.place(x=0, y=0, width=200, height=SALE_UHEIGHT)

        menu_head = t.StringVar()
        menu_head.set("Select Sale")
        menu1 = t.OptionMenu(self.frame, menu_head, (*self.p.sale_names_frames), command=self._menu_change)
        menu1.place(x=0, y=SALE_UHEIGHT+10, width=150, height=SALE_UHEIGHT * 2)

        forr = t.Label(self.frame, bg=SEAGREEN, font=font24Cb, text='FOR')
        forr.place(x=150, y=SALE_UHEIGHT+10, width=150, height=SALE_UHEIGHT*2)

    def _menu_change(self, select):
        menu2_list = [sale_name for sale_name in self.p.sale_names_frames if sale_name != select]

        menu_head = t.StringVar()
        menu_head.set("Select Sale")
        menu2 = t.OptionMenu(self.frame, menu_head, (*menu2_list),
                             command=lambda selection, sel=select: self._submit_button(selection, sel=sel))
        menu2.place(x=300, y=SALE_UHEIGHT + 10, width=150, height=SALE_UHEIGHT * 2)

    def _submit_button(self, selection, **kwargs):
        sale_frame1 = self.p.sale_names_frames[kwargs['sel']]
        sale_frame2 = self.p.sale_names_frames[selection]

        submit = t.Button(self.frame, font=font10Cb, text='Swap')
        submit['command'] = lambda f1=sale_frame1, f2=sale_frame2: self.swap_commit(f1, f2)
        submit.place(x=475, y=SALE_UHEIGHT + 10 + (SALE_UHEIGHT//2), width=75, height=SALE_UHEIGHT)

    def swap_commit(self, sale_frame1, sale_frame2):
        auction_frame1 = sale_frame1.sale.auction
        auction_frame2 = sale_frame2.sale.auction

        sale_frame1.sale.update_auction_date(auction_frame2)
        sale_frame2.sale.update_auction_date(auction_frame1)

        sqlt.update_sale(self.p.db, sale_frame1.sale)
        sqlt.update_sale(self.p.db, sale_frame2.sale)

        self.p.post_commit_updates()
        self.top.destroy()