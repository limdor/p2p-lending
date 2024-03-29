import os
import pandas
from marketplace import mintos
from marketplace import iuvo
from marketplace import marketplace
from reports import diversification
from reports import overall
from logger import logger
from datacollection import datacollection

RELEVANT_COLUMNS = [marketplace.COUNTRY, marketplace.LOAN_ORIGINATOR, marketplace.OUTSTANDING_PRINCIPAL, marketplace.INTEREST_RATE]
DATA_DIRECTORY = os.path.join('.', 'data')


def aggregate_investment_data(investment_files):
    list_dataframes = []
    for investment_platform, files in investment_files.items():
        for date, file_path in sorted(files.items(), key=lambda item: item[0]):
            list_dataframes.append(get_dataframe_from_excel(file_path, date, investment_platform))
    df_investments = pandas.concat(list_dataframes)
    return df_investments


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
    df[marketplace.INVESTMENT_PLATFORM], df[marketplace.FILE_DATE] = investment_platform.name, pandas.Timestamp(date, unit='D')
    return df


def print_investment_data(investment_data):
    for investment_platform, files in investment_data.items():
        logger.info(f"Investment platform: {investment_platform.display_name}")
        for date, file_path in sorted(files.items(), key=lambda item: item[0]):
            logger.info(f'  {date}: {file_path}')


def main(show_past_investments):
    investment_files = datacollection.collect_investment_data(DATA_DIRECTORY, [mintos.META_DATA, iuvo.META_DATA])

    if show_past_investments:
        logger.info("Report containing all records")
    else:
        logger.info("Report containing only latest data")
        latest_common_date = datacollection.get_latest_common_date(investment_files)
        latest_date = datacollection.get_latest_date(investment_files)
        investment_files = datacollection.filter_investment_files_by_date(investment_files, latest_common_date)
        if latest_common_date != latest_date:
            logger.info(f"The newest date of a investment file across all platforms is from {latest_date}")
            logger.info(f"However, the date that is common for all platforms is {latest_common_date}")
            logger.info("For the moment the latest common date will be used, in the future the user will choose")

    logger.info("*********************")
    logger.info("**** Loaded data ****")
    logger.info("*********************")
    print_investment_data(investment_files)

    logger.info("**********************************")
    logger.info("**** Aggregate available data ****")
    logger.info("**********************************")
    df_investments = aggregate_investment_data(investment_files)
    logger.info('TODO: function to summarise information')

    logger.info("*******************************")
    logger.info("**** Plataform Investments ***")
    logger.info("*******************************")
    for investment_platform, files in investment_files.items():
        logger.info("|")
        logger.info(f" --- Platform : {investment_platform.display_name} ---")
        for date in sorted(files.keys()):
            if show_past_investments or date == latest_common_date:
                df_group_by_date_platform = df_investments[
                    (df_investments[marketplace.FILE_DATE] == pandas.Timestamp(date, unit='D')) &
                    (df_investments[marketplace.INVESTMENT_PLATFORM] == investment_platform.name)]
                logger.info('Investments by country:')
                df_group_by_country = df_group_by_date_platform.groupby([marketplace.COUNTRY]).sum()
                df_group_by_country = df_group_by_country[[marketplace.OUTSTANDING_PRINCIPAL]]
                logger.info(df_group_by_country.sort_values(by=marketplace.OUTSTANDING_PRINCIPAL, ascending=False))
                logger.info('Investments by loan originator:')
                df_group_by_originator = df_group_by_date_platform.groupby([marketplace.LOAN_ORIGINATOR]).sum()
                df_group_by_originator = df_group_by_originator[[marketplace.OUTSTANDING_PRINCIPAL]]
                logger.info(df_group_by_originator.sort_values(by=marketplace.OUTSTANDING_PRINCIPAL, ascending=False))

    overall_report = overall.generate_report_per_date(df_investments)
    overall.print_report_per_date(overall_report)

    diversification_report_per_date = diversification.generate_report_per_date(df_investments)
    diversification.print_report_per_date(diversification_report_per_date)
