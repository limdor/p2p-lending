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
        labels="",
        maxdepth=3)
    fig.update_traces(
        textinfo="label+percent entry",
        hovertemplate = "%{value:,.2f}€")
    fig.update_layout(
        grid=dict(columns=1, rows=1),
        margin=dict(t=5, l=5, r=5, b=5))
    return fig


def piechart_OriginatorCountry(investment_raw_data):
    modified_investment_raw_data = investment_raw_data.filter([marketplace.OUTSTANDING_PRINCIPAL, marketplace.LOAN_ORIGINATOR, marketplace.COUNTRY])
    modified_investment_raw_data['Different Originators'] = f"{investment_raw_data[marketplace.OUTSTANDING_PRINCIPAL].sum():,.2f}€<br>"\
        f"{len(set(investment_raw_data[marketplace.LOAN_ORIGINATOR].to_list()))} originators"
    return piechart(
        modified_investment_raw_data,
        ['Different Originators', marketplace.LOAN_ORIGINATOR, marketplace.COUNTRY]
    )


def piechart_CountryOriginator(investment_raw_data):
    modified_investment_raw_data = investment_raw_data.filter([marketplace.OUTSTANDING_PRINCIPAL, marketplace.COUNTRY, marketplace.LOAN_ORIGINATOR])
    modified_investment_raw_data['Different Countries'] = f"{investment_raw_data[marketplace.OUTSTANDING_PRINCIPAL].sum():,.2f}€<br>"\
        f"{len(set(investment_raw_data[marketplace.COUNTRY].to_list()))} countries"
    return piechart(
        modified_investment_raw_data,
        ['Different Countries', marketplace.COUNTRY, marketplace.LOAN_ORIGINATOR]
    )
