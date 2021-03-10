import tkinter as t
from tkinter import ttk, filedialog, messagebox
import os
import math
from parameters import *
from sql_tools import *
from p_sale_frame import Sale_Frame
from p_sale_tools import New_Sale, Delete_Sale
from p_reports import Trust_FY
from p_tools import Unit_LRM_MBF, Swap_Sales


class Program(object):
    def __init__(self):
        self.path = os.getcwd()
        self.db = self.path +'\TIMBER_SALES.db'
        self.root = t.Tk()

        self.root.title('{} v{}'.format(PROGRAM, VERSION))

        self.sale_edits = []
        self.sales_sorted = sorted([[i.sort_id, i.name, i] for i in sqlt.select_obj_col(self.db, 'SALES')], key=self.sort_sale_key)
        self.active_frames = []

        self.listbox_selected = None
        self.current_listbox_selection = None

        self.main_frame_format()
        self.menu_format()
        self.frame_tools_format()
        self.frame_sales_format()

        self.sale_frames = [Sale_Frame(self, i[2]) for i in self.sales_sorted]
        self.sale_names_frames = {sale_frame.sale.name: sale_frame for sale_frame in self.sale_frames}


    def sort_sale_key(self, element):
        return element[0]

    def main_frame_format(self):
        self.root.geometry("+{}+{}".format(SCREEN_POS_RIGHT, SCREEN_POS_DOWN))
        #self.root.iconbitmap(self.icon)

        self.main_canvas = t.Canvas(self.root, bg=BLACK, width=WIDTH, height=HEIGHT)
        self.main_canvas.pack(side='left', fill='both')

        self.menu = t.Menu(self.root)
        self.root.config(menu=self.menu)

    def menu_format(self):
        menus = {'Sale': [('New Sale', self.p_sale_new_sale),
                          ('Delete Sale', self.p_sale_delete_sale)],

                 'Tools': [('Swap Sales', self.p_tools_swap_sales),
                           ('Unit LRM MBF', self.p_tools_unit_lrm_mbf)],

                 'Reports': [('Trust Volume by FY', self.p_report_trust_vol_fy)]}

        for key in menus:
            menu = t.Menu(self.menu, tearoff=False)
            self.menu.add_cascade(label=key, menu=menu)
            for i in menus[key]:
                menu.add_command(label=i[0], command=i[1])
            menu.add_separator()



    def frame_tools_format(self):
        self.frame_tools = t.Frame(self.main_canvas, bg=PALEGREEN, bd=5)
        self.frame_tools.place(x=0, relwidth=0.15, relheight=1.0)
        self.root.update()
        self.frame_tools.listboxes = []

        commit = t.Button(self.frame_tools, font=font10Cb, text='COMMIT', command=self.commit_changes)
        commit.place(x=0, y=0, relwidth=1.0, relheight=0.1)
        self.listbox_format()

    def listbox_format(self):
        lb_list = self._listbox_lists()
        x = 0
        for i in lb_list:
            label = t.Label(self.frame_tools, bg=PALEGREEN, text=i[0], font=font10Cb)
            label.place(x=int(x * self.frame_tools.winfo_width()), y=int(0.1*self.frame_tools.winfo_height()), relwidth=0.25)
            self.root.update()

            listbox = t.Listbox(self.frame_tools, selectmode='multiple')
            listbox.call = i[0]
            listbox.placey = int(0.1*self.frame_tools.winfo_height()) + label.winfo_height()
            listbox.place(x=int(x * self.frame_tools.winfo_width()), y=listbox.placey,
                          relwidth=0.25, relheight=(0.115 / 5) * len(i[1]))
            listbox.bind('<Enter>', self._listbox_bound)
            listbox.bind('<Leave>', self._listbox_unbound)
            for j in i[1]:
                listbox.insert('end', j)
            x += 0.25
            self.frame_tools.listboxes.append(listbox)

    def listbox_manipulation(self, listbox, normal=True):
        if normal:
            self._listbox_normal_refresh(listbox)
        else:
            self._listbox_commit_refresh(listbox)

    def _listbox_lists(self):
        lb_list = [['FY', {i[2].fy for i in self.sales_sorted}],
                   ['MBF', sorted({(math.floor(i[2].mbf / 1000) * 1000) for i in self.sales_sorted})],
                   ['MBF_AC', sorted({(math.floor(i[2].mbf_ac / 5) * 5) for i in self.sales_sorted})],
                   ['TRUST', TRUST_CODES]]
        return lb_list

    def _listbox_bound(self, event):
        event.widget['exportselection'] = True
        event.widget.bind_all("<<ListboxSelect>>", self._listbox_from_button)

    def _listbox_unbound(self, event):
        event.widget['exportselection'] = False
        event.widget.unbind_all("<<ListboxSelect>>")

    def _listbox_from_button(self, event):
        self.listbox_manipulation(event.widget, normal=True)

    def _listbox_get_call_list(self, listbox, selected):
        if listbox.call != 'TRUST':
            forget_frames = [frame for frame in self.active_frames if frame.calls[listbox.call] not in selected]
            show_frames = [frame for frame in self.sale_frames if frame.calls[listbox.call] in selected]
        else:
            forget_frames = []
            for frame in self.active_frames:
                for trust in frame.calls['TRUST']:
                    if trust in selected:
                        break
                forget_frames.append(frame)
            show_frames = []
            for frame in self.sale_frames:
                for trust in frame.calls['TRUST']:
                    if trust in selected:
                        show_frames.append(frame)
                        break
        return forget_frames, show_frames

    def _listbox_grid_frames(self, show_frames):
        self.active_frames = []
        for frame in show_frames:
            self.active_frames.append(frame)
            for widget in frame.all_widgets:
                widget.place(x=widget.coords[0], y=widget.coords[1], width=widget.coords[2], height=widget.coords[3])
            frame.frame.grid(row=frame.sale.sort_id, column=0)
            self.canvas_sales_frame.update()
        self.canvas_sales['scrollregion'] = self.canvas_sales_frame.bbox("all")
        self.canvas_sales.update()
        self.root.update()

    def _listbox_commit_refresh(self, listbox):
        self.listbox_selected = listbox
        if self.current_listbox_selection is not None:
            selected = self.current_listbox_selection
            _, show_frames = self._listbox_get_call_list(listbox, selected)
            for frame in self.active_frames:
                frame.frame.grid_forget()
            self._listbox_grid_frames(show_frames)

    def _listbox_normal_refresh(self, listbox):
        self.listbox_selected = listbox
        selection = listbox.curselection()
        if selection:
            selected = [listbox.get(i) for i in selection]
            self.current_listbox_selection = selected
            forget_frames, show_frames = self._listbox_get_call_list(listbox, selected)
            for frame in forget_frames:
                frame.frame.grid_forget()
            self._listbox_grid_frames(show_frames)
        else:
            for frame in self.active_frames:
                frame.frame.grid_forget()
            self.active_frames = []



    def frame_sales_format(self):
        self.frame_sales_overall = t.Frame(self.main_canvas, bg=SEAGREEN, bd=5)
        self.frame_sales_overall.place(x = int(WIDTH * 0.15), relwidth=0.85, relheight=1.0)

        self.header_frame = t.Frame(self.frame_sales_overall, bg=FORESTGREEN, height=SALE_UHEIGHT)
        self.header_frame.pack(side='top', fill='x')
        self.root.update()

        x = 0
        for i, head in enumerate(SALE_HEADER):
            label = t.Label(self.header_frame, font=font8Cb, text=head[1], borderwidth=0.5, relief='solid')
            label.place(x=(x*self.header_frame.winfo_width()), relwidth=head[0], relheight=1.0)
            x += head[0]
            self.root.update()

        self.canvas_sales = t.Canvas(self.frame_sales_overall, bg=DSEAGREEN, highlightthickness=0)
        self.canvas_sales.pack(side='left', expand=1, fill='both')

        self.canvas_sales.bind('<Enter>', self._canvas_sales_bound)
        self.canvas_sales.bind('<Leave>', self._canvas_sales_unbound)
        self.root.update()

        self.scrollbar_sales = ttk.Scrollbar(self.frame_sales_overall, orient='vertical', command=self.canvas_sales.yview)
        self.scrollbar_sales.pack(side='right', fill='y')

        self.canvas_sales.config(yscrollcommand=self.scrollbar_sales.set)
        self.canvas_sales.bind('<Configure>', lambda e: self.canvas_sales.configure(scrollregion=self.canvas_sales.bbox("all")))

        self.canvas_sales_frame = t.Frame(self.canvas_sales, bg=DSEAGREEN)
        self.canvas_sales_frame.pack()
        self.canvas_sales.create_window((0, 0), window=self.canvas_sales_frame, anchor="nw")
        self.root.update()

    def _canvas_sales_bound(self, event):
        self.canvas_sales.bind_all('<MouseWheel>', self._canvas_sales_on_mousewheel)

    def _canvas_sales_unbound(self, event):
        self.canvas_sales.unbind_all('<MouseWheel>')

    def _canvas_sales_on_mousewheel(self, event):
        if self.canvas_sales.bbox("all")[3] > self.frame_sales_overall.winfo_height():
            self.canvas_sales.yview_scroll(int(-1 * (event.delta / 120)), "units")
            self.root.update()



    def commit_changes(self):
        widget_err_list = []
        for sale_frame in self.sale_edits:
            sale_frame.error_check(widget_err_list)

        if len(widget_err_list) > 0:
            messagebox.showerror('Value Errors', 'One or more values are missing or incorrect')
            for i in widget_err_list:
                i[0][i[1]] = i[2]
            return
        else:
            for sale_frame in self.sale_edits:
                sale_frame.commit_edits()
            self.post_commit_updates()

    def post_commit_updates(self, from_sale_tools=False):
        self.root.title(f'{PROGRAM} v{VERSION}')
        self.sale_edits = []
        self.sales_sorted = sorted([[i.sort_id, i.name, i] for i in sqlt.select_obj_col(self.db, 'SALES')], key=self.sort_sale_key)
        self.sale_frames = [Sale_Frame(self, i[2]) for i in self.sales_sorted]
        self.sale_names_frames = {sale_frame.sale.name: sale_frame for sale_frame in self.sale_frames}

        if self.listbox_selected is not None:
            self.listbox_manipulation(self.listbox_selected, normal=False)

        if not from_sale_tools:
            lb_list = self._listbox_lists()
            x = 0
            for i, lb in enumerate(self.frame_tools.listboxes):
                lb.delete(0, 'end')
                for j in lb_list[i][1]:
                    lb.insert('end', j)
                lb.place_forget()
                lb.place(x=int(x * self.frame_tools.winfo_width()), y=lb.placey, relwidth=0.25, relheight=(0.115 / 5) * len(lb_list[i][1]))
                x += 0.25



    def p_sale_new_sale(self):
        New_Sale(self)

    def p_sale_delete_sale(self):
        Delete_Sale(self)



    def p_tools_swap_sales(self):
        Swap_Sales(self)

    def p_tools_unit_lrm_mbf(self):
        Unit_LRM_MBF(self)



    def p_report_trust_vol_fy(self):
        Trust_FY(self)



















































