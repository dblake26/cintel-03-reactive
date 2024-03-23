
import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
from palmerpenguins import load_penguins # This package provides the Palmer Penguins dataset
import pandas as pd 
import seaborn as sns
from shiny import reactive, render, req

# Use the built-in function to load the Palmer Penguins dataset
penguins_df = load_penguins()

#name the page
ui.page_opts(title="Desiree's Penguin Data", fillable=True)


# Add a Shiny UI sidebar for user interaction
with ui.sidebar(open="open"):  # Set the open parameter to "open" to make the sidebar open by default
    # Add a second-level header to the sidebar
    ui.h2("Sidebar")

# Use ui.input_selectize() to create a dropdown input to choose a column
    ui.input_selectize(
        "selected_attribute", 
        "Select Attribute",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
    )

# Use ui.input_numeric() to create a numeric input for the number of Plotly histogram bins
    ui.input_numeric("plotly_bin_count", "Number of Plotly Histogram Bins", 40)

# Use ui.input_slider() to create a slider input for the number of Seaborn bins
    ui.input_slider("seaborn_bin_count", "Number of Seaborn Bins", 1, 40, 20)

# Use ui.input_checkbox_group() to create a checkbox group input to filter the species
    ui.input_checkbox_group(
        "selected_species_list", 
        "Select Species", 
        ["Adelie", "Gentoo", "Chinstrap"], 
        selected=["Adelie", "Gentoo", "Chinstrap"], 
        inline=False
    )

# Create checkbox group for island selection
    ui.input_checkbox_group(
        "selected_island_list", 
        "Filter by Island:", 
                            choices=["Torgersen", "Biscoe", "Dream"], 
                            selected=["Torgersen", "Biscoe", "Dream"], inline=True)    

# Use ui.hr() to add a horizontal rule to the sidebar
    ui.hr()

# Use ui.a() to add a hyperlink to Github
    ui.a("GitHub", href="https://github.com/dblake26/cintel-02-data", target="_blank")

# When passing in multiple arguments to a function, separate them with commas.

# Creates a DataTable showing all data

# Main content
with ui.layout_columns():
    with ui.card(full_screen=True):  
        ui.h6("Penguins Data Table")

        @render.data_frame
        def penguins_data_table():
            return render.DataTable(filtered_data())
            
    with ui.card(full_screen=True):
        ui.h6("Penguins Data Grid")

        @render.data_frame
        def penguins_data_grid():
            return render.DataGrid(filtered_data())
# added a horizontal rule
ui.hr()

with ui.layout_columns():
# Creates a Plotly Histogram showing all species
    with ui.card(full_screen=True):
        ui.h6("Species Plotly Histogram")
    
        @render_plotly
        def plotly_histogram():
            return px.histogram(
                filtered_data(), 
                x=input.selected_attribute(), 
                nbins=input.plotly_bin_count()
        )

# Creates a Seaborn Histogram showing all species

    with ui.card(full_screen=True):
        ui.h6("Seaborn Histogram")

        @render.plot(alt="Seaborn Histogram")
        def seaborn_histogram():
            histplot = sns.histplot(
                data=filtered_data(), 
                x="body_mass_g",
                bins=input.seaborn_bin_count())
            
            histplot.set_title("Palmer Penguins")
            histplot.set_ylabel("Measurement")

# Creates a Plotly Scatterplot showing all species

    with ui.card(full_screen=True):
        ui.h6("Plotly Scatterplot: Species")

        @render_plotly
        def plotly_scatterplot():
            return px.scatter(filtered_data(),
                x="flipper_length_mm",
                y="body_mass_g",
                color="species",
                hover_name="island",
                labels={
                    "flipper_length_mm": "Flipper Length (mm)",
                    "body_mass_g": "Body Mass (g)",
                    "species": "Species",
                    "bill_length_mm": "Bill Length (mm)",
                    "island": "Island"
            },
            title="Penguin Species Measurements",
            size_max=12
        )
            # ---------
# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

# Add a reactive calculation to filter the data
# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input functions used to generate that output changes.
# Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.

@reactive.calc
def filtered_data():
    return penguins_df
