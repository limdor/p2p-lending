from logger import logger
from marketplace import marketplace


def generate_report_per_date(overall_report):
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


def print_report_per_date(diversification_report_per_date):
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
