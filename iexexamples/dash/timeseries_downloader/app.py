# *****************************************************************************
#
# Copyright (c) 2021, the iexexamples authors.
#
# This file is part of the iexexamples library, distributed under the terms of
# the Apache License 2.0.  The full license can be found in the LICENSE file.
#

import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import pyEX as p
import os
import os.path


_RANGES = [
    "1d",
    "5d",
    "30d",
    "1m",
    "3m",
    "6m",
    "9m",
    "1y",
    "2y",
    "3y",
]


class TimeseriesDownloader(object):
    def __init__(self):
        # Instantiate dash instance
        self.app = dash.Dash(
            title="Timeseries Downloader",
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

        # initialize the layout
        self.initializeLayout()

        # initialize callbacks
        self.initializeCallbacks()

        # initialize data
        self.initializeData()

    def initializeLayout(self):
        # Dropdown containing all timeseries IDs
        self.id_dropdown = dcc.Dropdown(
            id="id-dropdown",
            className="mb2",
            options=[],
            value=None,
        )

        # Dropdown containing all timeseries keys
        # for the provided timeseries ID
        self.key_dropdown = dcc.Dropdown(
            id="key-dropdown",
            className="mb2",
            options=[],
            value=None,
        )

        # Dropdown containing all timeseries subkeys
        # for the provided timeseries ID and key
        self.subkey_dropdown = dcc.Dropdown(
            id="subkey-dropdown",
            className="mb2",
            options=[],
            value=None,
        )

        # Dropdown with collection of supported
        # ranges
        self.range_dropdown = dcc.Dropdown(
            id="range-dropdown",
            className="mb2",
            options=[{"label": x, "value": x} for x in _RANGES],
            clearable=False,
            value="1m",
        )

        # Text input for the folder to which the
        # downloaded CSVs should be emitted
        self.location_input = dcc.Input(
            id="location-input",
            placeholder="Path to output folder...",
            type="text",
            value="",
            required=True,
        )

        # setup base layout
        self.app.layout = html.Section(
            style={"height": "110vh"},  # slightly oversize for good chart dimensions
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
                            children="Timeseries Downloader",
                            style={"paddingTop": "25px"},
                        ),
                        html.P(
                            className="section-subtitle px2",  # these are dictated by cloud.css
                            children="Browse and download timeseries datasets",
                        ),
                    ],
                ),
                html.Div(
                    className="flex",
                    children=[
                        html.Div(
                            className="flex flex-column",
                            children=[
                                html.Label(
                                    className="header-subtitle mb2", children="ID"
                                ),
                                html.Label(
                                    className="header-subtitle mb2", children="Key"
                                ),
                                html.Label(
                                    className="header-subtitle mb2", children="SubKey"
                                ),
                                html.Label(
                                    className="header-subtitle mb2", children="Range"
                                ),
                                html.Label(
                                    className="header-subtitle mb2", children="Location"
                                ),
                            ],
                        ),
                        html.Div(
                            className="flex flex-column flex-1-auto pl2",
                            children=[
                                dcc.Loading(children=self.id_dropdown),
                                dcc.Loading(self.key_dropdown),
                                dcc.Loading(self.subkey_dropdown),
                                dcc.Loading(self.range_dropdown),
                                dcc.Loading(self.location_input),
                            ],
                        ),
                    ],
                ),
                html.Button(
                    id="download-data",
                    className="cloud-btn",
                    children="Download",
                ),
                dcc.Loading(
                    html.Label(
                        id="data-download-done",
                        style={"display": "none"},
                        children="",
                    ),
                ),
                # These two are just placeholder targets for
                # callbacks that dont really do anything
                html.Div(id="fake-output1", style={"display": "none"}),
                html.Div(id="fake-output2", style={"display": "none"}),
            ],
        )

    def initializeCallbacks(self):
        # Callback to populate key input based on ID
        @self.app.callback(
            Output("key-dropdown", "options"),
            Input("id-dropdown", "value"),
        )
        def handleIdChange(idDropdownValue):
            # TODO why didnt this happen automatically?
            self.id_dropdown.value = idDropdownValue
            if idDropdownValue is None:
                # user has not picked an ID, so return []
                return []

            ret = []
            for x in self.client.queryMetadata(id=idDropdownValue):
                ret.append({"label": x["value"], "value": x["value"]})
            return ret
            # return [{"label": x["value"], "value": x["value"]} for x in self.client.queryMetadata(id=idDropdownValue)]

        # Callback to populate subkey input based on key
        @self.app.callback(
            Output("subkey-dropdown", "options"),
            Input("key-dropdown", "value"),
        )
        def handleKeyChange(keyDropdownValue):
            # TODO why didnt this happen automatically?
            self.key_dropdown.value = keyDropdownValue

            if keyDropdownValue is None:
                # user has not picked an ID, so return []
                return []

            ret = []
            for x in self.client.queryMetadata(
                id=self.id_dropdown.value, key=keyDropdownValue
            ):
                ret.append({"label": x["value"], "value": x["value"]})
            return ret
            # return [{"label": x["value"], "value": x["value"]} for x in self.client.queryMetadata(id=idDropdownValue)]

        # Callback to ensure subkey and range are written properly
        @self.app.callback(
            Output("fake-output1", "children"),
            [
                Input("subkey-dropdown", "value"),
                Input("range-dropdown", "value"),
            ],
        )
        def handleSubKeyChange(subKeyDropdownValue, rangeDropdownValue):
            # TODO why didnt this happen automatically?
            self.subkey_dropdown.value = subKeyDropdownValue
            self.range_dropdown.value = rangeDropdownValue
            return []

        # Callback to ensure location is written properly
        @self.app.callback(
            Output("fake-output2", "children"),
            Input("location-input", "value"),
        )
        def handleLocationChange(locationValue):
            # TODO why didnt this happen automatically?
            self.location_input.value = locationValue
            return []

        # Callback to download and emit file
        @self.app.callback(
            [
                Output("data-download-done", "style"),
                Output("data-download-done", "children"),
            ],
            Input("download-data", "n_clicks"),
        )
        def downloadData(dataClick):
            if dataClick and dataClick > 0 and self.id_dropdown.value:
                # Fetch timeseries data via pyEX
                # as a dataframe
                df = self.client.timeSeriesDF(
                    id=self.id_dropdown.value,
                    key=self.key_dropdown.value,
                    subkey=self.subkey_dropdown.value,
                    range=self.range_dropdown.value,
                    limit=5000,
                )

                # Check if the output folder exists
                folderPath = os.path.abspath(
                    os.path.expanduser(self.location_input.value)
                )
                if os.path.exists(folderPath):
                    filename = "{}_{}_{}_{}.csv".format(
                        self.id_dropdown.value,
                        self.key_dropdown.value,
                        self.subkey_dropdown.value,
                        self.range_dropdown.value,
                    )

                    pathName = os.path.join(folderPath, filename)

                    # emit as CSV file
                    df.to_csv(pathName)

                    outputText = "Downloaded to {}".format(pathName)
                else:
                    outputText = "Folder does not exist: {}".format(
                        self.location_input.value
                    )

                return {"display": "block"}, outputText
            return {"display": "none"}, ""

    def initializeData(self):
        # set initial id dropdown
        # to be all timeseries IDs
        self.id_dropdown.options = [
            {"label": x["value"], "value": x["value"]}
            for x in self.client.queryMetadata()
        ]
