import os
import datetime
from collections import defaultdict
import pandas
from marketplace import mintos
from marketplace import iuvo
from marketplace import marketplace
from logger import logger

INVESTMENT_PLATFORM = 'Investment platform'
FILE_DATE = 'Date'
RELEVANT_COLUMNS = [marketplace.COUNTRY, marketplace.LOAN_ORIGINATOR, marketplace.OUTSTANDING_PRINCIPAL]
DATA_DIRECTORY = os.path.join('.', 'data')
PLATFORM_SPECIFIC_DATA = {
    iuvo.MARKETPLACE_NAME: iuvo.MARKETPLACE_META_DATA,
    mintos.MARKETPLACE_NAME: mintos.MARKETPLACE_META_DATA,
}


def get_latest_report_date(marketplace_files):
    return max(marketplace_files.keys())


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
            list_dataframes.append(get_dataframe_from_excel(file_path, date, investment_platform))
    df_investiments = pandas.concat(list_dataframes)
    return df_investiments


def get_dataframe_from_excel(file_path, date, investment_platform):
    df = pandas.read_excel(
        file_path,
        header=PLATFORM_SPECIFIC_DATA[investment_platform].header,
        skipfooter=PLATFORM_SPECIFIC_DATA[investment_platform].skipfooter,
        usecols=lambda column: column in PLATFORM_SPECIFIC_DATA[investment_platform].column_mapping.keys(
        ) and PLATFORM_SPECIFIC_DATA[investment_platform].column_mapping[column] in RELEVANT_COLUMNS
    ).rename(
        columns=PLATFORM_SPECIFIC_DATA[investment_platform].column_mapping)
    if PLATFORM_SPECIFIC_DATA[investment_platform].originators_rename:
        df[marketplace.LOAN_ORIGINATOR].replace(
            PLATFORM_SPECIFIC_DATA[investment_platform].originators_rename, inplace=True)
    df[INVESTMENT_PLATFORM], df[FILE_DATE] = investment_platform, date
    return df


def print_investment_data(investment_data):
    for investment_platform, files in investment_data.items():
        logger.info(f"Investment platform: {PLATFORM_SPECIFIC_DATA[investment_platform].display_name}")
        for date, file_path in sorted(files.items(), key=lambda item: item[0]):
            logger.info(f'  {date}: {file_path}')


def filter_investment_files_by_newest_date(investment_data):
    filtered_files = {}
    for investment_platform, files in investment_data.items():
        newest_date = get_latest_report_date(files)
        filtered_files[investment_platform] = {
            key: value for (key, value) in files.items() if key == newest_date
        }
    return filtered_files


def generate_overall_report_per_date(df_investiments, investment_files):
    overall_report = defaultdict(datetime.datetime)
    for date in sorted({date for data_file in investment_files.values() for date in data_file}):
        # Overall statistics
        overall_group_by_date = df_investiments[df_investiments[FILE_DATE] == date]
        total_invested_by_date = overall_group_by_date[marketplace.OUTSTANDING_PRINCIPAL].sum()
        total_invested_parts = len(overall_group_by_date.index)

        # Statistics by Country
        overall_group_by_country = overall_group_by_date.groupby(marketplace.COUNTRY).sum()
        overall_group_by_country = overall_group_by_country.sort_values(by=marketplace.OUTSTANDING_PRINCIPAL, ascending=False)
        overall_group_by_country['Percentage'] = overall_group_by_country[marketplace.OUTSTANDING_PRINCIPAL] / total_invested_by_date

        # Statistics by Loan Originator
        overall_group_by_originator = overall_group_by_date.groupby(marketplace.LOAN_ORIGINATOR).sum()
        overall_group_by_originator = overall_group_by_originator.sort_values(by=marketplace.OUTSTANDING_PRINCIPAL, ascending=False)
        overall_group_by_originator['Percentage'] = overall_group_by_originator[marketplace.OUTSTANDING_PRINCIPAL] / total_invested_by_date

        # It will be used in the diversification
        overall_report[date] = {
            'Data': overall_group_by_date,
            'DataByCountry': overall_group_by_country,
            'DataByLoanOriginator': overall_group_by_originator,
            'TotalInvestment':  total_invested_by_date,
            'NumberLoanParts': total_invested_parts
        }

    return overall_report


def print_overall_report_per_date(overall_report):
    logger.info("*****************************")
    logger.info("**** Overall Investments ****")
    logger.info("*****************************")
    for date, overall_data in overall_report.items():
        logger.info(f"Overall Investments on {date}")
        logger.info(f"|- Overall Investment: {overall_data['TotalInvestment']:.2f}€")
        logger.info("|- Investment by Country")
        logger.info(overall_data['DataByCountry'])
        logger.info("|- Investment by Loan Originator")
        logger.info(overall_data['DataByLoanOriginator'])


