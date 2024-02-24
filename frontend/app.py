import streamlit as st
import googlemaps as gm
import requests
from PIL import Image

def watermark_remover(url):
    #Takes the GoogleMaps API Image and returns it without the watermark

    #Get the image
    im = Image.open(requests.get(url,stream=True).raw)

    #Return cropped image
    return im.crop((0,0,572,572))


def call_backend(lat,lng,zoom_level,size_h,size_v,API_key):
    #Calls the backend to get the solar potential

    #Get the image
    # url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lng}&zoom={zoom_level}&size={size_h}x{size_v}&maptype=satellite&key={API_key}"

    #Return the new image
    pass




def confirm_image(url):

    with st.spinner("Loading..."):
        # st.success("Modal loaded successfully!")

        st.write("Please confirm that the area is correct:")
        # Display the image hosted on a URL
        # f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lng}&zoom={zoom_level}&size=500x500&maptype=satellite&key={API_key}"
        # url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lng}&zoom={zoom_level}&size=500x500&maptype=satellite&key={API_key}"
        img = watermark_remover(url)
        st.image(img, caption="Area to be analyzed")
        # st.image(url, caption="Area")

        # Accept and Close buttons
        if st.button("Accept"):
            st.write("You clicked Accept!")


        st.write(" ")
        if st.button("Close"):
            st.write("You clicked Close!")


def main():
    # Set up the page title
    st.title("Solar Potential Map")

    # Retrieve API_Key from .streamlit/secrets.toml:
    #
    # Example:
    # [credentials]
    # API_key = 'FJIkyi3y3...'
    #
    # TO-DO: If it's not set, display error message
    API_key = st.secrets["credentials"]["API_key"]

    # Initialize Google Maps API client
    gmaps = gm.Client(key=API_key)

    # Set up default location (Le Wagon Tokyo, Meguro)
    default_location = ( 35.633942, 139.708126)

    # Get user input for location
    location = st.text_input("Enter location:", 'Le Wagon Tokyo, Meguro')

    # Geocode location to get latitude and longitude
    geocode_result = gmaps.geocode(location)
    if geocode_result:
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']
    else:
        st.error("Error: Location not found.")
        st.stop()

    # Set up zoom level
    # zoom_level = st.slider("Zoom level:", 1, 20, 19)
    zoom_level = 19

    # Get user input for radius
    # radius = st.slider("Radius (meters):", 10, 250, 62)
    radius = 62

    size_h= 572
    size_v= 594


    # Set parameters for the map
    st.write(f"Map of {location}:")
    st.write(f"Latitude: {lat}, Longitude: {lng}")
    st.write(f"Zoom Level: {zoom_level}")

    # Build Html/JS code to visualize the map using Google Maps API:
    map_html = f"""
        <div id="map" style="width: 100%; height: 600px;"></div>
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
                        var marker = new google.maps.Marker({{
                            map: map,
                            draggable: true,  // Make the marker draggable
                            position: results[0].geometry.location
                        }});
                        // Event listener to update marker position when dragging ends
                        google.maps.event.addListener(marker, 'dragend', function(event) {{
                            lat = event.latLng.lat();
                            lng = event.latLng.lng();
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
                            strokeOpacity: 0.8,
                            strokeWeight: 2,
                            fillColor: '#FF0000',
                            fillOpacity: 0.35
                        }});
                        square.setMap(map);
                    }} else {{
                        alert('Geocode was not successful for the following reason: ' + status);
                    }}
                }});
            }}
            function updateLocation() {{
                var newUrl = window.location.href.split("?")[0] + "?location=" + lat + "," + lng;
                window.history.pushState('{{}}', '{{}}', newUrl);
                // Send message to parent with new location
                var newLocation = {{ lat: lat, lng: lng }};
                window.parent.postMessage({{ location: JSON.stringify(newLocation) }}, '*');
            }}


            setInterval(updateLocation, 10);
        </script>
        <script async defer src="https://maps.googleapis.com/maps/api/js?key={API_key}&callback=initMap"></script>
    """

    # Display the map:
    st.components.v1.html(map_html, width=800, height=600)


    # Temp: Button to open the link in a new tab
    url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lng}&zoom={zoom_level}&size={size_h}x{size_v}&maptype=satellite&key={API_key}"
    # st.link_button("Open Static Map", url)

    if st.button("Calculate Solar Potential"):
        confirm_image(url)







if __name__ == "__main__":
    main()
