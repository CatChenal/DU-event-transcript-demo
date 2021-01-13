#cmd:
#streamlit run stapp.py

import streamlit as st

import ipywidgets as ipw
from manage import Controls as CTR


AC = CTR.AppControls()
app = AC.app 

progress_bar = st.progress(0)
status_text = st.empty()

# load app

st.write(CTR.get_app_hdr())
st.write(app)
#left_column, right_column = st.beta_columns(2)
# You can use a column just like st.sidebar:
#left_column.button('Press me!')

# Or even better, call Streamlit functions inside a "with" block:
#with right_column:
#    chosen = st.radio(
#        'Sorting hat',
#        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
#    st.write(f"You are in {chosen} house!")

status_text.text('Done!')
st.balloons()
