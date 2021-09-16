import pandas
import os
import re
import datetime
from marketplace import Marketplace
from collections import defaultdict

COUNTRY = 'Country'
LOAN_ORIGINATOR = 'Loan originator'
OUTSTANDING_PRINCIPAL = 'Outstanding principal'
INVESTMENT_PLATFORM = 'Investment platform'
FILE_DATE = 'Date'
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


def aggregate_investment_data(investment_files):
    list_dataframes = list()
    for investment_platform, files in investment_files.items():
        for date, file_path in sorted(files.items(), key=lambda item: item[0]):
            list_dataframes.append( get_dataframe_from_excel(file_path,date,investment_platform) )
    df_investiments = pandas.concat( list_dataframes )
    return df_investiments


def get_dataframe_from_excel(file_path,date,investment_platform):
    df = pandas.read_excel(
        file_path, 
        header=PLATFORM_SPECIFIC_DATA[investment_platform].header, 
        skipfooter=PLATFORM_SPECIFIC_DATA[investment_platform].skipfooter,
        usecols= lambda column : True if column in PLATFORM_SPECIFIC_DATA[investment_platform].column_mapping.keys() else False
    ).rename(
        columns=PLATFORM_SPECIFIC_DATA[investment_platform].column_mapping)
    if PLATFORM_SPECIFIC_DATA[investment_platform].originators_rename:
        df[LOAN_ORIGINATOR].replace(
            PLATFORM_SPECIFIC_DATA[investment_platform].originators_rename, inplace=True )
    df[INVESTMENT_PLATFORM], df[FILE_DATE] = investment_platform, date
    return df


def print_investment_data(investment_data):
    for investment_platform, files in investment_data.items():
        print(f"Investment platform: {PLATFORM_SPECIFIC_DATA[investment_platform].display_name}")
        for date, file_path in sorted(files.items(), key=lambda item: item[0]):
            print(f'  {date}: {file_path}')


def filter_investment_files_by_date(investment_data, dates:list = []):
    filtered_files = {}
    if dates[0].lower() == 'newest' or dates[0].lower() == 'latest':
        for investment_platform, files in investment_data.items():
            newest_date = get_latest_report_date(files)
            filtered_files[investment_platform] = dict(filter(lambda file: file[0] == newest_date, files.items()))
    elif dates[0].lower() == 'all':
        filtered_files = investment_data.copy()
    else: 
        for investment_platform, files in investment_data.items():
            filtered_files[investment_platform] = dict(filter(lambda file: file[0] in dates, files.items()))
    return filtered_files


