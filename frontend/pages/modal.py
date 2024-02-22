import streamlit as st


def main():
    st.title("Streamlit Modal Example")
    st.write("Click the button below to open the modal.")

    # Button to open the modal
    if st.button("Open Modal"):
        # Call function to show the modal
        show_modal()

def show_modal():
    # Display the modal
    with st.spinner("Loading..."):
        # Display a loading spinner while the modal content loads
        # You can replace this with your actual modal content
        st.success("Modal loaded successfully!")

        # Display the modal content
        st.write("Example Modal Content")

        # Accept and Close buttons
        if st.button("Accept"):
            # st.write("You clicked Accept!")
            st.success("You clicked Accept!")

        st.write("11111111")
        if st.button("Close"):
            st.write("You clicked Close!")

        st.write("2222222")
    st.write("333333333333")

if __name__ == "__main__":
    main()
