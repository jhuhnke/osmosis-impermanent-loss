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
    ui.row(
        ui.column(
            6,
            ui.tags.div(class_="box", children=[
                ui.tags.div(class_="pool_selector", children=[
                    ui.input_select("pool", "Select A Pool", pool_id['POOL_ID']),
                ]),
                ui.tags.div(class_="pool_tokens", children=[
                    ui.row(
                        ui.column(
                            6, 
                            ui.tags.h5({"class": "token_name"}, "Token 1"),
                        ), 
                        ui.column(
                            6, 
                            ui.output_text_verbatim("token1")
                        ),
                    ),
                    ui.row(
                        ui.column(
                            4, 
                            ui.input_numeric("t1", "Number of Token 1", value = 1),
                        ), 
                        ui.column(
                            8, 
                            ui.input_slider("rt1", "Token 1 Percentage Price Change", -100, 100, 0, step=0.5),
                        ),
                    ),
                    ui.row(
                        ui.column(
                            6, 
                            ui.tags.h5({"class": "token_name"}, "Token 2"),
                        ), 
                        ui.column(
                            6, 
                            ui.output_text_verbatim("token2")
                        ),
                    ),
                    ui.row(
                        ui.column(
                            4, 
                            ui.input_numeric("t2", "Number of Token 2", value = 1),
                        ), 
                        ui.column(
                            8, 
                            ui.input_slider("rt2", "Token 2 Percentage Price Change", -100, 100, 0, step=0.5),
                        ),
                    ),
                ]), 
            ]),
        ),
        ui.column(
            6,
            ui.tags.div(class_="box", children=[
                ui.row(
                    ui.tags.h5({"class": "heading"}, "Input Values"),
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
                        ui.output_text_verbatim("num_t1"),
                    ), 
                    ui.column(
                        3, 
                        ui.output_text_verbatim("num_t2"),
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
            ])
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
    def num_t1(): 
        return f"{str(input.t1())}"
    
    @output
    @render.text
    def num_t2(): 
        return f"{str(input.t2())}"
    
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
        end = await end_values()
        return f"${round(end[0], 3)}"
    
    @output 
    @render.text
    async def f_lp2(): 
        end = await end_values()
        return f"${round(end[1], 3)}"
    
    @output 
    @render.text
    async def f_lpt(): 
        end = await end_values()
        return f"${round(end[2], 3)}"
    
    @output 
    @render.text
    async def f_h1(): 
        end = await end_values()
        return f"${round(end[3], 3)}"
    
    @output 
    @render.text
    async def f_h2(): 
        end = await end_values()
        return f"${round(end[4], 3)}"
    
    @output 
    @render.text
    async def f_ht(): 
        end = await end_values()
        return f"${round(end[5], 3)}"
    

app = App(app_ui, server, debug=True)