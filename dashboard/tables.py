import plotly.graph_objects
from marketplace import marketplace


def table_RawData(investment_raw_data, columns_excluded=None):
    if not columns_excluded:
        columns_excluded = []
    filtered_data = investment_raw_data.drop(columns_excluded, axis=1)
    table = plotly.graph_objects.Table(
        header=dict(
            values=list(filtered_data.columns),
            fill_color='paleturquoise',
            align='left'
            ),
        cells=dict(
            values=list(filtered_data.to_numpy().T),
            fill_color='lavender',
            align='left'
            )
        )
    fig = plotly.graph_objects.Figure(data=table)
    fig.update_layout(
        margin=dict(t=15, l=15, r=15, b=15))
    return fig


def table_DataGrouped(investment_raw_data, group_by):
    data_grouped_by = investment_raw_data.groupby(group_by).sum()
    data_grouped_by = data_grouped_by.sort_values(by=marketplace.OUTSTANDING_PRINCIPAL, ascending=False).reset_index()
    table = plotly.graph_objects.Table(
        header=dict(
            values=list(data_grouped_by.columns),
            fill_color='paleturquoise',
            align=['left','right'],
            ),
        cells=dict(
            values=list(data_grouped_by.round(2).to_numpy().T),
            fill_color='lavender',
            align=['left','right'],
            format=["",",.2f"],
            suffix=["","€"],
            ),
        )
    fig = plotly.graph_objects.Figure(data=table)
    fig.update_layout(
        margin=dict(t=15, l=15, r=15, b=15))
    return fig


def table_DataByOriginator(investment_raw_data):
    return table_DataGrouped(investment_raw_data, [marketplace.LOAN_ORIGINATOR])


def table_DataByCountry(investment_raw_data):
    return table_DataGrouped(investment_raw_data, [marketplace.COUNTRY])
