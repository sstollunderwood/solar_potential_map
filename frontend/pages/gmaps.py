import streamlit as st
import pandas as pd

def main():
    # Set up the page title
    st.title("Display Map")

    # Create a data frame with latitude and longitude columns
    data = pd.DataFrame({
        "latitude": [37.7749],
        "longitude": [-122.4194]
    })

    # Display the map
    st.write("Map:")
    st.map(data)

if __name__ == "__main__":
    main()
