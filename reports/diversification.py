from logger import logger
from . import calculator


def generate_report_per_date(overall_report):
    diversification_report_per_date = {}
    for date, overall_data in overall_report.items():
        diversification_report_per_date[date] = generate_report(date, overall_data)

    return diversification_report_per_date


def generate_report(date, overall_data):
    diversification_report = {}
    diversification_report['reportId'] = date
    diversification_report['RawDataHash'] = calculator.get_raw_data_hash(overall_data['Data'])
    diversification_report['overallInvestment'] = calculator.get_total_investment(overall_data['Data'])
    diversification_report['loanParts'] = calculator.get_number_loan_parts(overall_data['Data'])
    diversification_report['countryStatistics'] = {
        'investmentOneCountry': calculator.get_percentage_top_country(overall_data['Data']),
        'investmentThreeCountries': calculator.get_percentage_top_3_countries(overall_data['Data'])
    }
    diversification_report['originatorStatistics'] = {
        'investmentOneOriginator': calculator.get_percentage_top_originator(overall_data['Data']),
        'investmentFiveOriginators': calculator.get_percentage_top_5_originators(overall_data['Data'])
    }

    return diversification_report


def print_report_per_date(diversification_report_per_date):
    logger.info("*********************************")
    logger.info("**** Diversification reports ****")
    logger.info("*********************************")
    for date, report in diversification_report_per_date.items():
        logger.info(f"Investments diversification on {date}")
        logger.info(f"|- Raw data hash: {report['RawDataHash']}")
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
