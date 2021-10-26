import re
from marketplace import marketplace

MARKETPLACE_NAME = 'iuvo'
MARKETPLACE_META_DATA = marketplace.Marketplace(
    filename_regexp=re.compile(r'MyInvestments-(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2}).xlsx'),
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
