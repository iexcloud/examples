# *****************************************************************************
#
# Copyright (c) 2021, the iexexamples authors.
#
# This file is part of the iexexamples library, distributed under the terms of
# the Apache License 2.0.  The full license can be found in the LICENSE file.
#
# visit http://127.0.0.1:8050/ in your web browser.
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import os
import os.path
import pandas as pd
import pyEX as p

from .charts import yieldCurveSurface, lineOverlay

_curves = {
    "DGS1MO": "1 Month",
    "DGS3MO": "3 Month",
    "DGS6MO": "6 Month",
    "DGS1": "1 Year",
    "DGS2": "2 Year",
    "DGS3": "3 Year",
    "DGS5": "5 Year",
    "DGS7": "7 Year",
    "DGS10": "10 Year",
    "DGS20": "20 Year",
    "DGS30": "30 Year",
}

_overlays = {
    "SPY": {
        "name": "S&P500 ETF",
        "timeseriesId": "HISTORICAL_PRICES",
    },
    "DIA": {
        "name": "DJIA ETF",
        "timeseriesId": "HISTORICAL_PRICES",
    },
    "UNRATE": {
        "name": "Unemployment Rate",
        "timeseriesId": "ECONOMIC",
    },
    "FEDFUNDS": {
        "name": "Federal Funds Rate",
        "timeseriesId": "ECONOMIC",
    },
    "CPIAUCSL": {
        "name": "Consumer Price Index",
        "timeseriesId": "ECONOMIC",
    },
    "A191RL1Q225SBEA": {
        "name": "Real GDP",
        "timeseriesId": "ECONOMIC",
    },
    "MORTGAGE30US": {
        "name": "Thirty Year Mortgage",
        "timeseriesId": "MORTGATE",
    },
    "MORTGAGE15US": {
        "name": "Fifteen Year Mortgage",
        "timeseriesId": "MORTGATE",
    },
    "MORTGAGE5US": {
        "name": "Five Year Mortgage",
        "timeseriesId": "MORTGATE",
    },
    "TOTALSA": {
        "name": "Total Vehicle Sales",
        "timeseriesId": "ECONOMIC",
    },
    "RECPROUSM156N": {
        "name": "US Recession Probabilities",
        "timeseriesId": "ECONOMIC",
    },
    "DCOILWTICO": {
        "name": "WTI",
        "timeseriesId": "ENERGY",
    },
    "DCOILBRENTEU": {
        "name": "Brent",
        "timeseriesId": "ENERGY",
    },
}

_defaultFrom = "2008-01-01"
_defaultTo = "2021-01-01"


