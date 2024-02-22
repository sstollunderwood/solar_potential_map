import streamlit as st
import pydeck as pdk

def main():
    # Set up the page title
    st.title("Solar Potential Map")

    # Set up default location (Le Wagon Tokyo, Meguro)
    default_location = (35.633942, 139.708126)

    # Get user input for location
    location = st.text_input("Enter location:", 'Le Wagon Tokyo, Meguro')

    # Display map
    st.write(f"Map of {location}:")
    lat, lon = default_location
    view_state = pdk.ViewState(
        latitude=lat,
        longitude=lon,
        zoom=15,
        pitch=0
    )
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/satellite-streets-v11",
        initial_view_state=view_state,
        layers=[],
    ))

if __name__ == "__main__":
    main()
