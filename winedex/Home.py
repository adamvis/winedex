
import base64
import os
import time
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Winedex - Home", page_icon=":wine_glass:", layout='wide'
)
st.markdown(f"""
    <style>
        .reportview-container .main .block-container{{
            padding-top: {0}rem;
        }}
    </style>""",
    unsafe_allow_html=True,
)

def main():
    
    # st.markdown("<h1 style='text-align: center;'>WINEDEX</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center;'><img src='data:image/png;base64," + 
        base64.b64encode(open(os.path.join("setup", "sign.png"), 'rb').read()).decode() + 
        "' alt='Sign Image'></p>",
        unsafe_allow_html=True
    )
    
    col1, col2 = st.columns([1,1])
    with col1:
        st.image(os.path.join("setup", "home_img.png"))
        
    with col2:
        st.subheader("Gotta catch'em all!")
        word_stream = """
        This is WineDex, i'm your virtual study book designed to help you navigate through the discovery of the wine world!
        """
        st.write_stream(stream_text(word_stream))
        time.sleep(0.1)
        word_stream = """
        Start exploring terroirs, grapes varieties and rate new wines!
        """
        st.write_stream(stream_text(word_stream))
    
    st.markdown("---")
    st.markdown(
        '<h6>Made in &nbsp<img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="16">&nbsp by <a href="https://linkedin.com/adamviscusi">@adamvis</a></h6>',
        unsafe_allow_html=True,
    )

def stream_text(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.2)


if __name__ == "__main__":
    main()