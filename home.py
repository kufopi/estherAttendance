import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Page configuration
st.set_page_config(page_title='Attendance System', layout='wide')
col1, col2, col3 = st.columns(3)
with col2:
    st.image('logo.jpg')

# Load configuration
try:
    with open('auth_configure.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
except Exception as e:
    st.error(f"Error loading configuration file: {e}")
    st.stop()

# Initialize authenticator
try:
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )
except Exception as e:
    st.error(f"Error initializing authenticator: {e}")
    st.stop()

def main():
    # Login with fields parameter
    try:
        # Print debug information about the authentication configuration
        st.write("Debug: Authentication Configuration")
        st.write(config['credentials'])

        # Modify login call to handle potential None return
        login_result = authenticator.login(fields={
            'Form name': 'Login',
            'Username': 'Username',
            'Password': 'Password',
            'Login': 'Login'
        })

        # Check if login_result is None or has unexpected structure
        if login_result is None:
            st.error("Authentication failed: No response from login method")
            return

        # Unpack with a safety check
        try:
            name, authentication_status, username = login_result
        except (ValueError, TypeError) as e:
            st.error(f"Error unpacking login result: {e}")
            st.write(f"Received login result: {login_result}")
            return

        if authentication_status:
            st.title("☁️ **Cloud-based Facial Recognition Attendance System** 🚀")
            st.markdown("---")  # Adds a horizontal separator
            st.subheader(f"👤 Author: Akinjisola Esther Omobolanle")
            st.subheader(f"🆔 Matric No: CSC/2022/033")
            st.write(f'Welcome {name}!')

            # Logout button with a unique key
            if st.sidebar.button('Logout', key='logout_button'):
                authenticator.logout('Logout', 'main')
                st.session_state.clear()
                st.rerun()

            # Face recognition module
            with st.spinner("Loading Face Recognition"):
                import face_record
                st.success("Module Loaded")

        elif authentication_status == False:
            st.error('Username/password incorrect')

        elif authentication_status == None:
            st.warning('Enter username and password')

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        # Print the full traceback for more detailed debugging
        import traceback
        st.error(traceback.format_exc())

if __name__ == '__main__':
    main()
