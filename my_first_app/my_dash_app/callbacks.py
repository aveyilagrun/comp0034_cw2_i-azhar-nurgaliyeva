import json
from dash import Output, Input
import pandas as pd
import plotly.express as px
from my_first_app.my_dash_app.layout import df, line_fig, line_graph_tab, bar_graph_tab, pie_chart_tab, subplots_tab, \
    box_plots_tab


def register_callbacks(dash_app):
    """ Create the callbacks for a Plotly Dash dash_app. """

    @dash_app.callback(Output('tabs-content', 'children'),
                       Input('tabs', 'value'))
    def changing_tabs(tab):
        """ Changing tabs function for callback

        Args:
            tab: user clicks on the tab

        Returns:
            tab: specific tab with the visualisation

        """
        if tab == 'tab-1':
            return line_graph_tab
        if tab == 'tab-2':
            return bar_graph_tab
        if tab == 'tab-3':
            return pie_chart_tab
        if tab == 'tab-4':
            return subplots_tab
        if tab == 'tab-5':
            return box_plots_tab

        return ''

    @dash_app.callback(
        Output(component_id='line-graph', component_property='figure'),
        Input(component_id='journey-types-dropdown', component_property='value'))
    def update_line_graph(selected_type):
        """ Updating line graph

            Args:
                selected_type: a journey type chosen by the user

            Returns:
                line_fig_new: new line graph with only that journey type

            """
        if selected_type is not None:
            filtered_journeys = df[['Period ending', f'{selected_type}']]
            line_fig_new = px.line(filtered_journeys, x='Period ending',
                                   y=f'{selected_type}',
                                   title=f'Usage of {selected_type} in London')
        else:
            line_fig_new = line_fig
        return line_fig_new

    @dash_app.callback(
        Output(component_id='pie-graph', component_property='figure'),
        Input(component_id='timeline-slider', component_property='value'))
    def update_pie_graph(selected_year):
        """ Updating pie graph

            Args:
                selected_year: a timeline chosen by the user

            Returns:
                pie_fig_new: new pie graph with specific timeline

        """
        filtered_timeline = pd.DataFrame()
        if int(selected_year[1]) - int(selected_year[0]) == 1:
            for i in selected_year:
                filtered_timeline = filtered_timeline.append(
                    df[df['Period ending'].astype(str).str.contains(f'{i}') == True])
        elif int(selected_year[1]) - int(selected_year[0]) == 2:
            selected_year.append(int(selected_year[1]) - 1)
            for i in selected_year:
                filtered_timeline = filtered_timeline.append(
                    df[df['Period ending'].astype(str).str.contains(f'{i}') == True])
        elif int(selected_year[1]) - int(selected_year[0]) == 3:
            selected_year.append(int(selected_year[1]) - 1)
            selected_year.append(int(selected_year[1]) - 2)
            for i in selected_year:
                filtered_timeline = filtered_timeline.append(
                    df[df['Period ending'].astype(str).str.contains(f'{i}') == True])
        elif int(selected_year[1]) == int(selected_year[0]):
            filtered_timeline = filtered_timeline.append(
                df[df['Period ending'].astype(str).str.contains(f'{selected_year[0]}') == True])
        pie_df_new = filtered_timeline[
            ['Bus journeys (m)', 'Underground journeys (m)', 'DLR journeys (m)', 'Tram journeys (m)',
             'Overground journeys (m)', 'Emirates Airline journeys (m)', 'TfL Rail journeys (m)']].sum()
        pie_fig_new = px.pie(values=pie_df_new.values, names=pie_df_new.index,
                             title="Amount of journeys in a year")
        return pie_fig_new

    @dash_app.callback(
        Output("box-graph", "figure"),
        Input("y-axis", "value"))
    def update_box_plots(y_value):
        """ Updating box plots

            Args:
                y_value: a journey type chosen by the user

            Returns:
                box_fig_new: new box plot for only that journey type

        """
        box_fig_new = px.box(df, y=df[y_value])
        return box_fig_new