def generate_diversification_report_per_date(overall_report):
    diversification_report_per_date = {}
    for date, overall_data in overall_report.items():
        diversification_report_per_date[date] = {}
        diversification_report_per_date[date]['reportId'] = date

        # Overall statistics
        total_invested_parts = overall_data['TotalInvestment']
        diversification_report_per_date[date]['overallInvestment'] = total_invested_parts
        diversification_report_per_date[date]['loanParts'] = overall_data['NumberLoanParts']

        # Statistics by Country
        overall_group_by_country = overall_data['DataByCountry']
        sum_on_top_3_countries = overall_group_by_country[marketplace.OUTSTANDING_PRINCIPAL][0:3].sum()
        percentage_top_3_countries = (sum_on_top_3_countries / total_invested_parts) * 100
        top_country = overall_group_by_country[marketplace.OUTSTANDING_PRINCIPAL][0]
        percentage_top_country = (top_country / total_invested_parts) * 100
        diversification_report_per_date[date]['countryStatistics'] = {
            'investmentOneCountry': percentage_top_country, 'investmentThreeCountries': percentage_top_3_countries}

        # Statistics by Loan Originator
        overall_group_by_originator = overall_data['DataByLoanOriginator']
        sum_on_top_5_originators = overall_group_by_originator[marketplace.OUTSTANDING_PRINCIPAL][0:5].sum()
        percentage_top_5_originators = (sum_on_top_5_originators / total_invested_parts) * 100
        top_originator = overall_group_by_originator[marketplace.OUTSTANDING_PRINCIPAL][0]
        percentage_top_originator = (top_originator / total_invested_parts) * 100
        diversification_report_per_date[date]['originatorStatistics'] = {
            'investmentOneOriginator': percentage_top_originator, 'investmentFiveOriginators': percentage_top_5_originators}

    return diversification_report_per_date


def print_diversification_report_per_date(diversification_report_per_date):
    logger.info("*********************************")
    logger.info("**** Diversification reports ****")
    logger.info("*********************************")
    for date, report in diversification_report_per_date.items():
        logger.info(f"Investments diversification on {date}")
        logger.info(f"|- Diversification Investment: {report['overallInvestment']:.2f}€")
        logger.info(f"|- The portfolio consists of at least 100 different loan parts: {report['loanParts']:d}")
        logger.info("|- Statistics by Country:")
        logger.info(f"   |- No more than 50% of loans are issued in 3 (or less) countries: {report['countryStatistics']['investmentThreeCountries']:.2f}%")
        logger.info(f"   |- No more than 33% of loans are issued in any single country: {report['countryStatistics']['investmentOneCountry']:.2f}%")
        logger.info("|- Statistics by Originator:")
        logger.info(
            f"   |- No more than 50% of loans are issued by 5 (or less) lending companies: {report['originatorStatistics']['investmentFiveOriginators']:.2f}%")
        logger.info(
            f"   |- No more than 20% of loans are issued by any single lending company: {report['originatorStatistics']['investmentOneOriginator']:.2f}%")


def main(show_past_investments):

    if show_past_investments:
        logger.info("Report containing all records")
    else:
        logger.info("Report containing only latest data")

    logger.info("***********************************")
    logger.info("**** Collecting available data ****")
    logger.info("***********************************")
    all_investment_files = collect_investment_data(DATA_DIRECTORY)
    if not show_past_investments:
        investment_files = filter_investment_files_by_newest_date(all_investment_files)
    else:
        investment_files = all_investment_files.copy()
    print_investment_data(investment_files)

    logger.info("***********************************")
    logger.info("**** Aggregate available data ****")
    logger.info("***********************************")
    df_investiments = aggregate_investment_data(investment_files)
    logger.info('TODO: function to summarise information')

    logger.info("*******************************")
    logger.info("**** Plataform Investments ***")
    logger.info("*******************************")
    for investment_platform, files in investment_files.items():
        logger.info("|")
        logger.info(f" --- Platform : {PLATFORM_SPECIFIC_DATA[investment_platform].display_name} ---")
        newest_date = get_latest_report_date(files)
        for date in sorted(files.keys()):
            if show_past_investments or date == newest_date:
                df_group_by_date_platform = df_investiments[
                    (df_investiments[FILE_DATE] == date) &
                    (df_investiments[INVESTMENT_PLATFORM] == investment_platform)]
                logger.info('Investments by country:')
                df_group_by_country = df_group_by_date_platform.groupby([marketplace.COUNTRY]).sum()
                logger.info(df_group_by_country.sort_values(by=marketplace.OUTSTANDING_PRINCIPAL, ascending=False))
                logger.info('Investments by loan originator:')
                df_group_by_originator = df_group_by_date_platform.groupby([marketplace.LOAN_ORIGINATOR]).sum()
                logger.info(df_group_by_originator.sort_values(by=marketplace.OUTSTANDING_PRINCIPAL, ascending=False))

    overall_report = generate_overall_report_per_date(df_investiments, investment_files)
    print_overall_report_per_date(overall_report)

    diversification_report_per_date = generate_diversification_report_per_date(overall_report)
    print_diversification_report_per_date(diversification_report_per_date)
