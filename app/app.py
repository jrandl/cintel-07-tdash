# Import required libraries
import seaborn as sns
from faicons import icon_svg
from shiny import reactive
from shiny.express import input, render, ui
import palmerpenguins 

# Load the Palmer Penguins dataset
df = palmerpenguins.load_penguins()

# Configure the page options for the dashboard, setting the title and enabling the 'fillable' feature
ui.page_opts(title="Josiah's Penguins dashboard", fillable=True)

# Add custom CSS styles for the dashboard to use the 'Roboto' font family
ui.tags.style("body { font-family: 'Roboto', sans-serif; }")

# Define a sidebar for user input controls
with ui.sidebar(title="Filter controls"):
    # Slider for filtering penguins by body mass
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    # Checkbox group for selecting species to display
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    # Horizontal line for visual separation
    ui.hr()
    # Section for useful links
    ui.h6("Links")
    # Various hyperlinks to resources and related sites
    ui.a("GitHub Source", href="https://github.com/jrandl/cintel-07-tdash", target="_blank")
    ui.a("GitHub App", href="https://jrandl.github.io/cintel-07-tdash/", target="_blank")
    ui.a("GitHub Issues", href="https://github.com/jrandl/cintel-07-tdash/issues", target="_blank")
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a("Template: Basic Dashboard", href="https://shiny.posit.co/py/templates/dashboard/", target="_blank")
    ui.a("See also", href="https://github.com/denisecase/pyshiny-penguins-dashboard-express", target="_blank")

# Layout for data visualization and information display
with ui.layout_column_wrap(fill=False):
    # Display box for showing total count of penguins after filtering
    with ui.value_box(showcase=icon_svg("earlybirds")):
        "Number of penguins"
        # Render the text dynamically based on filtered data
        @render.text
        def count():
            return filtered_df().shape[0]

    # Display average bill length of the filtered data
    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average bill length"
        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    # Display average bill depth of the filtered data
    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average bill depth"
        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

# Layout for plotting and displaying data tables
with ui.layout_columns():
    # Column for scatterplot of bill dimensions
    with ui.card(full_screen=True):
        ui.card_header("Bill length and depth")
        @render.plot
        def length_depth():
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
            )

    # Column for displaying a data table of penguin metrics
    with ui.card(full_screen=True):
        ui.card_header("Penguin Data")
        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)

# Define a reactive calculation for filtering the dataframe based on user inputs
@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
