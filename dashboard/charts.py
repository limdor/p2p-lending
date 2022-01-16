import plotly.express
from marketplace import marketplace


def piechart(investment_raw_data, group_by):
    investment_grouped_data = investment_raw_data.groupby(
        group_by,
        as_index=False).sum()
    fig = plotly.express.sunburst(
        investment_grouped_data,
        path=group_by,
        values='Outstanding principal',
        labels='')
    fig.update_traces(textinfo="label+percent entry")
    fig.update_layout(grid=dict(columns=1, rows=1),
        margin=dict(t=0, l=0, r=0, b=0))
    return fig


def piechart_PlatformOriginator(investment_raw_data):
    return piechart(
        investment_raw_data,
        [marketplace.INVESTMENT_PLATFORM, marketplace.LOAN_ORIGINATOR]
    )


def piechart_CountryPlatformOriginator(investment_raw_data):
    return piechart(
        investment_raw_data,
        [marketplace.COUNTRY, marketplace.INVESTMENT_PLATFORM, marketplace.LOAN_ORIGINATOR]
    )
