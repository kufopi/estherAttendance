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
with open('auth_configure.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Initialize authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)


def main():
    # Login with fields parameter
    try:
        name, authentication_status, username = authenticator.login(fields={
            'Form name': 'Login',
            'Username': 'Username',
            'Password': 'Password',
            'Login': 'Login'
        })

        if authentication_status:
            st.title("☁️ **Cloud-based Facial Recognition Attendance System** 🚀")
            st.markdown("---")  # Adds a horizontal separator
            st.subheader(f"👤 Author: Akinjisola Esther Omobolanle")
            st.subheader(f"🆔 Matric No: CSC/2022/033")
            st.write(f'Welcome {name}!')

            # Logout button
            if st.sidebar.button('Logout'):
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
        st.error(f"An error occurred: {e}")


if __name__ == '__main__':
    main()