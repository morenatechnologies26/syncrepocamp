import streamlit as st
import pandas as pd
import json
import os
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
import pytz
from appclock import show_clocks

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Campaign Details",
    layout="wide",
    # page_icon="logo.png"
    page_icon="logo.png"

)

# =========================================================
# AUTO REFRESH EVERY 10 SECONDS
# =========================================================
st_autorefresh(
    interval=10 * 1000,
    key="datarefresh"
)

# =========================================================
# LOGIN CREDENTIALS
# =========================================================
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

USER_USERNAME = "user"
USER_PASSWORD = "user123"

# =========================================================
# FILES
# =========================================================
CONFIG_FILE = "campaign_config.json"
DETAILS_FILE = "campaign_details.json"

# =========================================================
# DEFAULT CAMPAIGN STATUS
# =========================================================
# default_config = {
#     "GRS DEFENCE": True,
#     "GRS REVERSE": True,
#     # "SMS REV-UNDER-6K+": True,
#     "SMS REV OVER-10K+": True,
#     # "GRS Tax 10k": True
# }

# =========================================================
# DEFAULT CAMPAIGN DETAILS
# =========================================================
# default_details = {

#     "GRS DEFENCE": {
#         "phone": "8775060274",
#         "hours": "8am - 8pm EST Monday-Friday",
#         "bad_states": "AK,AR,CA,DE,HI,ID,IA,KS,LA,ME,MD,MN,MT,NE,NV,NC,ND,OR,RI,SD,SC,TN,UT,VT,WV,WY",
#         "notes": "Defence Campaign",
#         "link":"",
#         "csv": "GRS DEFENCE SHEET.csv"
#     },

#     "GRS REVERSE": {
#         "phone": "4848044448",
#         "hours": "Mon-Fri 6am-5pm PST",
#         "bad_states": "AK, GA, HI, MA, ME, NY, RI, VT, VA, MO, DC",
#         "notes": "Age 62+ | Home Value 120K+",
#         "link":"",
#         "csv": ""
#     },

#     "SMS REV-UNDER-6K+": {
#         "phone": "2543293489",
#         "hours": "9am to 7.30pm EST",
#         "bad_states": "None",
#         "notes": "Affordability - 220$",
#         "link":"",
#         "csv": ""
#     },

#     "SMS REV OVER-10K+": {
#         "phone": "2544427086",
#         "hours": "9am to 7.30pm EST",
#         "bad_states": "OR",
#         "notes": "Affordability - 250$ - 300$ Dollars",
#         "link":"",
#         "csv": ""
#     },

#     "GRS Tax 10k": {
#         "phone": "8776840537",
#         "hours": "Open",
#         "bad_states": "None",
#         "notes": "Call Buffer - 120 Seconds",
#         "link":"",
#         "csv": "GRS TAX 10k.csv"
#     }
# }

# =========================================================
# CREATE FILES IF NOT EXISTS
# =========================================================
# if not os.path.exists(CONFIG_FILE):
#     with open(CONFIG_FILE, "w") as f:
#         json.dump(default_config, f, indent=4)

# if not os.path.exists(DETAILS_FILE):
#     with open(DETAILS_FILE, "w") as f:
#         json.dump(default_details, f, indent=4)

# =========================================================
# LOAD JSON FILES
# =========================================================
with open(CONFIG_FILE, "r") as f:
    campaign_status = json.load(f)

with open(DETAILS_FILE, "r") as f:
    campaign_details = json.load(f)

# =========================================================
# SESSION
# =========================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = ""

