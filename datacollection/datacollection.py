import os
import datetime

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
