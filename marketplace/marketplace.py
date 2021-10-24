from collections import namedtuple

Marketplace = namedtuple(
    'Marketplace',
    [
        'filename_regexp', 'display_name', 'column_mapping',
        'originators_rename', 'header', 'skipfooter'
    ]
)

COUNTRY = 'Country'
LOAN_ORIGINATOR = 'Loan originator'
OUTSTANDING_PRINCIPAL = 'Outstanding principal'
INTEREST_RATE = 'Interest rate'
