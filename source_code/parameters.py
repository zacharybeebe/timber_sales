
PROGRAM = 'Timber Sales'
VERSION = '0.1 beta'

SCREEN_POS_RIGHT = 40
SCREEN_POS_DOWN = 25
WIDTH = 1440
HEIGHT = 720

#SQLITE3 DATA TYPES
TXT = 'TEXT'
INT = 'INTEGER'
RL = 'REAL'
BB = 'BLOB'

CREATE_SALE_COLS = [['SORT_ID', INT], ['SALE', TXT], ['FISCAL_YEAR', INT], ['AUCTION_DATE', TXT], ['FIELD_WORK_DUE', TXT], ['object', BB]]
CREATE_PURCHASER_COLS = [['PURCHASER', TXT], ['object', BB]]

# SALE-PURCHASER-UNIT DICTIONARY CONSTANTS
ACRES = 'ACRES'
HARVEST = 'HARVEST'
MBF = 'MBF'
MBF_AC = 'MBF_AC'
TRUSTS = 'TRUSTS'

WIN = 'WIN'
BID = 'BID'
BID_MBF = 'BID_MBF'
BID_ACRES = 'BID_ACRES'
OB = 'OVERBID'
OB_MBF = 'OVERBID_MBF'
OB_ACRES = 'OVERBID_ACRES'
OB_PCT = 'OVERBID_PCT'
PURCHASER = 'PURCHASER_CLASS'

SALE_HEADER = [(0.03, ''), (0.1, 'SALE'), (0.1, '$/MBF'), (0.1, 'AUCTION'),
               (0.1, 'FY'), (0.1, 'FIELD WORK'), (0.1, ACRES), (0.1, MBF), (0.1, 'MBF/AC'), (0.17, 'REVENUE')]

TRUST_CODES = ['01', '03', '06', '07', '08', '09', '10', '11', '12', '77']

UNIT_HEADER = [(0.03, ''), (0.075, 'NAME'), (0.075, 'HARVEST'), (0.041, '01 ACRES', '01'), (0.041, '01 MBF', '01'),
               (0.041, '03 ACRES', '03'), (0.041, '03 MBF', '03'), (0.041, '06 ACRES', '06'), (0.041, '06 MBF', '06'),
               (0.041, '07 ACRES', '07'), (0.041, '07 MBF', '07'), (0.041, '08 ACRES', '08'), (0.041, '08 MBF', '08'),
               (0.041, '09 ACRES', '09'), (0.041, '09 MBF', '09'), (0.041, '10 ACRES', '10'), (0.041, '10 MBF', '10'),
               (0.041, '11 ACRES', '11'), (0.041, '11 MBF', '11'), (0.041, '12 ACRES', '12'), (0.041, '12 MBF', '12'),
               (0.041, '77 ACRES', '77'), (0.041, '77 MBF', '77')]


SALE_SV_VALS = ['NAME', 'FY', '$/MBF', 'AUCTION']

UNIT_SV_VALS = ['NAME', 'HARVEST', '01 ACRES', '01 MBF', '03 ACRES', '03 MBF',
                 '06 ACRES', '06 MBF', '07 ACRES', '07 MBF', '08 ACRES', '08 MBF',
                 '09 ACRES', '09 MBF', '10 ACRES', '10 MBF', '11 ACRES', '11 MBF',
                 '12 ACRES', '12 MBF', '77 ACRES', '77 MBF']


DNR_REVENUE = {'01': 0.25, '03': 0.31, '06': 0.31, '07': 0.31, '08': 0.31, '09': 0.31, '10': 0.31, '11': 0.31, '12': 0.31, '77': 0.25}
TRUST_REVENUE = {'01': 0.75, '03': 0.69, '06': 0.69, '07': 0.69, '08': 0.69, '09': 0.69, '10': 0.69, '11': 0.69, '12': 0.69, '77': 0.75}


SALE_UHEIGHT = 20


BLACK = '#000000'
RED = '#FF0000'
DARKRED = '#A10C0C'
GREY = '#E1E1E1'
WHITE = '#FFFFFF'
FORESTGREEN = '#418A52'
PALEGREEN = '#CCFFE5'
SEAGREEN = '#99FFCC'
DSEAGREEN = '#0DE3A4'



font_name = 'Calibri'

font5Cb = (font_name, "5", "bold")
font6Cb = (font_name, "6", "bold")
font7Cb = (font_name, "7", "bold")
font7_5Cb = (font_name, "7.5", "bold")
font8Cb = (font_name, "8", "bold")
font10Cb = (font_name, "10", "bold")
font11Cb = (font_name, "11", "bold")
font12Cb = (font_name, "12", "bold")
font14Cb = (font_name, "14", "bold")
font18Cb = (font_name, "18", "bold")
font24Cb = (font_name, "24", "bold")
font36Cb = (font_name, "36", "bold")

FONT_DICT = {'font5': font5Cb,
             'font6': font6Cb,
             'font7': font7Cb,
             'font8': font8Cb,
             'font10': font10Cb,
             'font11': font11Cb,
             'font12': font12Cb,
             'font14': font14Cb,
             'font18': font18Cb,
             'font36': font36Cb}



