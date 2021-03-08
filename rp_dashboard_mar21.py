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
import dash_extensions as de

#lotties:
url = "https://assets3.lottiefiles.com/packages/lf20_5Hkbhv.json"
options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))


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
df_m_ES = pd.read_excel(xls_m,'ES')
df_m_IT = pd.read_excel(xls_m,'IT')
df_m_DE = pd.read_excel(xls_m,'DE')
df_m_FR = pd.read_excel(xls_m,'FR')
df_m_PL = pd.read_excel(xls_m,'PL')
df_m_RO = pd.read_excel(xls_m,'RO')
df_m_UK = pd.read_excel(xls_m,'UK')


df_m = df_m_PT.append([df_m_ES,df_m_IT,df_m_DE,df_m_FR,df_m_PL,df_m_RO,df_m_UK],ignore_index=True)



xls_q = pd.ExcelFile("retail_pulse_quarters.xls")
df_q_PT = pd.read_excel(xls_q,'PT')
df_q_ES = pd.read_excel(xls_q,'ES')
df_q_IT = pd.read_excel(xls_q,'IT')
df_q_DE = pd.read_excel(xls_q,'DE')
df_q_FR = pd.read_excel(xls_q,'FR')
df_q_PL = pd.read_excel(xls_q,'PL')
df_q_RO = pd.read_excel(xls_q,'RO')
df_q_UK = pd.read_excel(xls_q,'UK')

df_q = df_q_PT.append([df_q_ES,df_q_IT,df_q_DE,df_q_FR,df_q_PL,df_q_RO,df_q_UK],ignore_index=True)


xls_y = pd.ExcelFile("retail_pulse_years.xls")
df_y_PT = pd.read_excel(xls_y,'PT')
df_y_ES = pd.read_excel(xls_y,'ES')
df_y_IT = pd.read_excel(xls_y,'IT')
df_y_DE = pd.read_excel(xls_y,'DE')
df_y_FR = pd.read_excel(xls_y,'FR')
df_y_PL = pd.read_excel(xls_y,'PL')
df_y_RO = pd.read_excel(xls_y,'RO')
df_y_UK = pd.read_excel(xls_y,'UK')

df_y = df_y_PT.append([df_y_ES,df_y_IT,df_y_DE,df_y_FR,df_y_PL,df_y_RO,df_y_UK],ignore_index=True)



df_final = df_m
df_final = df_final.append([df_q,df_y], ignore_index=True)
df_final = df_final.round(1)


