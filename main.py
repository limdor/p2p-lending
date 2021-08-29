import argparse
import pandas
import os
import re
import datetime
from p2pplatform import P2PPlatform
from collections import defaultdict

COUNTRY = 'Country'
LOAN_ORIGINATOR = 'Loan originator'
OUTSTANDING_PRINCIPAL = 'Outstanding principal'
RELEVANT_COLUMNS = [COUNTRY, LOAN_ORIGINATOR, OUTSTANDING_PRINCIPAL]
DATA_DIRECTORY = os.path.join('.', 'data')
PLATFORM_SPECIFIC_DATA = {
    'iuvo': P2PPlatform(
        filename_regexp=re.compile(r'MyInvestments-(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2}).xlsx'),
        display_name='IUVO',
        column_mapping={'Country': COUNTRY, 'Originator': LOAN_ORIGINATOR, 'Outstanding principal': OUTSTANDING_PRINCIPAL},
        originators_rename={'iCredit Poland': 'iCredit', 'iCredit Romania': 'iCredit'},
        header=3,
        skipfooter=3),
    'mintos': P2PPlatform(
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


def read_marketplace_files(data_directory, marketplace_name):
    marketplace_files = {}
    for root, _, files in os.walk(os.path.join(data_directory, marketplace_name)):
        for investment_snapshot in files:
            match = PLATFORM_SPECIFIC_DATA[marketplace_name].filename_regexp.search(investment_snapshot)
            if match:
                report_date = datetime.date.fromisoformat(f"{match.group('year')}-{match.group('month')}-{match.group('day')}")
                file_path = os.path.join(root, investment_snapshot)
                marketplace_files[report_date] = file_path
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
        print(f'Available files:')
        for date, file_path in sorted(files.items(), key=lambda item: item[0]):
            print(f'  {date}: {file_path}')


def main(show_past_investments):
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
        for date, file_path in sorted(files.items(), key=lambda item: item[0]):
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
    for date, investment_data in investments_by_country_by_date.items():
        overall_group_by_country = pandas.concat(investment_data).groupby([COUNTRY]).sum()
        total_invested_by_country = overall_group_by_country[OUTSTANDING_PRINCIPAL].sum()
        print(f"Overall Investment on {date}: {total_invested_by_country:.2f}€")
        overall_group_by_country['Percentage'] = overall_group_by_country[OUTSTANDING_PRINCIPAL] / total_invested_by_country
        print(overall_group_by_country.sort_values(by=OUTSTANDING_PRINCIPAL, ascending=False))

    for date, investment_data in investments_by_originator_by_date.items():
        overall_group_by_originator = pandas.concat(investment_data).groupby([LOAN_ORIGINATOR]).sum()
        total_invested_by_originator = overall_group_by_originator[OUTSTANDING_PRINCIPAL].sum()
        print(f"Overall Investment on {date}: {total_invested_by_originator:.2f}€")
        overall_group_by_originator['Percentage'] = overall_group_by_originator[OUTSTANDING_PRINCIPAL] / total_invested_by_originator
        print(overall_group_by_originator.sort_values(by=OUTSTANDING_PRINCIPAL, ascending=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--past", action="store_true",
                        help="Show past investments")
    args = parser.parse_args()
    show_past_investments = args.past
    main(show_past_investments)
