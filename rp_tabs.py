import plotly.express as px  # (version 4.7.0)
import plotly
import plotly.graph_objects as go
import dash_table
import pandas as pd
import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import base64
from dash.dependencies import Input, Output
import numpy as np

#proximos passos:
#1.ajustar tamanho da pagina nos diferentes ecrãs
#2.adicionar dados de preços
#3.adicionar outros países
#4.passar países a dropdown menu, com multi
#5.passar para o pythonanywhere


app = dash.Dash(__name__)


# Import and clean data (importing csv into pandas)
xls_m = pd.ExcelFile("retail_pulse_data.xls")
df_m_PT = pd.read_excel(xls_m,'PT')
df_m_ESP = pd.read_excel(xls_m,'ESP')
df_m_IT = pd.read_excel(xls_m,'IT')
df_m_DE = pd.read_excel(xls_m,'DE')

df_m = df_m_PT.append([df_m_ESP,df_m_IT,df_m_DE],ignore_index=True)

xls_q = pd.ExcelFile("retail_pulse_quarters.xls")
df_q_PT = pd.read_excel(xls_q,'PT')
df_q_ESP = pd.read_excel(xls_q,'ESP')
df_q_IT = pd.read_excel(xls_q,'IT')
df_q_DE = pd.read_excel(xls_q,'DE')


df_q = df_q_PT.append([df_q_ESP,df_q_IT,df_q_DE],ignore_index=True)


xls_y = pd.ExcelFile("retail_pulse_years.xls")
df_y_PT = pd.read_excel(xls_y,'PT')
df_y_ESP = pd.read_excel(xls_y,'ESP')
df_y_IT = pd.read_excel(xls_y,'IT')
df_y_DE = pd.read_excel(xls_y,'DE')


df_y = df_y_PT.append([df_y_ESP,df_y_IT,df_y_DE],ignore_index=True)


df_final = df_m
df_final = df_final.append([df_q,df_y], ignore_index=True)
df_final = df_final.round(1)

app.layout = html.Div([

            dbc.Row([
                dbc.Col(html.Img(src=app.get_asset_url('logo_retailpulse.png'),
                                        style={'float': 'left'}
                                ),
                            ),
       #             dbc.Col(html.Img(src=app.get_asset_url('logoSONAE.png'),
       #                     style={#'height': '25%',
       #                             #'width': '25%',
       #                            'float': 'right',
       #                            'margin-top': 20,
       #                             'margin-right': 250
       #                            }
       #                      ),
       #                ),
                        ],
                    ),

            html.Br(),
            html.Br(),
            html.Br(),

                 dbc.Row(dbc.Col(html.H1("Retail Pulse"
                                " ", style={'text-align': 'left'}),
                                        width={'size': 3, 'offset': 1}
                                        ),
                                ),


                dbc.Row(dbc.Col(html.Div("Evolution of nominal retail sales in different "
                                     "Euro area countries"),
                            width={'size':3, 'offset': 1}
                            )
                    ),

                html.Br(),

                dbc.Row(dbc.Col(html.Label(['Select country:'], style={'font-weight': 'bold'}),
                                width={'size': 5, 'offset': 1},
                                ),
                        ),

                dbc.Row(dbc.Col(dcc.RadioItems(id="slct_cntry",
                                options=[
                                    {'label': 'Portugal', 'value': 'PT'},
                                    {'label': 'Spain', 'value': 'ES'},
                                    {'label': 'Germany', 'value': 'DE'},
                                    {'label': 'Italy', 'value': 'IT'},
                                    ],
                                value= 'PT',
                                labelStyle = {'display': 'inline-block'}
                                           ),
                                        width={'size': 5 , 'offset': 1},
                                        ),
                                ),

                dbc.Row(dbc.Col(html.Div(id='output_container_country', children=[]),
                                width={'size': 5, 'offset': 1}
                                ),
                        ),

                html.Br(),


                dbc.Row(dbc.Col(html.Label(['Select period:'], style={'font-weight': 'bold'}),
                                width={'size': 5, 'offset': 1},
                                ),
                        ),

                dbc.Row(dbc.Col(dcc.RadioItems(id="slct_period",
                                                           options=[
                                                               {'label': 'Monthly', 'value': 'MON'},
                                                               {'label': 'Quarterly', 'value': 'QUA'},
                                                               {'label': 'Annual', 'value': 'ANU'},
                                                           ],
                                                           value='MON',
                                                           labelStyle={'display': 'inline-block'}
                                                           ),
                                            width={'size': 5, 'offset': 1},
                                            ),
                                    ),

                dbc.Row(dbc.Col(html.Div(id='output_container_period', children=[]),
                                width={'size': 5, 'offset': 1}
                                ),
                        ),


                html.Br(),

                dbc.Row(dbc.Col(dcc.Graph(id='the_graph', figure={}),
                                    width={'size': 11, 'offset': 1}
                                ),
                        ),

                html.Br(),

                html.Br(),

                html.Br(),

                dbc.Row(dbc.Col(html.Div(id='table-container', className='tableDiv'),
                        width={'size': 8, 'offset': 1})
                        ),

                html.Br(),

                html.Br(),

                dbc.Row(dbc.Col(html.Img(src=app.get_asset_url('logo_gspc.png')),
                                width={'size': 10, 'offset': 2}
                                ),
                        ),

                html.Br(),

                html.Br(),


])