def report(show_past_investments):

    if show_past_investments:
        print("Report containing all records")
    else:
        print("Report containing only latest data")

    print("***********************************")
    print("**** Collecting available data ****")
    print("***********************************")
    all_investment_files = collect_investment_data(DATA_DIRECTORY)
    if not show_past_investments:
        investment_files = filter_investment_files_by_date(all_investment_files,dates=['NEWEST'])
    else:
        investment_files = all_investment_files.copy()
    print_investment_data(investment_files)


    print("***********************************")
    print("**** Aggregate available data ****")
    print("***********************************")
    df_investiments = aggregate_investment_data(investment_files)
    print('TODO: function to summarise information')


    print("*******************************")
    print("**** Plataform Investments ***")
    print("*******************************")
    for investment_platform, files in investment_files.items():
        print("|")
        print(f" --- Platform : {PLATFORM_SPECIFIC_DATA[investment_platform].display_name} ---")
        newest_date = get_latest_report_date(files)
        for date in sorted(files.keys()):
            if show_past_investments or date == newest_date:
                df_group_by_date_platform = df_investiments[ 
                    (df_investiments[FILE_DATE] == date) &
                    (df_investiments[INVESTMENT_PLATFORM] == investment_platform) ]
                print(f'Investments by country:')
                df_group_by_country = df_group_by_date_platform.groupby([COUNTRY]).sum()
                print(df_group_by_country.sort_values(by=OUTSTANDING_PRINCIPAL, ascending=False))
                print(f'Investments by loan originator:')
                df_group_by_originator = df_group_by_date_platform.groupby([LOAN_ORIGINATOR]).sum()
                print(df_group_by_originator.sort_values(by=OUTSTANDING_PRINCIPAL, ascending=False))


    print("*****************************")
    print("**** Overall Investments ****")
    print("*****************************")
    overall_report = defaultdict(datetime.datetime)
    for date in sorted(set([ date for data_file in investment_files.values() for date in data_file ])):
        print(f"Overall Investments on {date}")
        # Overall statistics
        overall_group_by_date = df_investiments[ df_investiments[FILE_DATE] == date ]
        total_invested_by_date = overall_group_by_date[OUTSTANDING_PRINCIPAL].sum()
        total_invested_parts = len(overall_group_by_date.index)
        print(f"|- Overall Investment: {total_invested_by_date:.2f}€")

        # Statistics by Country
        print("|- Investment by Country")
        overall_group_by_country = overall_group_by_date.groupby(COUNTRY).sum()
        overall_group_by_country = overall_group_by_country.sort_values(by=OUTSTANDING_PRINCIPAL, ascending=False)
        overall_group_by_country['Percentage'] = overall_group_by_country[OUTSTANDING_PRINCIPAL] / total_invested_by_date
        print(overall_group_by_country)

        # Statistics by Loan Originator
        print("|- Investment by Country")
        overall_group_by_originator = overall_group_by_date.groupby(LOAN_ORIGINATOR).sum()
        overall_group_by_originator = overall_group_by_originator.sort_values(by=OUTSTANDING_PRINCIPAL, ascending=False)
        overall_group_by_originator['Percentage'] = overall_group_by_originator[OUTSTANDING_PRINCIPAL] / total_invested_by_date
        print(overall_group_by_originator)

        # It will be used in the diversification
        overall_report[date] = {
            'Data' : overall_group_by_date,
            'DataByCountry' : overall_group_by_country,
            'DataByLoanOriginator' : overall_group_by_originator,
            'TotalInvestment' :  total_invested_by_date,
            'NumberLoanParts' : total_invested_parts
        }


    print("*********************************")
    print("**** Diversification reports ****")
    print("*********************************")
    for date, overall_data in overall_report.items():
        print(f"Investments diversification on {date}")

        # Overall statistics
        total_invested_parts = overall_data['TotalInvestment']
        print(f"|- Diversification Investment: {total_invested_parts:.2f}€")

        total_loan_parts = overall_data['NumberLoanParts']
        print(f'|- The portfolio consists of at least 100 different loan parts: {total_loan_parts:d}')

        # Statistics by Country
        print(f"|- Statistics by Country:")
        overall_group_by_country = overall_data['DataByCountry']

        sum_on_top_3_countries = overall_group_by_country[OUTSTANDING_PRINCIPAL][0:3].sum()
        percentage_top_3_countries = (sum_on_top_3_countries / total_invested_by_date) * 100
        print(f'   |- No more than 50% of loans are issued in 3 (or less) countries: {percentage_top_3_countries:.2f}%')

        top_country = overall_group_by_country[OUTSTANDING_PRINCIPAL][0]
        percentage_top_country = (top_country / total_invested_by_date) * 100
        print(f'   |- No more than 33% of loans are issued in any single country: {percentage_top_country:.2f}%')

        # Statistics by Loan Originator
        print(f"|- Statistics by Originator:")
        overall_group_by_originator = overall_data['DataByLoanOriginator']

        sum_on_top_5_originators = overall_group_by_originator[OUTSTANDING_PRINCIPAL][0:5].sum()
        percentage_top_5_originators = (sum_on_top_5_originators / total_invested_by_date) * 100
        print(f'   |- No more than 50% of loans are issued by 5 (or less) lending companies: {percentage_top_5_originators:.2f}%')

        top_originator = overall_group_by_originator[OUTSTANDING_PRINCIPAL][0]
        percentage_top_originator = (top_originator / total_invested_by_date) * 100
        print(f'   |- No more than 20% of loans are issued by any single lending company: {percentage_top_originator:.2f}%')