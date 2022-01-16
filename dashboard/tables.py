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


def table_DataGrouped(investment_raw_data, group_by):
    data_grouped_by = investment_raw_data.groupby(group_by).sum()
    data_grouped_by = data_grouped_by.sort_values(by=marketplace.OUTSTANDING_PRINCIPAL, ascending=False).reset_index()
    table = plotly.graph_objects.Table(
        header=dict(
            values=list(data_grouped_by.columns),
            fill_color='paleturquoise',
            align='left'
            ),
        cells=dict(
            values=list(data_grouped_by.round(2).to_numpy().T),
            fill_color='lavender',
            align='left'
            )
        )
    return plotly.graph_objects.Figure(data=table)


def table_DataByPlatform(investment_raw_data):
    return table_DataGrouped(investment_raw_data, [marketplace.INVESTMENT_PLATFORM])


def table_DataByCountry(investment_raw_data):
    return table_DataGrouped(investment_raw_data, [marketplace.COUNTRY])
