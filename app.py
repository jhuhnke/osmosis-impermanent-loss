import matplotlib.pyplot as plt
import numpy as np
import requests
import json
from shiny import ui, render, App, reactive
from pandas import json_normalize

# Get Pool Data
pool_ids = requests.get("https://node-api.flipsidecrypto.com/api/v2/queries/355406c5-ed57-430d-8940-1bf4d11a64cc/data/latest")
pools = pool_ids.json()
pool_id = json_normalize(pools)

app_ui = ui.page_fixed(
    ui.panel_title("Osmosis Impermanent Loss Calculator"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_select("pool", "Select A Pool", pool_id['POOL_ID']),
            ui.input_slider("rt1", "Token 1 Percentage Price Change", -100, 100, 0, step=0.5),
            ui.input_slider("rt2", "Token 2 Percentage Price Change", -100, 100, 0, step=0.5)
        ),
        ui.panel_main(
            ui.output_text_verbatim("txt")
        )
    )
)

def server(input, output, session):
    @reactive.Calc
    async def get_pool():
        pool_num = pool_id.loc[int(input.pool()), "POOL_ID"]
        return pool_num
    
    @output
    @render.text
    async def txt(): 
        pool_num = await get_pool()
        return f"Your Liquidity Pool is {pool_num}"

app = App(app_ui, server, debug=True)