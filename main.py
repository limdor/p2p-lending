import pandas

COUNTRY = 'Country'
LOAN_ORIGINATOR = 'Loan originator'
OUTSTANDING_PRINCIPAL = 'Outstanding principal'
RELEVANT_COLUMNS = [COUNTRY, LOAN_ORIGINATOR, OUTSTANDING_PRINCIPAL]

def parse_investments(current_investments, column_mapping):
    current_investments = current_investments.rename(columns=column_mapping)

    current_investments = current_investments[RELEVANT_COLUMNS]
    sum_outstanding_principal = current_investments[OUTSTANDING_PRINCIPAL].sum()
    print(f"Current investment: {sum_outstanding_principal}")
    group_by_country = current_investments.groupby([COUNTRY]).sum()
    group_by_originator = current_investments.groupby([LOAN_ORIGINATOR]).sum()
    return group_by_country, group_by_originator

def main():
    print("**************************")
    print("**** IUVO Investments ****")
    print("**************************")
    IUVO_CURRENT_INVESTMENTS = "MyInvestments-20201213-193645.xlsx"
    IUVO_COLUMN_MAPPING = {'Country':COUNTRY, 'Originator': LOAN_ORIGINATOR, 'Outstanding principal':OUTSTANDING_PRINCIPAL}

    iuvo_investments = pandas.read_excel(IUVO_CURRENT_INVESTMENTS, header=3, skipfooter=3)
    iuvo_group_by_country, iuvo_group_by_originator = parse_investments(iuvo_investments, IUVO_COLUMN_MAPPING)
    print(iuvo_group_by_country)
    print(iuvo_group_by_originator)
    iuvo_group_by_originator = iuvo_group_by_originator.rename(index={'iCredit Poland': 'iCredit', 'iCredit Romania': 'iCredit'})

    print("****************************")
    print("**** Mintos Investments ****")
    print("****************************")
    MINTOS_CURRENT_INVESTMENTS = "20201213-current-investments.xlsx"
    # TODO: There might be money in 'Pending Payments' column even if the investment is not finished
    MINTOS_COLUMN_MAPPING = {'Country':COUNTRY, 'Loan Originator': LOAN_ORIGINATOR, 'Outstanding Principal':OUTSTANDING_PRINCIPAL}

    mintos_investments = pandas.read_excel(MINTOS_CURRENT_INVESTMENTS)
    mintos_group_by_country, mintos_group_by_originator = parse_investments(mintos_investments, MINTOS_COLUMN_MAPPING)
    print(mintos_group_by_country)
    print(mintos_group_by_originator)

    print("*****************************")
    print("**** Overall Investments ****")
    print("*****************************")
    overall_group_by_country = pandas.concat([iuvo_group_by_country, mintos_group_by_country]).groupby([COUNTRY]).sum()
    overall_group_by_originator = pandas.concat([iuvo_group_by_originator, mintos_group_by_originator]).groupby([LOAN_ORIGINATOR]).sum()
    total_invested_by_country = overall_group_by_country[OUTSTANDING_PRINCIPAL].sum()
    total_invested_by_originator = overall_group_by_originator[OUTSTANDING_PRINCIPAL].sum()
    assert(total_invested_by_country == total_invested_by_originator)
    #print(total_invested_by_country)
    overall_group_by_country['Percentage'] = overall_group_by_country[OUTSTANDING_PRINCIPAL] / total_invested_by_country
    print(overall_group_by_country.sort_values(by=OUTSTANDING_PRINCIPAL, ascending=False))
    overall_group_by_originator['Percentage'] = overall_group_by_originator[OUTSTANDING_PRINCIPAL] / total_invested_by_originator
    print(overall_group_by_originator.sort_values(by=OUTSTANDING_PRINCIPAL, ascending=False))

if __name__ == "__main__":
    main()
