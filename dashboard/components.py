
import dash
import figures

def add_figure_card(figure_id):
    return dash.html.Div(
        [
            dash.dcc.Graph(
                    id=figure_id,
                    figure=figures.blank(),
                    className="border",
                    style={
                        'height': '40vh',
                        'text-align': 'center',
                        'margin': '10px',
                        'box-shadow': 'rgba(17, 17, 26, 0.05) 0px 1px 0px, rgba(17, 17, 26, 0.1) 0px 0px 8px',
                    }
                )
        ],
        className="col",
        style={
            'height': 'fit-content',
            },
        )