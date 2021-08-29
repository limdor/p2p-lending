import pandas
import os
import re
import datetime
from marketplace import Marketplace
from collections import defaultdict

COUNTRY = 'Country'
LOAN_ORIGINATOR = 'Loan originator'
OUTSTANDING_PRINCIPAL = 'Outstanding principal'
RELEVANT_COLUMNS = [COUNTRY, LOAN_ORIGINATOR, OUTSTANDING_PRINCIPAL]
DATA_DIRECTORY = os.path.join('.', 'data')
PLATFORM_SPECIFIC_DATA = {
    'iuvo': Marketplace(
        filename_regexp=re.compile(r'MyInvestments-(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2}).xlsx'),
        display_name='IUVO',
        column_mapping={'Country': COUNTRY, 'Originator': LOAN_ORIGINATOR, 'Outstanding principal': OUTSTANDING_PRINCIPAL},
        originators_rename={'iCredit Poland': 'iCredit', 'iCredit Romania': 'iCredit'},
        header=3,
        skipfooter=3),
    'mintos': Marketplace(
        filename_regexp=re.compile(r'(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})-current-investments.xlsx'),
        display_name='Mintos',
        # TODO: There might be money in 'Pending Payments' column even if the investment is not finished
        column_mapping={'Country': COUNTRY, 'Loan Originator': LOAN_ORIGINATOR,
                        'Lending Company': LOAN_ORIGINATOR, 'Outstanding Principal': OUTSTANDING_PRINCIPAL},
        originators_rename=None,
        header=0,
        skipfooter=0),
}


def parse_investments(date, current_investments, column_mapping):
    current_investments = current_investments.rename(columns=column_mapping)

    current_investments = current_investments[RELEVANT_COLUMNS]
    sum_outstanding_principal = current_investments[OUTSTANDING_PRINCIPAL].sum()
    print(f"Investment on {date}: {len(current_investments.index)} with a total amount of {sum_outstanding_principal:.2f}€")
    group_by_country = current_investments.groupby([COUNTRY]).sum()
    group_by_originator = current_investments.groupby([LOAN_ORIGINATOR]).sum()
    return group_by_country, group_by_originator


def get_latest_report_date(marketplace_files):
    newest_date = datetime.date.min
    for report_date in marketplace_files.keys():
        if(report_date > newest_date):
            newest_date = report_date
    return newest_date


def read_marketplace_files(data_directory, marketplace_name):
    marketplace_files = {}
    for root, _, files in os.walk(os.path.join(data_directory, marketplace_name)):
        for investment_snapshot in files:
            match = PLATFORM_SPECIFIC_DATA[marketplace_name].filename_regexp.search(investment_snapshot)
            if match:
                report_date = datetime.date.fromisoformat(f"{match.group('year')}-{match.group('month')}-{match.group('day')}")
                marketplace_files[report_date] = os.path.join(root, investment_snapshot)
    return marketplace_files


def collect_investment_data(data_directory):
    data_files = {}
    investment_platforms = [entry.name for entry in os.scandir(data_directory) if entry.is_dir()]
    for investment_platform in investment_platforms:
        data_files[investment_platform] = read_marketplace_files(data_directory, investment_platform)
    return data_files


def print_investment_data(investment_data):
    for investment_platform, files in investment_data.items():
        print(f"Investment platform: {PLATFORM_SPECIFIC_DATA[investment_platform].display_name}")
        for date, file_path in sorted(files.items(), key=lambda item: item[0]):
            print(f'  {date}: {file_path}')


