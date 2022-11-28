import folium
import pandas as pd


def main():
    # Initialize map object and set starting point to center map upon loading.
    map = folium.Map(
        location=[42.681339, -89.026932], tiles="Stamen Terrain", zoom_start=5
    )

    # Add a volcano layer
    volcano_ft_grp = folium.FeatureGroup(name="Volcano Layer")

    # Add a population layer
    population_ft_grp = folium.FeatureGroup(name="Population Layer")

    # Add data into population layer via .json file
    population_ft_grp.add_child(
        folium.GeoJson(
            data=open("world.json", "r", encoding="utf-8-sig").read(),
            style_function=lambda x: {
                "fillColor": "green"
                if x["properties"]["POP2005"] < 10_000_000
                else "orange"
                if 10_000_000 <= x["properties"]["POP2005"] < 20_000_000
                else "red"
            },
        )
    )

    # Load in the dataframe that contains the volcano information for the USA
    df = pd.read_csv("Volcanoes.txt", sep=",", index_col=False)

    # Create list objects from volcano df to use in for loops to create markers
    lat = list(df.LAT)
    lon = list(df.LON)
    elevation = list(df.ELEV)
    volc_name = list(df.NAME)
    volc_type = list(df.TYPE)

    # HTML code for the volcano icon popup window
    icon_html = """
    Volcano Name<br>
    <a href="https://www.google.com/search?q=%%22%s%%22+volcano" 
    target="_blank">%s</a><br>
Height: %s meters<br>
Type: %s
    """

    # Use for loop to add all of the volcano markers listed in the .txt file
    # This places all of the volcanos into one single feature group layer
    for lt, lg, el, nm, typ in zip(
        lat,
        lon,
        elevation,
        volc_name,
        volc_type,
    ):
        iframe = folium.IFrame(
            html=icon_html % (nm, nm, el, typ), width=200, height=100
        )
        volcano_ft_grp.add_child(
            folium.CircleMarker(
                radius=7,
                location=[lt, lg],
                popup=folium.Popup(iframe),
                color="gray",
                fill=True,
                fill_color=color_producer(el),
                fill_opacity=0.7,
            )
        )

    # Add both of the created layers to the overall map
    map.add_child(population_ft_grp)
    map.add_child(volcano_ft_grp)

    # Add layer control feature
    map.add_child(folium.LayerControl())
    # Save created map
    map.save("volcano_map.html")


def color_producer(elevation):
    """Colorize Volcano markers based on elevation (in meters)"""
    if elevation < 1000:
        return "green"
    elif elevation > 1000 and elevation < 2000:
        return "orange"
    elif elevation > 2000 and elevation < 3000:
        return "red"
    else:
        return "darkred"


if __name__ == "__main__":
    main()
