import re
import marketplace.marketplace as marketplace

MARKETPLACE_NAME = 'mintos'
MARKETPLACE_META_DATA = marketplace.Marketplace(
    filename_regexp=re.compile(r'(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})-current-investments.xlsx'),
    display_name='Mintos',
    # TODO: There might be money in 'Pending Payments' column even if the investment is not finished
    column_mapping={
        'Country': marketplace.COUNTRY,
        'Loan Originator': marketplace.LOAN_ORIGINATOR,
        'Lending Company': marketplace.LOAN_ORIGINATOR,
        'Outstanding Principal': marketplace.OUTSTANDING_PRINCIPAL,
        'Interest Rate': marketplace.INTEREST_RATE
    },
    originators_rename=None,
    header=0,
    skipfooter=0)
