from typing import Any, NamedTuple

class Marketplace(NamedTuple):
    """
    Class that contains all static data needed to read information from a specific marketplace
    """
    name: str
    filename_regexp: Any
    display_name: str
    column_mapping: 'dict[str, str]'
    originators_rename: 'dict[str, str]'
    header: int
    skipfooter: int

    def __hash__(self):
        return hash(self.name)

COUNTRY = 'Country'
LOAN_ORIGINATOR = 'Loan originator'
OUTSTANDING_PRINCIPAL = 'Outstanding principal'
INTEREST_RATE = 'Interest rate'
FILE_DATE = 'Date'
INVESTMENT_PLATFORM = 'Investment platform'
