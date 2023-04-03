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

app_ui = ui.page_fixed(
    ui.tags.head(
        ui.tags.style(
            (Path(__file__).parent / "style.css").read_text(), 
        ),
    ),
    ui.row(
        ui.column(
            12,
            ui.row(
                ui.tags.h2({"class": "title"}, "Osmosis Impermanent Loss Calculator"), 
            ),
            ui.row(
                ui.tags.strong("How To Use:"),
                ui.tags.p("Fill out all the outlined boxes, using negative numbers to denote a decrease in token price. Other values will auto-populate based off the selected pool and other input values. On-chain pool and token pricing data is sourced from Flipside Crypto."),
            ),
            ui.row(
                ui.tags.strong("Important:"), 
                ui.tags.p("This calculator is not meant to be investment or financial advice."),
            ),
            ui.row(
                ui.hr()
            ),
            ui.row(
                ui.tags.h5({"class": "heading"}, "Input Values"),
            ), 
            ui.row(
                ui.column(
                    3
                ),
                ui.column(
                    3, 
                    ui.input_select("pool", "Select A Pool", pool_id['POOL_ID']),
                ), 
                ui.column(
                    3,
                    ui.input_numeric("fee", "Percent Pool Fee", value = 0.2, step=0.05) 
                ),
                ui.column(
                    3,
                ),
            ),
            ui.row(
                ui.column(
                    3, 
                ), 
                ui.column(
                    3, 
                    ui.tags.h6({"class": "output_text"}, "Token 1"),
                ), 
                ui.column(
                    3, 
                    ui.tags.h6({"class": "output_text"}, "Token 2"),
                ), 
                ui.column(
                    3, 
                    ui.tags.h6({"class": "output_text"}, "Total"),
                ), 
            ),
            ui.row(
                ui.column(
                    3, 
                ), 
                ui.column(
                    3,
                    ui.output_text_verbatim("symbol1"),
                ),
                ui.column(
                    3, 
                    ui.output_text_verbatim("symbol2"),
                ), 
                ui.column(
                    3, 
                ), 
            ),
            ui.row(
                ui.column(
                    3,
                    ui.tags.h6({"class": "col-label"}, "# Tokens"),
                ), 
                ui.column(
                    3, 
                    ui.input_numeric("t1", None, value = 1),
                ), 
                ui.column(
                    3, 
                    ui.input_numeric("t2", None, value = 1),
                ), 
                ui.column(
                    3, 
                ), 
            ),
            ui.row(
                ui.column(
                    3,
                    ui.tags.h6({"class": "col-label"}, "% Price Change"),
                ), 
                ui.column(
                    3, 
                    ui.input_numeric("rt1", None, value = -2.0),
                ), 
                ui.column(
                    3, 
                    ui.input_numeric("rt2", None, value = 1),
                ), 
                ui.column(
                    3, 
                ), 
            ),
            ui.row(
                ui.column(
                    3,
                    ui.tags.h6({"class": "col-label"}, "Price (30 Day Avg)"),
                ), 
                ui.column(
                    3, 
                    ui.output_text_verbatim("mov_avg1"),
                ), 
                ui.column(
                    3, 
                    ui.output_text_verbatim("mov_avg2"),
                ), 
                ui.column(
                    3, 
                ), 
            ),
            ui.row(
                ui.column(
                    3,
                    ui.tags.h6({"class": "col-label"}, "USD Value"),
                ), 
                ui.column(
                    3, 
                    ui.output_text_verbatim("usd_val1"),
                ), 
                ui.column(
                    3, 
                    ui.output_text_verbatim("usd_val2"),
                ), 
                ui.column(
                    3, 
                    ui.output_text_verbatim("usd_valt"),
                ), 
            ),
            ui.row(
                ui.hr()
            ),
            ui.row(
                ui.tags.h5({"class": "heading"}, "Future Values"),
            ), 
            ui.row(
                ui.column(
                    3, 
                ), 
                ui.column(
                    3, 
                    ui.tags.h6({"class": "output_text"}, "Token 1"),
                ), 
                ui.column(
                    3, 
                    ui.tags.h6({"class": "output_text"}, "Token 2"),
                ), 
                ui.column(
                    3, 
                    ui.tags.h6({"class": "output_text"}, "Total")
                ), 
            ),
            ui.row(
                ui.column(
                    3,
                    ui.tags.h6({"class": "col-label"}, "# Tokens") 
                ), 
                ui.column(
                    3, 
                    ui.output_text_verbatim("f_t1"),
                ), 
                ui.column(
                    3, 
                    ui.output_text_verbatim("f_t2"),
                ), 
                ui.column(
                    3,        
                ), 
            ),
            ui.row(
                ui.column(
                    3,
                    ui.tags.h6({"class": "col-label"}, "USD Value") 
                ), 
                ui.column(
                    3, 
                    ui.output_text_verbatim("f_lp1"),
                ), 
                ui.column(
                    3, 
                    ui.output_text_verbatim("f_lp2"),
                ), 
                ui.column(
                    3,
                    ui.output_text_verbatim("f_lpt")        
                ), 
            ),
            ui.row(
                ui.column(
                    3,
                    ui.tags.h6({"class": "col-label"}, "Hodl Value") 
                ), 
                ui.column(
                    3, 
                    ui.output_text_verbatim("f_h1"),
                ), 
                ui.column(
                    3, 
                    ui.output_text_verbatim("f_h2"),
                ), 
                ui.column(
                    3,
                    ui.output_text_verbatim("f_ht")        
                ), 
            ),
            ui.row(
                ui.column(
                    12,
                    ui.tags.textarea("Powered By Flipside \nMade With ❤️ By @web3_analyst")
                ),  
            ),
        ),
    ),
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

        return t1_lp_exit, t2_lp_exit, total_lp_exit, t1_hodl, t2_hodl, t2_hodl_total, lp_val_entry, t1_lp, t2_lp
    
    @reactive.Calc
    async def usd_values(): 
        moving = await moving_avg()
        v1 = moving[0]*input.t1()
        v2 = moving[1]*input.t2()
        vt = moving[0]*input.t1()+moving[1]*input.t2()

        return v1, v2, vt

    
    @output
    @render.text
    def token1(): 
        token1 = pool_id.loc[int(input.pool()), "TOKEN_1"]
        return f"{token1}"
    
    @output
    @render.text
    def token2(): 
        token2 = pool_id.loc[int(input.pool()), "TOKEN_2"]
        return f"{token2}"
    
    @output
    @render.text
    def symbol1(): 
        symbol1 = pool_id.loc[int(input.pool()), "SYMBOL_1"]
        return f"{symbol1}"
    
    @output
    @render.text
    def symbol2(): 
        symbol2 = pool_id.loc[int(input.pool()), "SYMBOL_2"]
        return f"{symbol2}"
    
    @output
    @render.text
    async def mov_avg1(): 
        moving = await moving_avg()
        return f"${round(moving[0], 3)}"
    
    @output
    @render.text
    async def mov_avg2(): 
        moving = await moving_avg()
        return f"${round(moving[1], 3)}"
    
    @output
    @render.text
    async def usd_val1(): 
        moving = await moving_avg()
        return f"${round(moving[0]*input.t1(), 3)}"
    
    @output
    @render.text
    async def usd_val2(): 
        moving = await moving_avg()
        return f"${round(moving[1]*input.t2(), 3)}"
    
    @output
    @render.text
    async def usd_valt(): 
        moving = await moving_avg()
        return f"${round(moving[0]*input.t1()+moving[1]*input.t2(), 3)}"
    
    @output 
    @render.text
    async def f_t1(): 
        end = await end_values()
        return f"{round(end[7], 3)}"
    
    @output 
    @render.text
    async def f_t2(): 
        end = await end_values()
        return f"{round(end[8], 3)}"
    
    @output 
    @render.text
    async def f_lp1(): 
        start = await usd_values()
        end = await end_values()
        return f"${round((start[0]+end[0])*(100-input.fee())/100, 3)}"
    
    @output 
    @render.text
    async def f_lp2(): 
        start = await usd_values()
        end = await end_values()
        return f"${round(start[1]+end[1]*(100-input.fee())/100, 3)}"
    
    @output 
    @render.text
    async def f_lpt():
        start = await usd_values()
        end = await end_values()
        return f"${round(start[2]+end[2]*(100-input.fee())/100, 3)}"
    
    @output 
    @render.text
    async def f_h1(): 
        start = await usd_values()
        end = await end_values()
        return f"${round(start[0]+end[3], 3)}"
    
    @output 
    @render.text
    async def f_h2(): 
        start = await usd_values()
        end = await end_values()
        return f"${round(start[1]+end[4], 3)}"
    
    @output 
    @render.text
    async def f_ht(): 
        start = await usd_values()
        end = await end_values()
        return f"${round(start[2]+end[5], 3)}"
    
www_dir = Path(__file__).parent
app = App(app_ui, server, debug=True, static_assets=www_dir)