#2 Connect the Plotly graphs with Dash Components
@app.callback(
        [Output(component_id='output_container_country', component_property='children'),
        Output(component_id='output_container_period', component_property='children'),
          Output(component_id='the_graph', component_property='figure'),
         Output(component_id='table-container', component_property='children')],
        [Input(component_id='slct_cntry', component_property='value'),
         Input(component_id='slct_period', component_property='value')],
)


def update_graph(option_slctd, period_slctd):
#1 App layout
        print(option_slctd)
        print(type(option_slctd))

        container_country  = "The country chosen by user was: {}".format(option_slctd)
        container_period = "The period selected by user was: {}".format(period_slctd)

        dff_final = df_final.copy()
        dff_final = dff_final[dff_final["country"] == option_slctd]
        dff_final = dff_final[dff_final["periodicidade"] == period_slctd]
        #dff_final.to_excel(r'dff_final.xlsx', index=False)
        dff_final.time = pd.DatetimeIndex(dff_final.time).strftime("%Y-%m-%d")
        fig = px.line(data_frame=dff_final,
                    x='time',
                    y=['Total','Food','Food in non-specialized stores','Food in specialized stores','Non-food','Fuel','Audio and video equipment and household appliances','Fashion','Computers, peripheral units and software','Healthcare','Eletronics'],
                    template='seaborn',
                    title="<b>Nominal retail sales - growth rate (YoY)<b>",
                    labels={
                        'time': 'time',
                        'y': 'categories'
                }
            )
        #3 Ploty

        fig.update_traces(mode='markers+lines', hovertemplate=None)
        fig.update_xaxes(rangeslider_visible=True, showspikes=True)
        fig.update_yaxes(title="Percantage", showspikes=True),
        #plotly.offline.plot(fig, filename="Retail_Pulse.html")
        fig.update_layout(  # customize font and legend orientation & position
            font_family="Calibri",
            hovermode="x",
            legend=dict(
            title=None, orientation="h", y=-0.5, yanchor="top", x=0.5, xanchor="center", font = dict (size=18)
           ),
        )
        fig.update_layout(
            autosize=False,
            width=1280,
            height=720,
            margin=dict(l=125, r=125, t=125, b=50),
            )


        categories_to_hide = ['Food','Food in non-specialized stores','Food in specialized stores','Non-food','Fuel','Audio and video equipment and household appliances','Fashion','Computers, peripheral units and software','Healthcare','Eletronics']
        fig.for_each_trace(lambda trace: trace.update(visible="legendonly")
                   if trace.name in categories_to_hide else ())




        tab = dash_table.DataTable(
                id='table',
                columns=[
                    {"name": i, "id": i, "deletable": True, "selectable": True, "hideable": True}
                    for i in df_final.columns
                ],
                data=dff_final.to_dict('records'),
                editable=False,
                export_format='xlsx',
                export_columns='visible',
                style_cell={'textAlign': 'center', 'font_size': '16px'},
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)',
                        'minWidth': 95, 'maxWidth': 295, 'width': 150,
                    }
                ],
                style_header={
                    'backgroundColor': '#e0ffff',
                    'fontWeight': 'bold',
                    'textAlign': 'left',
                    'minWidth': 200, 'maxWidth': 600, 'width': 400,
                    'whiteSpace': 'normal',
                    'height': 'auto',
                },
                filter_action="none",
                sort_action="native",
                sort_mode="multi",
                column_selectable="multi",
                row_selectable="multi",
                row_deletable=False,
                selected_columns=[],
                selected_rows=[],
                page_action="native",  # all data is passed to the table up-front or not ('none')
                page_current=0,
                page_size=10,
                style_table={'overflowX': 'auto'},
        ),


        return container_country, container_period, fig, tab


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=False)