app.layout = html.Div([
            html.Div([
            html.Div(de.Lottie(options=options, width="20%", height="20%", url=url)),
                   dbc.Row(dbc.Col(html.H1("Retail Pulse"
                                " ", style={'text-align': 'center', 'color':'#7F90AC'}),
                                        className="gs-header gs-text-header padded",
                                        width={'size': 4, 'offset': 1},
                                        ),
                                justify="center", align="center"),


                dbc.Row(dbc.Col(html.Div("Evolution of nominal retail sales in different countries (Source: Eurostat)", style={'text-align': 'center'}), width={'size': 4, 'offset': 1},
                            ),
                    justify="center", align="center"),

                html.Br(),

                html.Br(),
                html.Br(),

                dbc.Row([

                            dbc.Col(html.Label(['Select country:'], style={'font-weight': 'bold'}),
                                width={'size': 2, 'offset': 1}),

                            dbc.Col(html.Label(['Select period:'], style={'font-weight': 'bold'}),
                                                            width={'size': 2, 'offset': 1},
                                                            ),

                        ],
                        justify="center", align="center"),

                dbc.Row([
                    dbc.Col(dcc.Dropdown(id="slct_cntry",
                                options=[
                                    {'label': 'Portugal', 'value': 'PT'},
                                    {'label': 'Spain', 'value': 'ES'},
                                    {'label': 'Germany', 'value': 'DE'},
                                    {'label': 'Italy', 'value': 'IT'},
                                    {'label': 'France', 'value': 'FR'},
                                    {'label': 'Poland', 'value': 'PL'},
                                    {'label': 'Romania', 'value': 'RO'},
                                    {'label': 'United Kingdom', 'value': 'UK'},
                                    ],
                                value= 'PT',
                                multi = False
                                           ),
                                        width={'size': 2, 'offset': 1},
                                        ),
                                dbc.Col(dcc.Dropdown(id="slct_period",
                                                           options=[
                                                               {'label': 'Monthly', 'value': 'MON'},
                                                               {'label': 'Quarterly', 'value': 'QUA'},
                                                               {'label': 'Annual', 'value': 'ANU'},
                                                           ],
                                                           value='MON',
                                                           multi = False
                                                           ),
                                            width={'size': 2, 'offset': 1},
                                            )],
                justify="center", align="center"),

                dbc.Row([
                    dbc.Col(html.Div(id='output_container_country', children=[]),
                                width={'size': 2, 'offset': 1},
                                style={'color':'#e60000'},
                                ),

                    dbc.Col(html.Div(id='output_container_period', children=[]),
                                width={'size': 2, 'offset': 1},
                                style={'color':'#e60000'},
                                ),
                        ] , justify="center", align="center"),
                ],
                style={'width': '100%', 'horizontal-align': 'left'}),


                html.Div([


                dbc.Col(dcc.Graph(id='the_graph', figure={}),
                                                                    ),
                ],
                style={'width': '60%', 'display': 'inline-block', 'vertical-align': 'top'}),

                html.Div([

                 html.Br(),

                  html.Br(),

                html.Br(),

                dbc.Col(html.Div(id='table-container', className='tableDiv'),
                        ),



                ],
                style={'width': '35%', 'display': 'inline-block', 'vertical-align': 'top'}),


                html.Br(),
                html.Br(),

                html.Div([

                html.Br(),
                html.Br(),

                dbc.Row(dbc.Col(html.Div("Values on Retail Pulse are often provisional and subject to monthly official revisions. For further information visit https://ec.europa.eu/eurostat/cache/metadata/en/sts_esms.htm", style={'text-align': 'center'}), width={'size': 6, 'offset': 1},
                            ),
                    justify="center", align="center"),

                ]),


                html.Div([

                html.Br(),
                html.Br(),

                dbc.Row(dbc.Col(html.Div("Developed by SONAE Group Strategy Planning and Control", style={'text-align': 'center'}), width={'size': 6, 'offset': 1},
                            ),
                    justify="center", align="center"),

                html.Br(),
                html.Br(),

                ]),
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
        dff_final = dff_final[dff_final["frequency"] == period_slctd]
        #dff_final.to_excel(r'dff_final.xlsx', index=False)
        dff_final.time = pd.DatetimeIndex(dff_final.time).strftime("%Y-%m-%d")
        fig = px.line(data_frame=dff_final,
                    x='time',
                    y=['Total','Food','Food in non-specialized stores','Food in specialized stores','Non-food','Fuel','Audio and video equipment and household appliances','Fashion','Computers, peripheral units and software','Healthcare','Electronics'],
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
            title=None, orientation="h", y=-0.8, yanchor="top", x=0.5, xanchor="center", font = dict (size=18)
           ),
        )
        fig.update_layout(
            autosize=True,
            height=720,
            margin=dict(l=125, r=125, t=125, b=50),
            )


        categories_to_hide = ['Food','Food in non-specialized stores','Food in specialized stores','Non-food','Fuel','Audio and video equipment and household appliances','Fashion','Computers, peripheral units and software','Healthcare','Electronics']
        fig.for_each_trace(lambda trace: trace.update(visible="legendonly")
                   if trace.name in categories_to_hide else ())

        dff_final.sort_values(by=['time'], inplace=True, ascending=False)


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
                    'backgroundColor': '#e6f7ff',
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
                style_table={'overflowX': 'auto', 'overflowY': 'scroll','height': 600},
                fixed_rows={'headers': True},
        ),


        return container_country, container_period, fig, tab


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=False)


