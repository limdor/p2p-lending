import re
from marketplace import marketplace

META_DATA = marketplace.Marketplace(
    name='iuvo',
    filename_regexp=re.compile(r'[Mm]y_*[Ii]nvestments[-_](page_)*(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})(-\d*)*.xlsx'),
    display_name='IUVO',
    column_mapping={
        'Country': marketplace.COUNTRY,
        'Originator': marketplace.LOAN_ORIGINATOR,
        'Outstanding principal': marketplace.OUTSTANDING_PRINCIPAL,
        'Interest Rate (%)': marketplace.INTEREST_RATE
    },
    originators_rename={'iCredit Poland': 'iCredit', 'iCredit Romania': 'iCredit'},
    header=3,
    skipfooter=3)