class YieldCurveApp(object):
    def __init__(self):
        # Instantiate dash instance
        self.app = dash.Dash(
            title="IEX - Yield Curve",
            suppress_callback_exceptions=True,
            external_stylesheets=["https://iexcloud.io/css/cloud.css"],
        )

        # Initialize layout and callbacks
        self.initialize()

    def run(self):
        """Run the server with debug=False"""
        self.app.run_server(debug=False)

    def debug(self):
        """Run the server with debug=True"""
        self.app.run_server(debug=True)

    def initialize(self):
        """Initialize:
        - pyEX Client
        - Pull data from cache if available
        - Setup Dash layouts
        - Setup Dash callbacks
        """
        # create a client
        try:
            self.client = p.Client()  # set IEX_TOKEN env var or provide here
        except Exception as e:
            print(
                "To run this app, set IEX_TOKEN environmnent variable or hard code in app.py"
            )
            raise e

        # load data from cache if available
        self.loadData()

        # initialize the layout
        self.initializeLayout()

        # initialize the callbacks
        self.initializeCallbacks()

    def initializeLayout(self):
        # Div that contains the 3D chart once we have data available
        self.chart_container = html.Div(
            id="chart-container",  # this is used in a callback below
            className="border mt2 flex",  # these are dictated by cloud.css
            style={"height": "100%", "width": "100%"},
        )

        # Div that contains our overlay multi-select dropdown
        self.overlayconfig_container = html.Div(
            className="px2 flex flex-column flex-1",  # these are dictated by cloud.css
            id="overlayconfig-container",  # this is used in a callback below
            style={
                "display": "none"
            },  # leave hidden to start until we have data and the chart is renderered
            children=[
                # Title of the block
                html.H3(className="section-title mt2", children="Overlay datasets"),
                # Description of the block
                html.P(children="Overlay other datasets from time-series"),
                # Select from a set of other timeseries datasets to overlay
                dcc.Dropdown(
                    id="data-overlay",
                    options=[
                        {"label": v["name"], "value": k} for k, v in _overlays.items()
                    ],
                    multi=True,  # overlay more than one
                    value="",  # dont overlay anything by default
                ),
            ],
        )

        # if i have cached data, adjust button accordingly
        if not self.df.empty:
            # First update the 3D chart
            self.updateChart()

            # show overlay config
            self.overlayconfig_container.style = {}

            # set the data button to "Reload"
            self.load_reload_button = html.Button(
                "Reload",
                id="start-load-data",  # this is used in a callback below
                n_clicks=0,
                className="cloud-btn",  # these are dictated by cloud.css
            )
        else:
            # Make sure figure is none
            self.fig = None

            # No data yet so set button to "Load"
            self.load_reload_button = html.Button(
                "Load",
                id="start-load-data",  # this is used in a callback below
                n_clicks=0,
                className="cloud-btn",  # these are dictated by cloud.css
            )

        # specify div for config content, this holds the data load button
        self.config_container = html.Div(
            id="config-container",
            className="px2 flex flex-column",  # these are dictated by cloud.css
            children=[
                # Title of the block
                html.H3(className="section-title mt2", children="Yield Curve Data"),
                # Description of the block
                html.P(children="Pull historical treasury yield curves"),
                # Load/Reload button
                self.load_reload_button,
            ],
        )

        # setup base layout
        self.app.layout = html.Section(
            style={"height": "110vh"},  # slightly oversize for good chart dimensions
            # Store as:
            # Flex column:
            # Flex column:
            #   Logo
            #     Title
            #     Subtitle
            #
            # Flex Row:
            #  Data Config            Overlay Config
            #
            # Chart
            className="px2 py2 mb4 flex flex-column",  # these are dictated by cloud.css
            children=[
                # Layout is logo / Top level Title / Top level description in column
                html.Div(
                    className="",
                    children=[
                        html.Img(
                            src="https://iexcloud.io/icons/cloud-logo-full.svg",  # pull from website
                            style={"width": "50px"},
                        ),
                        html.H1(
                            className="hero-header",  # this is dictated in cloud.css
                            children="Yield Curve Explorer",
                            style={"paddingTop": "25px"},
                        ),
                        html.P(
                            className="header-subtitle px2",  # these are dictated by cloud.css
                            children="Interactively explorer IEX Cloud Datasets via TimeSeries",
                        ),
                    ],
                ),
                html.Div(
                    # Store data load config and overlay config as flex row
                    className="section flex",
                    children=[
                        self.config_container,
                        self.overlayconfig_container,
                    ],
                ),
                # Finally show chart underneath it all
                html.Div(
                    className="flex-2",
                    children=[dcc.Loading(children=[self.chart_container])],
                ),
            ],
        )

    def initializeCallbacks(self):
        @self.app.callback(
            [
                # Show overlay once data loaded
                Output("overlayconfig-container", "style"),
                # Show chart once data loaded
                Output("chart-container", "children"),
            ],
            [
                # Data load button
                Input("start-load-data", "n_clicks"),
                # Data overlay values
                Input("data-overlay", "value"),
            ],
        )
        def handleLoad(buttonClick, overlays):
            if buttonClick:
                # grab data
                self.buildYieldCurve()

                # set load button to be reload
                self.load_reload_button.value = "Reload"

                # ready to go, move on
                self.updateChart()

                # show overlay config
                self.overlayconfig_container.style = {}

                # add overlays
                self.addOverlays(overlays or [])

            return self.overlayconfig_container.style, self.chart_container.children

    def updateChart(self):
        if not self.df.empty:
            # assemble 3D figure
            self.fig = yieldCurveSurface(self.df)

            # Add graph to chart container
            self.chart_container.children = [
                dcc.Graph(
                    id="3d-graph",
                    figure=self.fig,
                    style={"height": "95%"},
                    className="flex-1",
                ),
            ]

    def addOverlays(self, overlays):
        for overlay in overlays:
            df = self.client.timeSeriesDF(
                _overlays[overlay]["timeseriesId"],
                overlay,
                from_=_defaultFrom,
                to_=_defaultTo,
            )

            if _overlays[overlay]["timeseriesId"] == "HISTORICAL_PRICES":
                df["value"] = df["close"]

            df = df[["date", "value"]]
            df.set_index("date", inplace=True)
            lineOverlay(self.fig, df, _overlays[overlay]["name"])

    def buildYieldCurve(self):
        """build a full yield curve from `from_` to `to_`"""
        dfs = pd.DataFrame()
        for curve in _curves.keys():
            df = self.client.timeSeriesDF(
                "TREASURY",
                curve,
                from_=_defaultFrom,
                to_=_defaultTo,
                filter="date,value",
            )

            # Filter out nones
            # TODO we dont want to do this really because rates can be 0
            df = df[df["value"] > 0]

            # set date column to be index
            df.set_index("date", inplace=True)

            # drop any remaining nans
            dfs[_curves[curve]] = df["value"]

        self.df = dfs
        self.df.dropna(inplace=True)
        self.saveData()

    def saveData(self):
        if self.df.empty:
            # nothing to do
            return
        self.df.to_csv(os.path.join(os.path.dirname(__file__), "data_cache.csv"))

    def loadData(self):
        if os.path.exists(os.path.join(os.path.dirname(__file__), "data_cache.csv")):
            self.df = pd.read_csv(
                os.path.join(os.path.dirname(__file__), "data_cache.csv")
            )

            # parse date columns
            self.df["date"] = pd.to_datetime(self.df["date"])

            # set date column to be index
            self.df.set_index("date", inplace=True)

            # drop any remaining nans
            self.df.dropna(inplace=True)
        else:
            self.df = pd.DataFrame()
