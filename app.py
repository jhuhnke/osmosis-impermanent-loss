import matplotlib.pyplot as plt
import numpy as np
from shiny import ui, render, App

# Create some random data
choices = [1, 2, 3, 4, 5]

app_ui = ui.page_fixed(
    ui.panel_title("Osmosis Impermanent Loss Calculator"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_select("pool", "Select Liquidity Pool", choices),
            ui.input_slider("rt1", "Token 1 Percentage Price Change", -100, 100, 0, step=0.5),
            ui.input_slider("rt2", "Token 2 Percentage Price Change", -100, 100, 0, step=0.5)
        ),
        ui.panel_main(
            ui.output_text("txt")
        )
    )
)

def server(input, output, session):
    @output
    @render.text
    def txt(): 
        return f"Your Liquidity Pool is {input.pool()}"


app = App(app_ui, server)