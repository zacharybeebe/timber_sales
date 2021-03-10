import tkinter as t
from tkinter import ttk, filedialog, messagebox
import math
from sql_tools import sqlt
from parameters import *
from sale import Sale
from unit import Unit
from purchaser import Purchaser



class Sale_Frame(object):
    def __init__(self, program, sale):
        self.p = program
        self.sale = sale
        self.sale_color = SEAGREEN
        self.unit_color = PALEGREEN
        self.get_lists_dicts_frame()
        self.get_sale_data()
        self.create_sale_frame()



    def _format_date(self, date):
        return f'{date.month}/{date.day}/{date.year}'

    def get_lists_dicts_frame(self):
        self.all_widgets = []
        self.sale_widgets = []
        self.unit_widgets = []
        self.edit_widgets = []

        self.calls = {'FY': self.sale.fy,
                      'MBF': math.floor(self.sale.mbf / 1000) * 1000,
                      'MBF_AC': math.floor(self.sale.mbf_ac / 5) * 5,
                      'TRUST': self.sale.trusts}

    def get_sale_data(self):
       #[Editable, Sale Attribute, Error Check Func, Sale Update Func]
       self.sale_data = [[True, self.sale.name, self._err_name_blank, self.sale.update_name, 'NAME'],
                         [True, self.sale.format_currency(self.sale.est_val_mbf), self._err_sale_currency, self.sale.update_est_mbf, '$MBF'],
                         [True, self._format_date(self.sale.auction), self._err_sale_auction, self.sale.update_auction_date, 'AUCTION'],
                         [False, self.sale.fy],
                         [False, self._format_date(self.sale.field_work_due)],
                         [False, round(self.sale.acres, 1)],
                         [False, int(round(self.sale.mbf, 0))],
                         [False, round(self.sale.mbf_ac, 1)],
                         [False, self.sale.format_currency(self.sale.est_val)]]



    def create_sale_frame(self):
        frame_height = SALE_UHEIGHT * (len(self.sale.units) + 2)
        self.frame = t.Frame(self.p.canvas_sales_frame, bg=GREY, height=SALE_UHEIGHT, width=int(self.p.canvas_sales.winfo_width()))
        self.frame.units_height = frame_height

        self._sale_expand_button()
        self._sale_edit_button()
        self._sale_labels()
        self._units()
        self.frame.update()
        self.p.root.update()

    def _sale_expand_button(self):
        button = t.Button(self.frame, text='v', font=font10Cb, bg=self.sale_color)
        button['command'] = lambda fr=self.frame, b=button: self.toggle_sale_frame(b)
        button.coords = [0, 0, (SALE_HEADER[0][0]*self.p.header_frame.winfo_width() // 2), SALE_UHEIGHT]
        self.all_widgets.append(button)
        self.p.root.update()

    def _sale_edit_button(self):
        button = t.Button(self.frame, text='/', font=font10Cb, bg=self.sale_color)
        button.coords = [(SALE_HEADER[0][0] * self.p.header_frame.winfo_width() // 2), 0,
                         (SALE_HEADER[0][0] * self.p.header_frame.winfo_width() // 2), SALE_UHEIGHT]
        button['command'] = lambda b=button: self.toggle_edits(b, code=1)

        self.all_widgets.append(button)
        self.p.root.update()

    def _sale_labels(self):
        x = (SALE_HEADER[0][0] * self.p.header_frame.winfo_width() // 1)
        for i, dat in enumerate(self.sale_data):
            label = t.Label(self.frame, font=font10Cb, bg=self.sale_color, fg=BLACK, text=dat[1], borderwidth=0.5, relief='solid')
            label.background = self.sale_color
            label.coords = [x, 0, (SALE_HEADER[i+1][0] * self.p.header_frame.winfo_width() // 1), SALE_UHEIGHT]
            self.all_widgets.append(label)

            if dat[0]:
                label.class_ = self.sale
                label.edits = [None, 'SALE', dat[2], dat[3], None]
                self.sale_widgets.append(label)

            self.p.root.update()
            x += (SALE_HEADER[i+1][0] * self.p.header_frame.winfo_width() // 1)

    def _units(self):
        self._unit_head_add_button()
        self._unit_head_edit_all_button()
        self._unit_head_labels()

        y = SALE_UHEIGHT * 2
        for u in sorted(self.sale.units):
            unit = self.sale.units[u][1]
            unit_data = self._units_get_unit_data(unit)
            x = int(UNIT_HEADER[0][0] * self.p.header_frame.winfo_width())
            for i, data in enumerate(unit_data):
                if i == 0:
                    self._units_unit_delete_button(unit, y)
                    self._units_unit_edit_button(unit, y)
                else:
                    self._units_data_label(unit, x, y, i, data)
                    x += int(UNIT_HEADER[i][0] * self.p.header_frame.winfo_width())
            y += SALE_UHEIGHT

    def _unit_head_add_button(self):
        width = int(UNIT_HEADER[0][0] * self.p.header_frame.winfo_width() // 2)
        button = t.Button(self.frame, text='+', font=font10Cb, bg=self.unit_color, command=lambda: self.create_unit())
        button.coords = [0, SALE_UHEIGHT, width, SALE_UHEIGHT]
        self.all_widgets.append(button)
        self.p.root.update()

    def _unit_head_edit_all_button(self):
        width = int(UNIT_HEADER[0][0] * self.p.header_frame.winfo_width() // 2)
        button = t.Button(self.frame, text='/', font=font10Cb, bg=self.unit_color)
        button.coords = [width, SALE_UHEIGHT, width, SALE_UHEIGHT]
        button['command'] = lambda b=button: self.toggle_edits(b, code=2)
        self.all_widgets.append(button)
        self.p.root.update()

    def _unit_head_labels(self):
        x_pos = int(UNIT_HEADER[0][0] * self.p.header_frame.winfo_width())
        for i in range(1, len(UNIT_HEADER)):
            width = int(UNIT_HEADER[i][0] * self.p.header_frame.winfo_width() // 1)
            label = t.Label(self.frame, font=font7Cb, text=str(UNIT_HEADER[i][1]), borderwidth=0.5, relief='solid')
            label.coords = [x_pos, SALE_UHEIGHT, width, SALE_UHEIGHT]
            self.all_widgets.append(label)
            self.p.root.update()
            x_pos += width

    def _units_unit_delete_button(self, unit, y):
        width = int(UNIT_HEADER[0][0] * self.p.header_frame.winfo_width() // 2)
        button = t.Button(self.frame, text='X', font=font10Cb, bg=self.unit_color)
        button.id = y
        button.unit = unit
        button.coords = [0, y, width, SALE_UHEIGHT]
        button['command'] = lambda b=button: self.delete_unit(b)
        self.all_widgets.append(button)
        self.p.root.update()

    def _units_unit_edit_button(self, unit, y):
        width = int(UNIT_HEADER[0][0] * self.p.header_frame.winfo_width() // 2)
        button = t.Button(self.frame, text='/', font=font10Cb, bg=self.unit_color)
        button.id = y
        button.unit = unit
        button.coords = [width, y, width, SALE_UHEIGHT]
        button['command'] = lambda b=button: self.toggle_edits(b, code=3)
        self.all_widgets.append(button)
        self.p.root.update()

    def _units_data_label(self, unit, x, y, index, data):
        label = t.Label(self.frame, bg=self.unit_color, fg=BLACK, font=font10Cb, text=data[0], borderwidth=0.5, relief='solid')
        label.id = y
        label.background = self.unit_color
        label.coords = [x, y, int(UNIT_HEADER[index][0] * self.p.header_frame.winfo_width()), SALE_UHEIGHT]
        label.class_ = unit
        #CHECKING FOR NEW UNIT ADDED
        if index == 2 and data[0] == '':
            label.edits = ['', 'UNIT', data[1], data[2], data[3]]
            self.edit_widgets.append(label)
            if self not in self.p.sale_edits:
                self.p.sale_edits.append(self)
        else:
            label.edits = [None, 'UNIT', data[1], data[2], data[3]]
        self.all_widgets.append(label)
        self.unit_widgets.append(label)
        self.p.root.update()

    def _units_get_unit_data(self, unit):
        unit_data = [[None],
                     [unit.name, self._err_name_blank, unit.update_name, None],
                     [unit.harvest, self._err_unit_harvest, unit.update_harvest, None]]

        for trust in TRUST_CODES:
            if trust in unit.trusts:
                unit_data.append([round(unit.trusts[trust][ACRES], 1), self._err_float_check, unit.update_trust_acres, trust])
                unit_data.append([int(round(unit.trusts[trust][MBF], 0)), self._err_float_check, unit.update_trust_mbf, trust])
            else:
                unit_data.append(['', self._err_float_check, unit.update_trust_acres, trust])
                unit_data.append(['', self._err_float_check, unit.update_trust_mbf, trust])
        return unit_data



    def toggle_sale_frame(self, button):
        if button['text'] == 'v':
            button['text'] = '^'
        else:
            button['text'] = 'v'

        if self.frame['height'] > SALE_UHEIGHT + self.frame['highlightthickness']:
            self.frame['height'] = SALE_UHEIGHT + self.frame['highlightthickness']
        else:
            self.frame['height'] = self.frame.units_height + self.frame['highlightthickness']
        self.frame.update()

        self.p.canvas_sales['scrollregion'] = self.p.canvas_sales.bbox("all")
        self.p.canvas_sales.update()
        self.p.root.update()

    def toggle_edits(self, button, code=1):
        if code == 1:
            for widget in self.sale_widgets:
                self._toggle_edits_widgets(widget, code)
        elif code == 2:
            for widget in self.unit_widgets:
                self._toggle_edits_widgets(widget, code)
        else:
            for widget in self.unit_widgets:
                if widget.id == button.id:
                    self._toggle_edits_widgets(widget, code)

    def _toggle_edits_widgets(self, widget, code):
        if isinstance(widget, t.Label):
            entry = self._toggle_edits_entry(widget)
            if code != 1:
                entry.id = widget.id
            self._toggle_edits_update_frame_widgets(widget, entry, code)
        else:
            label = self._toggle_edits_label(widget)
            if code != 1:
                label.id = widget.id
            self._toggle_edits_update_frame_widgets(widget, label, code)

        widget.destroy()
        self.p.root.update()

    def _toggle_edits_entry(self, widget):
        sv = t.StringVar()
        sv.set(widget['text'])
        entry = t.Entry(self.frame, font=font10Cb, fg=widget['fg'], textvariable=sv)
        entry.background = widget.background
        entry.coords = widget.coords
        entry.class_ = widget.class_
        entry.edits = widget.edits
        sv.trace("w", lambda name, index, mode, sv=sv, e=entry: self.add_sale_to_edits(sv, e))
        entry.place(x=entry.coords[0], y=entry.coords[1], width=entry.coords[2], height=entry.coords[3])
        return entry

    def _toggle_edits_label(self, widget):
        label = t.Label(self.frame, bg=widget.background, fg=widget['fg'], font=font10Cb, text=widget.get(), borderwidth=0.5, relief='solid')
        label.background = widget.background
        label.coords = widget.coords
        label.class_ = widget.class_
        label.edits = widget.edits
        label.place(x=label.coords[0], y=label.coords[1], width=label.coords[2], height=label.coords[3])
        return label

    def _toggle_edits_update_frame_widgets(self, old_widget, new_widget, code):
        if old_widget in self.edit_widgets:
            self.edit_widgets.insert(self.edit_widgets.index(old_widget), new_widget)
            self.edit_widgets.remove(old_widget)

        self.all_widgets.insert(self.all_widgets.index(old_widget), new_widget)
        self.all_widgets.remove(old_widget)
        if code == 1:
            self.sale_widgets.insert(self.sale_widgets.index(old_widget), new_widget)
            self.sale_widgets.remove(old_widget)
        else:
            self.unit_widgets.insert(self.unit_widgets.index(old_widget), new_widget)
            self.unit_widgets.remove(old_widget)



    def delete_unit(self, button):
        question = messagebox.askyesno('Delete Unit',
                                       f'Are you sure you would like to delete\n{button.unit.name} from {self.sale.name}?')
        if question:
            self.sale.delete_unit(button.unit)
            self.refresh_sale_frame()
        else:
            return

    def create_unit(self):
        Unit(self.sale, self._create_unit_get_name(), '', [['01', 1, 1]])
        self.refresh_sale_frame()

    def _create_unit_get_name(self):
        u_num_list = [key for key in self.sale.units]
        return f'U{max(u_num_list) + 1}'



    def error_check(self, list_to_append):
        for widget in self.edit_widgets:
            if not widget.edits[2](widget.edits[0]):
                if widget.edits[0] == '':
                    list_to_append.append([widget, 'bg', RED])
                else:
                    list_to_append.append([widget, 'fg', RED])

    def _err_name_blank(self, value):
        if value == '':
            return False
        else:
            return True

    def _err_int_check(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    def _err_float_check(self, value):
        if value == '':
            return True
        else:
            try:
                float(value)
                return True
            except ValueError:
                return False

    def _err_sale_currency(self, value):
        try:
            float(value)
            return True
        except ValueError:
            try:
                rep1 = value.replace('$', '')
                float(rep1.replace(',', ''))
                return True
            except ValueError:
                return False

    def _err_sale_auction(self, value):
        delimiters = [',', '.', '/', '-', '_', ':', ';', '?', '|', '~', '`']
        try:
            month, day, year = value[:2], value[2:4], value[4:]
            month, day, year = int(month), int(day), int(year)
            return True
        except:
            for i in delimiters:
                try:
                    month, day, year = value.split(i)
                    month, day, year = int(month), int(day), int(year)
                    return True
                except:
                    next
            else:
                return False

    def _err_unit_harvest(self, value):
        harvest = ['VRH', 'VDT', 'ROW']
        if value.upper() in harvest:
            return True
        else:
            return False



    def refresh_sale_frame(self):
        self.sale.reorder_units()
        self.sale.calc_trusts()

        sale_frame_index = self.p.sale_frames.index(self)
        active_frame_index = self.p.active_frames.index(self)

        sqlt.update_sale(self.p.db, self.sale)

        self.p.sale_frames.remove(self)
        self.p.active_frames.remove(self)
        self.frame.destroy()

        self.get_lists_dicts_frame()
        self.get_sale_data()
        self.create_sale_frame()
        self.p.sale_frames.insert(sale_frame_index, self)
        self.p.active_frames.insert(active_frame_index, self)

        for widget in self.all_widgets:
            widget.place(x=widget.coords[0], y=widget.coords[1], width=widget.coords[2], height=widget.coords[3])
        self.frame.grid(row=self.sale.sort_id, column=0)
        self.p.canvas_sales_frame.update()
        self.p.canvas_sales['scrollregion'] = self.p.canvas_sales_frame.bbox("all")
        self.p.canvas_sales.update()
        self.p.root.update()

    def add_sale_to_edits(self, sv, entry):
        self.p.root.title(f'*{PROGRAM} v{VERSION}*')
        entry.config(fg=BLACK, bg=WHITE)
        entry.edits[0] = entry.get()
        if entry not in self.edit_widgets:
            self.edit_widgets.append(entry)

        if self not in self.p.sale_edits:
            self.p.sale_edits.append(self)

    def commit_edits(self):
        for widget in self.edit_widgets:
            if widget.edits[-1] is None:
                widget.edits[3](widget.edits[0])
            else:
                if widget.edits[0] == '':
                    widget.class_.delete_trust(widget.edits[-1])
                else:
                    widget.edits[3](widget.edits[-1], widget.edits[0])

        self.refresh_sale_frame()