def report(show_past_investments):
    if show_past_investments:
        print("Report containing all records")
    else:
        print("Report containing only latest data")

    print("***********************************")
    print("**** Collecting available data ****")
    print("***********************************")
    investment_files = collect_investment_data(DATA_DIRECTORY)
    print_investment_data(investment_files)

    investments_by_country_by_date = defaultdict(list)
    investments_by_originator_by_date = defaultdict(list)
    for investment_platform, files in investment_files.items():
        print("**************************")
        print(f"**** {PLATFORM_SPECIFIC_DATA[investment_platform].display_name} Investments ****")
        print("**************************")
        newest_date = get_latest_report_date(files)
        print(f"Newest report date: {newest_date}")
        for date, file_path in sorted(files.items(), key=lambda item: item[0]):
            if show_past_investments or date == newest_date:
                investments = pandas.read_excel(
                    file_path, header=PLATFORM_SPECIFIC_DATA[investment_platform].header, skipfooter=PLATFORM_SPECIFIC_DATA[investment_platform].skipfooter)
                group_by_country, group_by_originator = parse_investments(date, investments, PLATFORM_SPECIFIC_DATA[investment_platform].column_mapping)
                print(f'Investments by country:')
                print(group_by_country.sort_values(by=OUTSTANDING_PRINCIPAL, ascending=False))
                print(f'Investments by loan originator:')
                print(group_by_originator.sort_values(by=OUTSTANDING_PRINCIPAL, ascending=False))
                originators_rename = PLATFORM_SPECIFIC_DATA[investment_platform].originators_rename
                if originators_rename:
                    group_by_originator = group_by_originator.rename(index=originators_rename)
                investments_by_country_by_date[date].append(group_by_country)
                investments_by_originator_by_date[date].append(group_by_originator)

    print("*****************************")
    print("**** Overall Investments ****")
    print("*****************************")
    print(f'The portfolio consists of at least 100 different loan parts: TODO')  # {len(investment_data.index)}')
    for date, investment_data in investments_by_country_by_date.items():
        overall_group_by_country = pandas.concat(investment_data).groupby([COUNTRY]).sum()
        total_invested_by_country = overall_group_by_country[OUTSTANDING_PRINCIPAL].sum()
        print(f"Overall Investment on {date}: {total_invested_by_country:.2f}€")
        overall_group_by_country['Percentage'] = overall_group_by_country[OUTSTANDING_PRINCIPAL] / total_invested_by_country

        countries_sorted_by_principal = overall_group_by_country.sort_values(by=OUTSTANDING_PRINCIPAL, ascending=False)
        print(countries_sorted_by_principal)

        sum_on_top_3_countries = countries_sorted_by_principal[OUTSTANDING_PRINCIPAL][0:3].sum()
        percentage_top_3_countries = (sum_on_top_3_countries / total_invested_by_country) * 100
        print(f'No more than 50% of loans are issued in 3 (or less) countries: {percentage_top_3_countries:.2f}%')

        top_country = countries_sorted_by_principal[OUTSTANDING_PRINCIPAL][0]
        percentage_top_country = (top_country / total_invested_by_country) * 100
        print(f'No more than 33% of loans are issued in any single country: {percentage_top_country:.2f}%')

    for date, investment_data in investments_by_originator_by_date.items():
        overall_group_by_originator = pandas.concat(investment_data).groupby([LOAN_ORIGINATOR]).sum()
        total_invested_by_originator = overall_group_by_originator[OUTSTANDING_PRINCIPAL].sum()
        print(f"Overall Investment on {date}: {total_invested_by_originator:.2f}€")
        overall_group_by_originator['Percentage'] = overall_group_by_originator[OUTSTANDING_PRINCIPAL] / total_invested_by_originator

        originators_sorted_by_principal = overall_group_by_originator.sort_values(by=OUTSTANDING_PRINCIPAL, ascending=False)
        print(originators_sorted_by_principal)

        sum_on_top_5_originators = originators_sorted_by_principal[OUTSTANDING_PRINCIPAL][0:5].sum()
        percentage_top_5_originators = (sum_on_top_5_originators / total_invested_by_originator) * 100
        print(f'No more than 50% of loans are issued by 5 (or less) lending companies: {percentage_top_5_originators:.2f}%')

        top_originator = originators_sorted_by_principal[OUTSTANDING_PRINCIPAL][0]
        percentage_top_originator = (top_originator / total_invested_by_originator) * 100
        print(f'No more than 20% of loans are issued by any single lending company: {percentage_top_originator:.2f}%')
