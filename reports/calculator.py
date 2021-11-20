from marketplace import marketplace


def get_total_investment(investment_raw_data):
    return investment_raw_data[marketplace.OUTSTANDING_PRINCIPAL].sum()


def get_number_loan_parts(investment_raw_data):
    return len(investment_raw_data.index)


def get_percentage_investment_by_country(investment_raw_data):
    overall_group_by_country = investment_raw_data.groupby(marketplace.COUNTRY).sum()
    overall_group_by_country = overall_group_by_country.sort_values(by=marketplace.OUTSTANDING_PRINCIPAL, ascending=False)
    overall_group_by_country['Percentage'] = overall_group_by_country[marketplace.OUTSTANDING_PRINCIPAL] / (
        overall_group_by_country[marketplace.OUTSTANDING_PRINCIPAL].sum())
    return overall_group_by_country


def get_percentage_investment_by_originator(investment_raw_data):
    overall_group_by_originator = investment_raw_data.groupby(marketplace.LOAN_ORIGINATOR).sum()
    overall_group_by_originator = overall_group_by_originator.sort_values(by=marketplace.OUTSTANDING_PRINCIPAL, ascending=False)
    overall_group_by_originator['Percentage'] = overall_group_by_originator[marketplace.OUTSTANDING_PRINCIPAL] / (
        overall_group_by_originator[marketplace.OUTSTANDING_PRINCIPAL].sum() )
    return overall_group_by_originator