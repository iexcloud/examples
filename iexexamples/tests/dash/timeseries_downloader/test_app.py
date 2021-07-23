# *****************************************************************************
#
# Copyright (c) 2021, the iexexamples authors.
#
# This file is part of the iexexamples library, distributed under the terms of
# the Apache License 2.0.  The full license can be found in the LICENSE file.
#


class TestTimeseriesDownloaderApp:
    def test_import(self):
        from iexexamples.dash.timeseries_downloader import TimeseriesDownloader

        TimeseriesDownloader()
