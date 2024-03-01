import numpy as np
import streamlit as st
import googlemaps as gm
import requests
from PIL import Image
import gdown
from utils.params import *
from utils.utils import get_gmaps_image, solar_panel_energy_output, co2_calculator, rooftop_area_calculator


#interact with endpoint
fast_url = "http://0.0.0.0:8000/predict"
endpoint = '/predict'


def send_backend(lat, lng, zoom, fast_url):
    """
    Capture google maps image, put that in list form in a dict
    and send to the fast API back end
    """
    image = get_gmaps_image(lat, lng, zoom)
    image_np = np.array(image)
    data = {'image': image_np.tolist()}

    r = requests.post(fast_url=fast_url,
                      json=data)

    return r

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    """Stateful button, allows the page to change to the
    image + mask when button is clicked"""
    st.session_state.clicked = True

def click_reset():
    """Resets page, lets calculation button be clicked again"""
    st.session_state.clicked = False

def main():

    #LAYOUT / CONFIG
    #set page configuration to wide
    st.set_page_config(layout="wide")

    #shrink the page margins
    margins_css = """
        <style>
            .main > div {
                padding-top: 0rem;
                padding-left: 5rem;
                padding-right: 3rem;
            }
        </style>
    """

    #markdown for button color
    m = st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: rgb(178, 239, 178);
        }
        </style>""", unsafe_allow_html=True)

    st.markdown(margins_css, unsafe_allow_html=True)

    # Set up the page title
    st.title("Solar Potential Map")

    # Initialize Google Maps API client
    API_key = MAPS_API_KEY
    gmaps = gm.Client(key=API_key)

    # Set up default location
    default_location = (35.633942, 139.708126)
    zoom_level = 17.8
    radius = 62
    size_h= 572
    size_v= 594

    #Establish column layout, details in left small column, map in larger right column
    col1, col2, col3 = st.columns([3.5, 1, 7])

    with col1:
        st.write("How much solar power can the rooftops of an area generate?")
        st.write('')
        location = st.text_input("Enter location or address:", 'Le Wagon, Meguro, Tokyo')

    # Geocode location to get latitude and longitude
    geocode_result = gmaps.geocode(location)
    if geocode_result:
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']
        zipcode = geocode_result[0]['address_components'][0]['long_name']
        address = ""
        for component in geocode_result[0]['address_components']:
            address += component['long_name'] + " "
        address = address.strip()

    else:
        st.error("Error: Location not found.")
        st.stop()

    with col1:
        #Left most column
        co2 = ''
        solar_kw = ''
        sqrm = ''
        if st.button("Calculate!", on_click=click_button):
            #this is where the back end call will go
            img = get_gmaps_image(lat=lat, lon=lng, zoom=19)
            img_np = np.asarray(img)

            #calculations
            sqrm = np.rint(rooftop_area_calculator(zoom=zoom_level, lat=lat, mask=img_np)).astype(np.int32)
            #need to add a city grabber to pass through the energy output function, default is tokyo
            solar_kw = np.rint(solar_panel_energy_output(area=sqrm)).astype(np.int32)
            co2 = np.rint(co2_calculator(solar_panel_output = solar_kw)).astype(np.int32)

        st.write('')
        st.write('Totals for chosen area')
        #area for calculation totals
        container = st.container(border=True)
        container.write(f"Square meters: {sqrm}")
        container.write(f"Solar Kilowatts: {solar_kw}")
        container.write(f"Equivalent CO2: {co2}")

    with col2:
        #middle column, just white space to add a more balanced look
        st.write("")

    # Build Html/JS code to visualize the map using Google Maps API:
    map_html = f"""
        <div id="map" style="width: 90%; height:400px;"></div>
        <script>
            var lat = {lat};
            var lng = {lng};
            function initMap() {{
                var geocoder = new google.maps.Geocoder();
                var address = "{location}";
                geocoder.geocode({{ 'address': address }}, function(results, status) {{
                    if (status === 'OK') {{
                        var map = new google.maps.Map(document.getElementById('map'), {{
                            zoom: {zoom_level},
                            mapTypeId: 'satellite',
                            tilt: 0,
                            center: results[0].geometry.location
                        }});
                        // Enable the map type control
                        var mapTypeControlOptions = {{
                            style: google.maps.MapTypeControlStyle.DEFAULT,
                            position: google.maps.ControlPosition.TOP_RIGHT
                        }};
                        map.setOptions({{ mapTypeControl: true, mapTypeControlOptions: mapTypeControlOptions }});


                        // Draw square overlay
                        var center = results[0].geometry.location;
                        var north = center.lat() + ({radius} / 111000);
                        var south = center.lat() - ({radius} / 111000);
                        var east = center.lng() + ({radius} / (111000 * Math.cos(center.lat() * Math.PI / 180)));
                        var west = center.lng() - ({radius} / (111000 * Math.cos(center.lat() * Math.PI / 180)));
                        var squareCoords = [
                            {{ lat: north, lng: west }},
                            {{ lat: north, lng: east }},
                            {{ lat: south, lng: east }},
                            {{ lat: south, lng: west }},
                            {{ lat: north, lng: west }}
                        ];
                        var square = new google.maps.Polygon({{
                            paths: squareCoords,
                            strokeColor: '#FF0000',
                            strokeOpacity: 0.9,
                            strokeWeight: 2,
                            fillColor: '#FF0000',
                            fillOpacity: 0.00
                        }});
                        square.setMap(map);
                    }} else {{
                        alert('Geocode was not successful for the following reason: ' + status);
                    }}
                }});
            }}

        </script>
        <script async defer src="https://maps.googleapis.com/maps/api/js?key={API_key}&callback=initMap"></script>
    """

    # Display the map:
    with col3:
        if not st.session_state.clicked:
            st.components.v1.html(map_html, width=650, height=500)
        else:
            st.text("Original image                          Segmentation mask")
            #replace second image with mask img
            st.image([img,img], width=320)
            if st.button("Reset", on_click=click_reset):
                co2 = ''
                solar_kw = ''
                sqrm = ''
                st.components.v1.html(map_html, width=650, height=500)




if __name__ == "__main__":
    main()
