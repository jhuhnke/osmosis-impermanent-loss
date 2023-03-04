import matplotlib.pyplot as plt
import numpy as np
import requests
import json
from shiny import ui, render, App, reactive, Inputs, Outputs, Session
from pandas import json_normalize
from pathlib import Path

# Get Liquidity Pool Data
pool_ids = requests.get("https://node-api.flipsidecrypto.com/api/v2/queries/355406c5-ed57-430d-8940-1bf4d11a64cc/data/latest")
pools = pool_ids.json()
pool_id = json_normalize(pools)

# Import Price Data For Last Month
last30_prices = requests.get("https://node-api.flipsidecrypto.com/api/v2/queries/e35fa300-acdb-44d0-a532-5f0ea2daeeee/data/latest")
price_json = last30_prices.json()
prices = json_normalize(price_json)

app_ui = ui.page_fluid(
    ui.tags.style((Path(__file__).parent / "style.css").read_text()),
    ui.tags.h2({"class": "title"}, "Osmosis Impermanent Loss Calculator"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_select("pool", "Select A Pool", pool_id['POOL_ID']),
            ui.input_numeric("t1", "Number of Token 1", value = 1),
            ui.input_slider("rt1", "Token 1 Percentage Price Change", -100, 100, 0, step=0.5),
            ui.input_numeric("t2", "Number of Token 2", value = 1),
            ui.input_slider("rt2", "Token 2 Percentage Price Change", -100, 100, 0, step=0.5),
            ui.input_numeric("time", "Number of Days You Plan To LP", value = 10)
        ),
        ui.panel_main(
            ui.output_text_verbatim("txt"),
            ui.output_text_verbatim("mov_avg"), 
            ui.output_text_verbatim("values")
            #ui.output_plot("price_plot")
        )
    )
)

def server(input: Inputs, output: Outputs, session: Session):
    @reactive.Calc
    async def moving_avg():
        if input.pool() == "":
            return ""
        asset1 = pool_id.loc[int(input.pool()), "ASSET_1"]
        asset2 = pool_id.loc[int(input.pool()), "ASSET_2"]
        t1a = sum(prices.loc[prices["CURRENCY"] == asset1, "PRICE"]) / 720
        t2a = sum(prices.loc[prices["CURRENCY"] == asset2, "PRICE"]) / 720
        return t1a, t2a
    
    @reactive.Calc
    async def end_values(): 
        moving = await moving_avg()
        if input.pool() == "":
            return ""
        
        ## LP values 
        lp_val_entry = (input.t1()*moving[0] + input.t2()*moving[1]) / 2
        t1_lp = ((input.t1()*moving[0] + input.t2()*moving[1]) / 2) / moving[0]
        t2_lp = ((input.t1()*moving[0] + input.t2()*moving[1]) / 2) / moving[1]
        t1_lp_exit = (((input.t1()*moving[0] + input.t2()*moving[1]) / 2) / moving[0]) * moving[0]*input.rt1()/100
        t2_lp_exit = (((input.t1()*moving[0] + input.t2()*moving[1]) / 2) / moving[1]) * moving[1]*input.rt2()/100
        total_lp_exit = ((((input.t1()*moving[0] + input.t2()*moving[1]) / 2) / moving[0]) * moving[0]*input.rt1()/100) + ((((input.t1()*moving[0] + input.t2()*moving[1]) / 2) / moving[1])*moving[1]*input.rt2()/100)

        ## Hodl Values
        t1_hodl = input.t1() * moving[0] * input.rt1() / 100
        t2_hodl = input.t2() * moving[1] * input.rt2() / 100
        t2_hodl_total = t1_hodl + t2_hodl

        return t1_lp_exit, t2_lp_exit, total_lp_exit, t1_hodl, t2_hodl, t2_hodl_total, lp_val_entry
    
    @output
    @render.text
    def txt(): 
        pool_num = pool_id.loc[int(input.pool()), "POOL_ID"]
        token1 = pool_id.loc[int(input.pool()), "TOKEN_1"]
        token2 = pool_id.loc[int(input.pool()), "TOKEN_2"]
        return f"Your Liquidity Pool is {pool_num} \nThis pool consists of {token1} and {token2}"
    
    @output
    @render.text
    async def mov_avg(): 
        moving = await moving_avg()
        return f"The 30 day moving avg of token 1 is ${moving[0]}. \nThe 30 day moving avg of token 2 is ${moving[1]}."
    
    @output 
    @render.text
    async def values(): 
        prices = await end_values() 
        return f"Entry value ${prices[6]} \nThe value of your LP Position Changes By: ${prices[0]} Token 1, ${prices[1]} Token 2, ${prices[2]} Total \nHodl Values Change By: ${prices[3]} Token 1, ${prices[4]} Token 2, and ${prices[5]} in Total."
    
        
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