# =========================================================
# LOGIN FUNCTION
# =========================================================
def login():

    st.title("🔐 Campaign Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        # ADMIN LOGIN
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:

            st.session_state.logged_in = True
            st.session_state.role = "admin"

            st.rerun()

        # USER LOGIN
        elif username == USER_USERNAME and password == USER_PASSWORD:

            st.session_state.logged_in = True
            st.session_state.role = "user"

            st.rerun()

        else:
            st.error("Invalid Username or Password")

# =========================================================
# LOGOUT FUNCTION
# =========================================================
def logout():

    st.session_state.logged_in = False
    st.session_state.role = ""

    st.rerun()

# =========================================================
# LOAD CSV
# =========================================================
@st.cache_data(ttl=2)
def load_data(csv_file):

    if csv_file == "":
        return pd.DataFrame()

    if not os.path.exists(csv_file):
        return pd.DataFrame()

    df = pd.read_csv(csv_file, dtype=str)

    df.columns = df.columns.str.strip()

    df = df.fillna("")

    return df

# =========================================================
# ZIP SEARCH
# =========================================================
def search_section(csv_file):

    if csv_file == "":
        return

    df = load_data(csv_file)

    if df.empty:
        st.warning("CSV File Not Found")
        return

    st.divider()

    st.subheader("🔍 ZIP Search")

    search_zip = st.text_input(
        "Enter ZIP Code",
        placeholder="Search ZIP Code"
    )

    if search_zip:

        if "ZipCode" not in df.columns:

            st.error("CSV must contain ZipCode column")

        else:

            result = df[
                df["ZipCode"]
                .astype(str)
                .str.contains(search_zip, case=False, na=False)
            ]

            st.success(f"Results Found: {len(result)}")

            if not result.empty:

                st.dataframe(
                    result,
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.warning("No ZIP Found")

    st.write(f"Total Records: {len(df)}")



# =========================================================
# LOGIN CHECK
# =========================================================
if not st.session_state.logged_in:
    login()
    st.stop()

# =========================================================
# HEADER
# =========================================================
col1, col2 = st.columns([8, 1])

with col1:
    st.title("📞 Campaign Details")

with col2:
    if st.button("Logout"):
        logout()

# =========================================================
# ADMIN PANEL
# =========================================================
if st.session_state.role == "admin":

    st.sidebar.title("🛠 Admin Panel")

    # ==========================================
    # SELECT CAMPAIGN
    # ==========================================
    selected_campaign = st.sidebar.selectbox(
        "Select Campaign To Edit",
        list(campaign_details.keys())
    )

    details = campaign_details[selected_campaign]

    # ==========================================
    # TOGGLE
    # ==========================================
    # campaign_active = st.sidebar.toggle(
    #     "Campaign Active",
    #     value=campaign_status.get(selected_campaign, True)
    # )

    toggle_key = f"toggle_{selected_campaign}"

    if toggle_key not in st.session_state:
        st.session_state[toggle_key] = campaign_status.get(
            selected_campaign,
            True
        )

    campaign_active = st.sidebar.toggle(
        "Campaign Active",
        key=toggle_key
    )


    # ==========================================
    # EDITABLE FIELDS
    # ==========================================
    # phone = st.sidebar.text_input(
    #     "Phone",
    #     value=details["phone"]
    # )

    # hours = st.sidebar.text_input(
    #     "Hours",
    #     value=details["hours"]
    # )

    # bad_states = st.sidebar.text_area(
    #     "Bad States",
    #     value=details["bad_states"]
    # )

    # good_states = st.sidebar.text_area(
    #     "Good_states",
    #     value=details["bad_states"])

    # notes = st.sidebar.text_area(
    #     "Notes",
    #     value=details["notes"]
    # )

    # csv_name = st.sidebar.text_input(
    #     "CSV File Name",
    #     value=details["csv"]
    # )

    # link = st.sidebar.text_input(
    #     "Link",
    #     value=details["link"]
    # )


    # ==========================================
    # UNIQUE KEYS
    # ==========================================
    phone_key = f"phone_{selected_campaign}"
    hours_key = f"hours_{selected_campaign}"
    bad_states_key = f"bad_states_{selected_campaign}"
    notes_key = f"notes_{selected_campaign}"
    csv_key = f"csv_{selected_campaign}"
    good_states_key = f"good_state_{selected_campaign}"
    link_key = f"link_{selected_campaign}"

    # ==========================================
    # PRESERVE EXISTING VALUES
    # ==========================================
    if phone_key not in st.session_state:
        st.session_state[phone_key] = details["phone"]

    if hours_key not in st.session_state:
        st.session_state[hours_key] = details["hours"]

    if bad_states_key not in st.session_state:
        st.session_state[bad_states_key] = details["bad_states"]

    if notes_key not in st.session_state:
        st.session_state[notes_key] = details["notes"]

    if csv_key not in st.session_state:
        st.session_state[csv_key] = details["csv"]

    if good_states_key not in st.session_state:
        st.session_state[good_states_key] = details["good_states"]

    if link_key not in st.session_state:
        st.session_state[link_key] = details["link"]

    # ==========================================
    # EDITABLE FIELDS
    # ==========================================
    phone = st.sidebar.text_input(
        "Phone",
        key=phone_key
    )

    hours = st.sidebar.text_input(
        "Hours",
        key=hours_key
    )

    bad_states = st.sidebar.text_area(
        "Bad States",
        key=bad_states_key
    )

    notes = st.sidebar.text_area(
        "Notes",
        key=notes_key
    )

    csv_name = st.sidebar.text_input(
        "CSV File Name",
        key=csv_key
    )

    csv_name = st.sidebar.text_input(
        "good_state",
        key=good_states_key
    )
        
    csv_name = st.sidebar.text_input(
        "link",
        key=link_key
    )


    # ==========================================
    # SAVE BUTTON
    # ==========================================
    if st.sidebar.button("💾 Save Campaign"):

        # campaign_details[selected_campaign] = {

        #     "phone": phone,
        #     "hours": hours,
        #     "bad_states": bad_states,
        #     "good_states": good_states,
        #     "notes": notes,
        #     "csv": csv_name,
        #     "link": link
        # }

        campaign_details[selected_campaign] = {

            "phone": st.session_state[phone_key],
            "hours": st.session_state[hours_key],
            "bad_states": st.session_state[bad_states_key],
            "good_states": st.session_state[good_states_key],
            "notes": st.session_state[notes_key],
            "csv": st.session_state[csv_key],
            "link": st.session_state[link_key]
        }

        # campaign_status[selected_campaign] = campaign_active
        campaign_status[selected_campaign] = st.session_state[toggle_key]

        # SAVE DETAILS
        with open(DETAILS_FILE, "w") as f:
            json.dump(campaign_details, f, indent=4)

        # SAVE STATUS
        with open(CONFIG_FILE, "w") as f:
            json.dump(campaign_status, f, indent=4)

        st.sidebar.success("Campaign Saved Successfully")

        st.rerun()

    # ==========================================
    # ADD NEW CAMPAIGN
    # ==========================================
    st.sidebar.divider()

    st.sidebar.subheader("➕ Add New Campaign")

    new_campaign_name = st.sidebar.text_input(
        "Campaign Name"
    )

    new_phone = st.sidebar.text_input(
        "New Campaign Phone"
    )

    new_hours = st.sidebar.text_input(
        "New Campaign Hours"
    )

    new_bad_states = st.sidebar.text_area(
        "New Campaign Bad States"
    )

    new_notes = st.sidebar.text_area(
        "New Campaign Notes"
    )

    new_csv = st.sidebar.text_input(
        "New Campaign CSV File"
    )

    new_link = st.sidebar.text_input(
        "new link")
    
    new_good_states= st.sidebar.text_input(
        "new good states"
    )

    if st.sidebar.button("➕ Create Campaign"):

        if new_campaign_name.strip() == "":

            st.sidebar.error("Campaign Name Required")

        elif new_campaign_name in campaign_details:

            st.sidebar.error("Campaign Already Exists")

        else:

            campaign_details[new_campaign_name] = {

                "phone": new_phone,
                "hours": new_hours,
                "bad_states": new_bad_states,
                "good_states":new_good_states,
                "notes": new_notes,
                "csv": new_csv,
                "link":new_link
            }

            campaign_status[new_campaign_name] = True

            # SAVE DETAILS
            with open(DETAILS_FILE, "w") as f:
                json.dump(campaign_details, f, indent=4)

            # SAVE STATUS
            with open(CONFIG_FILE, "w") as f:
                json.dump(campaign_status, f, indent=4)

            st.sidebar.success("New Campaign Added")

            st.rerun()

# =========================================================
# SHOW ACTIVE CAMPAIGNS
# =========================================================
visible_campaigns = [

    campaign

    for campaign in campaign_status

    if campaign_status[campaign]
]

if not visible_campaigns:

    st.warning("No Active Campaigns")

    st.stop()

# =========================================================
# LIVE CLOCKS
# =========================================================
show_clocks()


# st.markdown("""
# <style>

# /* Reduce gap below clocks */
# h2 {
#     margin-top: -120px !important;
#     padding-top: 0px !important;
# }

# /* Optional: reduce overall block spacing */
# div.block-container {
#     padding-top: 1rem;
# }

# /* Sidebar font */
# #root > div:nth-child(1) > div.withScreencast > div > div > section > div.st-emotion-cache-1ybqi87.e9ic3ti2 > div.st-emotion-cache-1r1cntt.e9ic3ti1 > div > div > div > div > label > span > div > p{
#     font-size: 25px !important;
#     font-weight: bold;
# }

# </style>
# """, unsafe_allow_html=True)


# # =========================================================
# # REDUCE GAP / SHIFT CONTENT UP
# # =========================================================
# st.markdown("""
# <style>

# /* Move all content below clocks upward */
# h2 {
#     margin-top: -120px !important;
# }

# /* Remove extra spacing from markdown blocks */
# div[data-testid="stMarkdownContainer"] {
#     margin-top: 0px !important;
#     padding-top: 0px !important;
# }

# /* Reduce Streamlit default vertical spacing */
# .block-container {
#     padding-top: 1rem !important;
# }

# /* Sidebar heading font size */
# #root > div:nth-child(1) > div.withScreencast > div > div > section > div.st-emotion-cache-1ybqi87.e9ic3ti2 > div.st-emotion-cache-1r1cntt.e9ic3ti1 > div > div > div > div > label > span > div > p{
#     font-size: 25px !important;
#     font-weight: bold;
# }

# </style>
# """, unsafe_allow_html=True)


# st.markdown("""
# <style>
# #root > div:nth-child(1) > div.withScreencast > div > div > section > div.st-emotion-cache-1ybqi87.e9ic3ti2 > div.st-emotion-cache-1r1cntt.e9ic3ti1 > div > div > div > div > label > span > div > p{
#     font-size: 25px !important;
#     font-weight: bold;
# }
# </style>
# """, unsafe_allow_html=True)

st.markdown("""
<style>
#root > div:nth-child(1) > div.withScreencast > div > div > section > div.st-emotion-cache-1ybqi87.eelgd2m2 > div.st-emotion-cache-1r1cntt.eelgd2m1 > div > div > div > div > label > span > div > p{
    font-size: 25px !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
#root > div:nth-child(1) > div.withScreencast > div > div > div > header > div{
    visiblity : hidden !important;
}
</style>
""", unsafe_allow_html=True)


# hide_streamlit_style = """
# <style>
# header[data-testid="stHeader"] {
#     display: none;
# }

# #MainMenu {
#     visibility: hidden;
# }

# footer {
#     visibility: hidden;
# }
# </style>
# """

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# =========================================================
# USER SIDEBAR RADIO BUTTON
# =========================================================
page = st.sidebar.radio(
    "📋 Active Campaigns",
    visible_campaigns
)


# =========================================================
# SHOW CAMPAIGN
# =========================================================
details = campaign_details[page]

# =========================================================
# USER VIEW
# =========================================================
st.header(page)

st.markdown(f"### 📞 Phone : {details['phone']}")

st.markdown(f"### ⏰ Hours : {details['hours']}")

st.markdown("### 🚫 Bad States")

st.write(details["bad_states"])

st.markdown("### ✔️Good States")
st.write(details["good_states"])

st.markdown("### 📝 Notes")

st.write(details["notes"])

st.markdown(f"### 🔗Link : {details['link']}")

# =========================================================
# ZIP SEARCH
# =========================================================
search_section(details["csv"])