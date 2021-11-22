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
    return {investment_platform: read_marketplace_files(data_directory, investment_platform) for investment_platform in investment_platforms}


def get_latest_report_date(marketplace_files):
    return max(marketplace_files.keys())


def filter_investment_files_by_newest_date(investment_data):
    filtered_files = {}
    for investment_platform, files in investment_data.items():
        newest_date = get_latest_report_date(files)
        filtered_files[investment_platform] = {
            key: value for (key, value) in files.items() if key == newest_date
        }
    return filtered_files
