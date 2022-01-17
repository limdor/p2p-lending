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
    fig.update_traces(
        textinfo="label+percent entry",
        hovertemplate = "%{value:,.2f}€")
    fig.update_layout(
        grid=dict(columns=1, rows=1),
        margin=dict(t=5, l=5, r=5, b=5))
    return fig


def piechart_OriginatorCountry(investment_raw_data):
    return piechart(
        investment_raw_data,
        [marketplace.LOAN_ORIGINATOR, marketplace.COUNTRY]
    )


def piechart_CountryOriginator(investment_raw_data):
    return piechart(
        investment_raw_data,
        [marketplace.COUNTRY, marketplace.LOAN_ORIGINATOR]
    )
