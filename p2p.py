import os
import datetime
import pandas
from marketplace import mintos
from marketplace import iuvo
from marketplace import marketplace
from reports import diversification
from reports import overall
from logger import logger


RELEVANT_COLUMNS = [marketplace.COUNTRY, marketplace.LOAN_ORIGINATOR, marketplace.OUTSTANDING_PRINCIPAL]
DATA_DIRECTORY = os.path.join('.', 'data')


def get_latest_report_date(marketplace_files):
    return max(marketplace_files.keys())


def read_marketplace_files(data_directory, investment_platform):
    marketplace_files = {}
    for root, _, files in os.walk(os.path.join(data_directory, investment_platform.name)):
        for investment_snapshot in files:
            match = investment_platform.filename_regexp.search(investment_snapshot)
            if match:
                report_date = datetime.date.fromisoformat(f"{match.group('year')}-{match.group('month')}-{match.group('day')}")
                marketplace_files[report_date] = os.path.join(root, investment_snapshot)
    return marketplace_files


def collect_investment_data(data_directory, investment_platforms):
    data_files = {}
    for investment_platform in investment_platforms:
        data_files[investment_platform] = read_marketplace_files(data_directory, investment_platform)
    return data_files


def aggregate_investment_data(investment_files):
    list_dataframes = []
    for investment_platform, files in investment_files.items():
        for date, file_path in sorted(files.items(), key=lambda item: item[0]):
            list_dataframes.append(get_dataframe_from_excel(file_path, date, investment_platform))
    df_investiments = pandas.concat(list_dataframes)
    return df_investiments


def get_dataframe_from_excel(file_path, date, investment_platform):
    df = pandas.read_excel(
        file_path,
        header=investment_platform.header,
        skipfooter=investment_platform.skipfooter,
        usecols=lambda column: column in investment_platform.column_mapping.keys(
        ) and investment_platform.column_mapping[column] in RELEVANT_COLUMNS
    ).rename(
        columns=investment_platform.column_mapping)
    if investment_platform.originators_rename:
        df[marketplace.LOAN_ORIGINATOR].replace(
            investment_platform.originators_rename, inplace=True)
    df[marketplace.INVESTMENT_PLATFORM], df[marketplace.FILE_DATE] = investment_platform.name, date
    return df


def print_investment_data(investment_data):
    for investment_platform, files in investment_data.items():
        logger.info(f"Investment platform: {investment_platform.display_name}")
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


def main(show_past_investments):

    if show_past_investments:
        logger.info("Report containing all records")
    else:
        logger.info("Report containing only latest data")

    logger.info("***********************************")
    logger.info("**** Collecting available data ****")
    logger.info("***********************************")
    all_investment_files = collect_investment_data(DATA_DIRECTORY, [mintos.META_DATA, iuvo.META_DATA])
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
        logger.info(f" --- Platform : {investment_platform.display_name} ---")
        newest_date = get_latest_report_date(files)
        for date in sorted(files.keys()):
            if show_past_investments or date == newest_date:
                df_group_by_date_platform = df_investiments[
                    (df_investiments[marketplace.FILE_DATE] == date) &
                    (df_investiments[marketplace.INVESTMENT_PLATFORM] == investment_platform.name)]
                logger.info('Investments by country:')
                df_group_by_country = df_group_by_date_platform.groupby([marketplace.COUNTRY]).sum()
                logger.info(df_group_by_country.sort_values(by=marketplace.OUTSTANDING_PRINCIPAL, ascending=False))
                logger.info('Investments by loan originator:')
                df_group_by_originator = df_group_by_date_platform.groupby([marketplace.LOAN_ORIGINATOR]).sum()
                logger.info(df_group_by_originator.sort_values(by=marketplace.OUTSTANDING_PRINCIPAL, ascending=False))

    overall_report = overall.generate_report_per_date(df_investiments)
    overall.print_report_per_date(overall_report)

    diversification_report_per_date = diversification.generate_report_per_date(overall_report)
    diversification.print_report_per_date(diversification_report_per_date)
