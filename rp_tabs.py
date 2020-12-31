import plotly.express as px  # (version 4.7.0)
import plotly
import plotly.graph_objects as go
import pandas as pd
import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

#proximos passos:
#1.melhorar design - check
#2.explorar outros componentes
#3.adicionar outros países - check
#4.comparação entre países para a mesma categoria - next step
#5.outro tab: selecionar a periodicidade, entre mensal, trimestral, e anual (aqui complica, porque tenho que calcular o ytd) - check



app = dash.Dash(__name__)

# Import and clean data (importing csv into pandas)
xls_m = pd.ExcelFile("C:/Users/afalmeida/Desktop/Retail_pulse_py/retail_pulse_data.xls")
df_m_PT = pd.read_excel(xls_m,'PT')
df_m_ESP = pd.read_excel(xls_m,'ESP')
df_m_IT = pd.read_excel(xls_m,'IT')
df_m_DE = pd.read_excel(xls_m,'DE')


df_m = df_m_PT.append([df_m_ESP,df_m_IT,df_m_DE],ignore_index=True)
df_m


xls_q = pd.ExcelFile("C:/Users/afalmeida/Desktop/Retail_pulse_py/retail_pulse_quarters.xls")
df_q_PT = pd.read_excel(xls_q,'PT')
df_q_ESP = pd.read_excel(xls_q,'ESP')
df_q_IT = pd.read_excel(xls_q,'IT')
df_q_DE = pd.read_excel(xls_q,'DE')


df_q = df_q_PT.append([df_q_ESP,df_q_IT,df_q_DE],ignore_index=True)
df_q


xls_y = pd.ExcelFile("C:/Users/afalmeida/Desktop/Retail_pulse_py/retail_pulse_years.xls")
df_y_PT = pd.read_excel(xls_y,'PT')
df_y_ESP = pd.read_excel(xls_y,'ESP')
df_y_IT = pd.read_excel(xls_y,'IT')
df_y_DE = pd.read_excel(xls_y,'DE')


df_y = df_y_PT.append([df_y_ESP,df_y_IT,df_y_DE],ignore_index=True)
df_y

#1 App layout
app.layout = html.Div([
html.H1("Retail pulse 2.0", style={'text-align': 'left'}),
                dcc.RadioItems(id="slct_cntry",
                    options=[
                        {'label': 'Portugal', 'value': 'PT'},
                        {'label': 'Spain', 'value': 'ES'},
                        {'label': 'Germany', 'value': 'DE'},
                        {'label': 'Italy', 'value': 'IT'},
                        ],
                    value= 'PT',
                    labelStyle = {'display': 'inline-block'}
                ),



                html.Div(id='output_container', children=[]),

                html.Br(),

                dcc.Graph(id='retail_sales_graph_month', figure={}),

                html.Br(),

                dcc.Graph(id='retail_sales_graph_quarter', figure={}),

                html.Br(),

                dcc.Graph(id='retail_sales_graph_years', figure={})

])


#2 Connect the Plotly graphs with Dash Components
@app.callback(
        [Output(component_id='output_container', component_property='children'),
         Output(component_id='retail_sales_graph_month', component_property='figure'),
         Output(component_id='retail_sales_graph_quarter', component_property='figure'),
         Output(component_id='retail_sales_graph_years', component_property='figure')         ],
        [Input(component_id='slct_cntry', component_property='value')],
)


def update_graph(option_slctd):
        print(option_slctd)
        print(type(option_slctd))

        container = "The country chosen by user was: {}".format(option_slctd)

        dff_m = df_m.copy()
        dff_m = dff_m[dff_m["country"] == option_slctd]

        dff_q = df_q.copy()
        dff_q = dff_q[dff_q["country"] == option_slctd]

        dff_y = df_y.copy()
        dff_y = dff_y[dff_y["country"] == option_slctd]

        #3 Ploty
        fig_m = px.line(data_frame=dff_m,
                    x='time',
                    y=['Total','Food','Food in non-specialized stores','Food in specialized stores','Non-food','Fuel','Audio and video equipment and household appliances','Fashion','Computers, peripheral units and software','Healthcare','Eletronics'],
                    template='seaborn',
                    title="<b>Monthly retail sales - growth rate (YoY)<b>",
                    labels={
                        'time': 'time',
                        'y': 'categories'
                }
            )
        fig_q = px.line(data_frame=dff_q,
                    x='time',
                    y=['Total','Food','Food in non-specialized stores','Food in specialized stores','Non-food','Fuel','Audio and video equipment and household appliances','Fashion','Computers, peripheral units and software','Healthcare','Eletronics'],
                    template='seaborn',
                    title="<b>Quarterly retail sales - growth rate (YoY)<b>",
                    labels={
                        'time': 'time',
                        'y': 'categories'
                }
            )


        fig_y = px.line(data_frame=dff_y,
                    x='time',
                    y=['Total','Food','Food in non-specialized stores','Food in specialized stores','Non-food','Fuel','Audio and video equipment and household appliances','Fashion','Computers, peripheral units and software','Healthcare','Eletronics'],
                    template='seaborn',
                    title="<b>Annual retail sales - growth rate (YoY)<b>",
                    labels={
                        'time': 'time',
                        'y': 'categories'
                }
            )

        fig_m.update_traces(mode='markers+lines')
        fig_m.update_xaxes(rangeslider_visible=True)
        #plotly.offline.plot(fig, filename="Retail_Pulse.html")
        fig_m.update_layout(  # customize font and legend orientation & position
            font_family="Calibri",
            legend=dict(
            title=None, orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center"
           )
        )
        fig_m.update_layout(
            autosize=False,
            width=1280,
            height=720,
            margin=dict(l=125, r=125, t=125, b=50),
            )
        #plotly.offline.plot(fig_m, filename="Retail_Pulse_months.html")

        fig_q.update_traces(mode='markers+lines')
        fig_q.update_xaxes(rangeslider_visible=True)
        fig_q.update_layout(  # customize font and legend orientation & position
                font_family="Calibri",
                legend=dict(
                title=None, orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center"
           )
        )
        fig_q.update_layout(
            autosize=False,
            width=1280,
            height=720,
            margin=dict(l=125, r=125, t=125, b=50),
            )
        #plotly.offline.plot(fig_q, filename="Retail_Pulse_quarters.html")

        fig_y.update_traces(mode='markers+lines')
        fig_y.update_xaxes(rangeslider_visible=True)
        fig_y.update_layout(  # customize font and legend orientation & position
            font_family="Calibri",
            legend=dict(
            title=None, orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center"
           )
        )
        fig_y.update_layout(
            autosize=False,
            width=1280,
            height=720,
            margin=dict(l=125, r=125, t=125, b=50),
            ),
        #plotly.offline.plot(fig_y, filename="Retail_Pulse_annual.html")

        return container, fig_m, fig_q, fig_y


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=False)


