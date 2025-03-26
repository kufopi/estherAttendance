import streamlit as st
import face_record

# Page configuration
st.set_page_config(page_title='Attendance System', layout='wide')

# Center the logo
col1, col2, col3 = st.columns(3)
with col2:
    st.image('logo.jpg')

def main():
    st.title("☁️ **Cloud-based Facial Recognition Attendance System** 🚀")
    st.markdown("---")  # Adds a horizontal separator
    st.subheader(f"👤 Author: Akinjisola Esther Omobolanle")
    st.subheader(f"🆔 Matric No: CSC/2022/033")

    # Face recognition module
    with st.spinner("Loading Face Recognition"):
        import face_record
        st.success("Module Loaded")

if __name__ == '__main__':
    main()
