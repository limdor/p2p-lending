import plotly.graph_objects
from marketplace import marketplace

def table_AllRawData(investment_raw_data):
    table = plotly.graph_objects.Table(
        header=dict(
            values=list(investment_raw_data.columns),
            fill_color='paleturquoise',
            align='left'
            ),
        cells=dict(
            values=list(investment_raw_data.to_numpy().T),
            fill_color='lavender',
            align='left'
            )
        )
    return plotly.graph_objects.Figure(data=table)


def table_DataByPlatform(investment_raw_data):
    data_group_by_platform = investment_raw_data.groupby([marketplace.INVESTMENT_PLATFORM]).sum()
    data_group_by_platform = data_group_by_platform.sort_values(by=marketplace.OUTSTANDING_PRINCIPAL, ascending=False).reset_index()
    table = plotly.graph_objects.Table(
        header=dict(
            values=list(data_group_by_platform.columns),
            fill_color='paleturquoise',
            align='left'
            ),
        cells=dict(
            values=list(data_group_by_platform.round(2).to_numpy().T),
            fill_color='lavender',
            align='left'
            )
        )
    return plotly.graph_objects.Figure(data=table)


def table_DataByCountry(investment_raw_data):
    data_group_by_country = investment_raw_data.groupby([marketplace.COUNTRY]).sum()
    data_group_by_country = data_group_by_country.sort_values(by=marketplace.OUTSTANDING_PRINCIPAL, ascending=False).reset_index()
    table = plotly.graph_objects.Table(
        header=dict(
            values=list(data_group_by_country.columns),
            fill_color='paleturquoise',
            align='left'
        ),
        cells=dict(
            values=list(data_group_by_country.round(2).to_numpy().T),
            fill_color='lavender',
            align='left'),
        )
    return plotly.graph_objects.Figure(data=table)
