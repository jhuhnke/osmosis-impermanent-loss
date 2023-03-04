import matplotlib.pyplot as plt
import numpy as np
import requests
import json
from shiny import ui, render, App, reactive, Inputs, Outputs, Session
from pandas import json_normalize

# Get Liquidity Pool Data
pool_ids = requests.get("https://node-api.flipsidecrypto.com/api/v2/queries/355406c5-ed57-430d-8940-1bf4d11a64cc/data/latest")
pools = pool_ids.json()
pool_id = json_normalize(pools)

# Import Price Data For Last Month
last30_prices = requests.get("https://node-api.flipsidecrypto.com/api/v2/queries/e35fa300-acdb-44d0-a532-5f0ea2daeeee/data/latest")
price_json = last30_prices.json()
prices = json_normalize(price_json)

app_ui = ui.page_fixed(
    ui.panel_title("Osmosis Impermanent Loss Calculator"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_select("pool", "Select A Pool", pool_id['POOL_ID']),
            ui.input_slider("rt1", "Token 1 Percentage Price Change", -100, 100, 0, step=0.5),
            ui.input_slider("rt2", "Token 2 Percentage Price Change", -100, 100, 0, step=0.5)
        ),
        ui.panel_main(
            ui.output_text_verbatim("txt"),
            #ui.output_plot("price_plot")
        )
    )
)

def server(input: Inputs, output: Outputs, session: Session):
    @output
    @render.text
    def txt(): 
        pool_num = pool_id.loc[int(input.pool()), "POOL_ID"]
        token1 = pool_id.loc[int(input.pool()), "TOKEN_1"]
        token2 = pool_id.loc[int(input.pool()), "TOKEN_2"]
        return f"Your Liquidity Pool is {pool_num} \nThis pool consists of {token1} and {token2}"
    
    # @output
    # @render.plot
    # def price_plot():
    #     asset1 = pool_id.loc[int(input.pool()), "ASSET_1"]
    #     asset2 = pool_id.loc[int(input.pool()), "ASSET_2"]
    #     date = prices.loc[prices["CURRENCY"] == asset1, "RECORDED_HOUR"]
    #     price1 = prices.loc[prices["CURRENCY"] == asset1, "PRICE"]
    #     price2 = prices.loc[prices["CURRENCY"] == asset2, "RECORDED_HOUR"]

    #     ## Create the plot 
    #     fig, ax = plt.subplots()
    #     ax.plot(date, price1)
    #     return fig

app = App(app_ui, server, debug=True)