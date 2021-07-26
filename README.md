# IEX Cloud - examples
Example applications, dashboards, scripts, notebooks, and other utilities built using [IEX Cloud](https://iexcloud.io/).

# ⚠️ This collection is under active development. [Reach out with comments, questions, or suggestions](https://iexcloud.io/community/developer)

| Preview | Name | Type | Language | Frameworks / Libraries | Datasets |
|:---:|:---:|:---:|:---:|:---:|:---:|
| <img width="150" src="./docs/img/ohlcv.png" alt="OHLCV"></img> | [OHLCV](./notebooks/1_OHLCV.ipynb) | Notebook | Python | [Pandas](https://pandas.pydata.org), [Matplotlib](https://matplotlib.org), [Plotly](https://plotly.com/python/) | [Historical Prices](https://iexcloud.io/docs/api/#historical-prices)  |
| <img width="150" src="./docs/img/timeseries_downloader.png" alt="Timeseries Downloader"></img> | [Timeseries Downloader](./iexexamples/dash/timeseries_downloader/) | App | Python | [Dash](https://dash.plotly.com), [Pandas](https://pandas.pydata.org) | [Time Series](https://iexcloud.io/docs/api/#time-series) |
| <img width="150" src="./docs/img/dash_yield_curve.png" alt="Dash Yield Curve"></img> | [Yield Curve](./iexexamples/dash/yield_curve/) | App | Python | [Dash](https://dash.plotly.com), [Pandas](https://pandas.pydata.org) | [Time Series](https://iexcloud.io/docs/api/#time-series), [Treasuries](https://iexcloud.io/docs/api/#treasuries), [Economic](https://iexcloud.io/docs/api/#economic-data) |

## Cloud Setup
[![](https://img.shields.io/badge/Launch-Cloud%20Instance-brightgreen?style=for-the-badge)](http://mybinder.org/v2/gh/iexcloud/examples/main?urlpath=lab)


## Local Setup
Install dependencies

`python -m pip install -e .`


## License

This software is licensed under the Apache 2.0 license. See the
[LICENSE](LICENSE) and [AUTHORS](AUTHORS) files for details.