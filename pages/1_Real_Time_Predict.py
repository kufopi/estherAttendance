from face_record import RealTimer
from home import st
import face_record
from streamlit_webrtc import webrtc_streamer
import av
import time

st.subheader("Real Time Prediction")

with st.spinner('Retrieving Data from Redis DB'):
    redis_face_db = face_record.retrieve_data()
    st.dataframe(redis_face_db)
st.success('Successful Retrieval')

waitTime = 20  # Time in seconds
setTime = time.time()
realtimePred = face_record.RealTimer()
course = st.selectbox("Select Course", options=("CSC401", "CSC412", "CSC403","CSC433"))

def video_frame_callback(frame):
    global setTime
    img = frame.to_ndarray(format="bgr24")

    predd_img = realtimePred.face_prediction(img, redis_face_db, 'Facial Features', ['Name', 'Role'],course=course, thresh=0.5)
    timenow = time.time()
    difftime = timenow - setTime

    if difftime >= waitTime:
        realtimePred.save_log_redis()
        setTime = time.time()
        print('Saved Data to Redis')

    return av.VideoFrame.from_ndarray(predd_img, format="bgr24")

webrtc_streamer(key="realtimePrediction", video_frame_callback=video_frame_callback,
                rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    })
