# import streamlit as st
# import pandas as pd
# import json
# import os

# # =========================================================
# # PAGE CONFIG
# # =========================================================
# st.set_page_config(
#     page_title="Campaign Details",
#     layout="wide"
# )

# # =========================================================
# # LOGIN CREDENTIALS
# # =========================================================
# ADMIN_USERNAME = "admin"
# ADMIN_PASSWORD = "admin123"

# USER_USERNAME = "user"
# USER_PASSWORD = "user123"

# # =========================================================
# # CAMPAIGN CONFIG FILE
# # =========================================================
# CONFIG_FILE = "campaign_config.json"

# # =========================================================
# # DEFAULT CAMPAIGN SETTINGS
# # =========================================================
# default_config = {
#     "GRS DEFENCE": True,
#     "GRS REVERSE": True,
#     "SMS REV-UNDER-6K+": True,
#     "SMS REV OVER-10K+": True,
#     "GRS Tax 10k": True
# }

# # =========================================================
# # CREATE CONFIG FILE IF NOT EXISTS
# # =========================================================
# if not os.path.exists(CONFIG_FILE):
#     with open(CONFIG_FILE, "w") as f:
#         json.dump(default_config, f)

# # =========================================================
# # LOAD CONFIG
# # =========================================================
# with open(CONFIG_FILE, "r") as f:
#     campaign_status = json.load(f)

# # =========================================================
# # SESSION STATE
# # =========================================================
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False

# if "role" not in st.session_state:
#     st.session_state.role = ""

# # =========================================================
# # LOGIN FUNCTION
# # =========================================================
# def login():

#     st.title("🔐 Login")

#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")

#     if st.button("Login"):

#         # ADMIN LOGIN
#         if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
#             st.session_state.logged_in = True
#             st.session_state.role = "admin"
#             st.rerun()

#         # USER LOGIN
#         elif username == USER_USERNAME and password == USER_PASSWORD:
#             st.session_state.logged_in = True
#             st.session_state.role = "user"
#             st.rerun()

#         else:
#             st.error("Invalid Username or Password")

# # =========================================================
# # LOGOUT
# # =========================================================
# def logout():
#     st.session_state.logged_in = False
#     st.session_state.role = ""
#     st.rerun()

# # =========================================================
# # CSV LOADER
# # =========================================================
# @st.cache_data(ttl=2)
# def load_data(csv_file):

#     if not os.path.exists(csv_file):
#         return pd.DataFrame()

#     df = pd.read_csv(csv_file, dtype=str)

#     df.columns = df.columns.str.strip()

#     df = df.fillna("")

#     return df

# # =========================================================
# # SEARCH FUNCTION
# # =========================================================
# def search_section(csv_file):

#     df = load_data(csv_file)

#     if df.empty:
#         st.error("CSV File Not Found")
#         return

#     search_zip = st.text_input(
#         "Enter ZIP Code",
#         placeholder="Search ZIP code..."
#     )

#     if search_zip:

#         if "ZipCode" not in df.columns:
#             st.error("CSV must contain 'ZipCode' column")

#         else:

#             result = df[
#                 df["ZipCode"]
#                 .astype(str)
#                 .str.contains(search_zip, case=False, na=False)
#             ]

#             st.success(f"Results Found: {len(result)}")

#             if not result.empty:
#                 st.dataframe(
#                     result,
#                     use_container_width=True,
#                     hide_index=True
#                 )
#             else:
#                 st.warning("No matching ZIP found.")

#     st.write(f"Total Records: {len(df)}")

# # =========================================================
# # ADMIN PANEL
# # =========================================================
# def admin_panel():

#     st.sidebar.markdown("## 🛠 Admin Panel")

#     st.sidebar.write("Toggle Campaign Visibility")

#     changed = False

#     for campaign in campaign_status:

#         new_value = st.sidebar.toggle(
#             campaign,
#             value=campaign_status[campaign]
#         )

#         if new_value != campaign_status[campaign]:
#             campaign_status[campaign] = new_value
#             changed = True

#     if changed:
#         with open(CONFIG_FILE, "w") as f:
#             json.dump(campaign_status, f)

# # =========================================================
# # LOGIN CHECK
# # =========================================================
# if not st.session_state.logged_in:
#     login()
#     st.stop()

# # =========================================================
# # TOP BAR
# # =========================================================
# col1, col2 = st.columns([8, 1])

# with col1:
#     st.title("📞 Campaign Details")

# with col2:
#     if st.button("Logout"):
#         logout()

# # =========================================================
# # ADMIN SETTINGS
# # =========================================================
# if st.session_state.role == "admin":
#     admin_panel()

# # =========================================================
# # VISIBLE CAMPAIGNS
# # =========================================================
# visible_campaigns = [
#     c for c, enabled in campaign_status.items() if enabled
# ]

# # =========================================================
# # NO CAMPAIGNS
# # =========================================================
# if not visible_campaigns:
#     st.warning("No Campaigns Available")
#     st.stop()

# # =========================================================
# # SIDEBAR MENU
# # =========================================================
# page = st.sidebar.selectbox(
#     "Select Campaign",
#     visible_campaigns
# )

# # =========================================================
# # GRS DEFENCE
# # =========================================================
# if page == "GRS DEFENCE":

#     st.header("GRS DEFENCE")

#     if st.session_state.role == "admin":

#         phone = st.text_input("Phone", "8775060274")

#         hours = st.text_input(
#             "Hours",
#             "8am -8pm EST Monday-Friday"
#         )

#         bad_states = st.text_area(
#             "Bad States",
#             "AK,AR,CA,DE,HI,ID,IA,KS,LA,ME,MD,MN,MT,NE,NV,NC,ND,OR,RI,SD,SC,TN,UT,VT,WV,WY"
#         )

#     else:

#         st.markdown("### Phone : 8775060274")
#         st.markdown("### Hours : 8am -8pm EST Monday-Friday")
#         st.markdown("### Bad States")
#         st.write(
#             "AK,AR,CA,DE,HI,ID,IA,KS,LA,ME,MD,MN,MT,NE,NV,NC,ND,OR,RI,SD,SC,TN,UT,VT,WV,WY"
#         )

#     search_section("GRS DEFENCE SHEET.csv")

# # =========================================================
# # GRS REVERSE
# # =========================================================
# elif page == "GRS REVERSE":

#     st.header("GRS REVERSE")

#     st.markdown("### Phone : 4848044448")
#     st.markdown("### Hours : Mon-Fri 6am-5pm PST")
#     st.markdown("### Bad States")
#     st.write("AK, GA, HI, MA, ME, NY, RI, VT, VA, MO, DC")

# # =========================================================
# # SMS REV OVER 10K
# # =========================================================
# elif page == "SMS REV OVER-10K+":

#     st.header("SMS REV OVER-10K+")

#     st.markdown("### Phone : 2544427086")
#     st.markdown("### Campaign Hours : 9am to 7.30pm EST")
#     st.markdown("### Affordability : 250$-300$")
#     st.markdown("### Bad States : OR")

# # =========================================================
# # SMS REV UNDER 6K
# # =========================================================
# elif page == "SMS REV-UNDER-6K+":

#     st.header("SMS REV-UNDER-6K+")

#     st.markdown("### Phone : 2543293489")
#     st.markdown("### Campaign Hours : 9am to 7.30pm EST")
#     st.markdown("### Affordability : 220$")
#     st.markdown("### Nationwide")

# # =========================================================
# # GRS TAX
# # =========================================================
# elif page == "GRS Tax 10k":

#     st.header("GRS Tax 10k")

#     st.markdown("### Phone : 8776840537")
#     st.markdown("### Call Buffer : 120 Seconds")

#     search_section("GRS TAX 10k.csv")



import streamlit as st
import pandas as pd
import json
import os

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Campaign Details",
    layout="wide"
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
default_config = {
    "GRS DEFENCE": True,
    "GRS REVERSE": True,
    "SMS REV-UNDER-6K+": True,
    "SMS REV OVER-10K+": True,
    "GRS Tax 10k": True
}

# =========================================================
# DEFAULT CAMPAIGN DETAILS
# =========================================================
default_details = {

    "GRS DEFENCE": {
        "phone": "8775060274",
        "hours": "8am - 8pm EST Monday-Friday",
        "bad_states": "AK,AR,CA,DE,HI,ID,IA,KS,LA,ME,MD,MN,MT,NE,NV,NC,ND,OR,RI,SD,SC,TN,UT,VT,WV,WY",
        "notes": "Defence campaign details",
        "csv": "GRS DEFENCE SHEET.csv"
    },

    "GRS REVERSE": {
        "phone": "4848044448",
        "hours": "Mon-Fri 6am-5pm PST",
        "bad_states": "AK, GA, HI, MA, ME, NY, RI, VT, VA, MO, DC",
        "notes": "Age 62+ | Home Value 120K+",
        "csv": ""
    },

    "SMS REV-UNDER-6K+": {
        "phone": "2543293489",
        "hours": "9am to 7.30pm EST",
        "bad_states": "None",
        "notes": "Affordability - 220$",
        "csv": ""
    },

    "SMS REV OVER-10K+": {
        "phone": "2544427086",
        "hours": "9am to 7.30pm EST",
        "bad_states": "OR",
        "notes": "Affordability - 250$-300$",
        "csv": ""
    },

    "GRS Tax 10k": {
        "phone": "8776840537",
        "hours": "Open",
        "bad_states": "None",
        "notes": "Call Buffer - 120 Seconds",
        "csv": "GRS TAX 10k.csv"
    }
}

# =========================================================
# CREATE FILES IF NOT EXISTS
# =========================================================
if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "w") as f:
        json.dump(default_config, f, indent=4)

if not os.path.exists(DETAILS_FILE):
    with open(DETAILS_FILE, "w") as f:
        json.dump(default_details, f, indent=4)

# =========================================================
# LOAD DATA
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
# LOGIN
# =========================================================
def login():

    st.title("🔐 Campaign Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.logged_in = True
            st.session_state.role = "admin"
            st.rerun()

        elif username == USER_USERNAME and password == USER_PASSWORD:
            st.session_state.logged_in = True
            st.session_state.role = "user"
            st.rerun()

        else:
            st.error("Invalid Username or Password")

# =========================================================
# LOGOUT
# =========================================================
def logout():
    st.session_state.logged_in = False
    st.session_state.role = ""
    st.rerun()

# =========================================================
# CSV LOADER
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

    st.subheader("🔍 ZIP Code Search")

    search_zip = st.text_input(
        "Enter ZIP Code",
        placeholder="Search ZIP code..."
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

    selected_campaign = st.sidebar.selectbox(
        "Edit Campaign",
        list(campaign_details.keys())
    )

    st.sidebar.subheader("Campaign Visibility")

    # Toggle ON/OFF
    campaign_status[selected_campaign] = st.sidebar.toggle(
        "Campaign Active",
        value=campaign_status[selected_campaign]
    )

    st.sidebar.subheader("Edit Campaign Details")

    phone = st.sidebar.text_input(
        "Phone",
        value=campaign_details[selected_campaign]["phone"]
    )

    hours = st.sidebar.text_input(
        "Hours",
        value=campaign_details[selected_campaign]["hours"]
    )

    bad_states = st.sidebar.text_area(
        "Bad States",
        value=campaign_details[selected_campaign]["bad_states"]
    )

    notes = st.sidebar.text_area(
        "Notes",
        value=campaign_details[selected_campaign]["notes"]
    )

    csv_name = st.sidebar.text_input(
        "CSV File Name",
        value=campaign_details[selected_campaign]["csv"]
    )

    # SAVE BUTTON
    if st.sidebar.button("💾 Save Changes"):

        campaign_details[selected_campaign]["phone"] = phone
        campaign_details[selected_campaign]["hours"] = hours
        campaign_details[selected_campaign]["bad_states"] = bad_states
        campaign_details[selected_campaign]["notes"] = notes
        campaign_details[selected_campaign]["csv"] = csv_name

        # Save details
        with open(DETAILS_FILE, "w") as f:
            json.dump(campaign_details, f, indent=4)

        # Save status
        with open(CONFIG_FILE, "w") as f:
            json.dump(campaign_status, f, indent=4)

        st.sidebar.success("Changes Saved Successfully")

    # =========================================================
# ADD NEW CAMPAIGN SECTION
# ADD THIS INSIDE ADMIN PANEL
# =========================================================

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

# =========================================================
# ADD CAMPAIGN BUTTON
# =========================================================
if st.sidebar.button("➕ Create Campaign"):

    if new_campaign_name.strip() == "":

        st.sidebar.error("Campaign Name Required")

    elif new_campaign_name in campaign_details:

        st.sidebar.error("Campaign Already Exists")

    else:

        # ADD DETAILS
        campaign_details[new_campaign_name] = {

            "phone": new_phone,
            "hours": new_hours,
            "bad_states": new_bad_states,
            "notes": new_notes,
            "csv": new_csv
        }

        # ENABLE CAMPAIGN
        campaign_status[new_campaign_name] = True

        # SAVE DETAILS
        with open(DETAILS_FILE, "w") as f:
            json.dump(campaign_details, f, indent=4)

        # SAVE STATUS
        with open(CONFIG_FILE, "w") as f:
            json.dump(campaign_status, f, indent=4)

        st.sidebar.success("New Campaign Added Successfully")

        st.rerun()

# =========================================================
# SHOW ACTIVE CAMPAIGNS
# =========================================================
visible_campaigns = [
    c for c in campaign_status if campaign_status[c]
]

if not visible_campaigns:
    st.warning("No Active Campaigns")
    st.stop()

# =========================================================
# CAMPAIGN MENU
# =========================================================
page = st.sidebar.selectbox(
    "Select Campaign",
    visible_campaigns
)

# =========================================================
# SHOW CAMPAIGN DETAILS
# =========================================================
details = campaign_details[page]

st.header(page)

st.markdown(f"### 📞 Phone : {details['phone']}")

st.markdown(f"### ⏰ Hours : {details['hours']}")

st.markdown(f"### 🚫 Bad States")

st.write(details["bad_states"])

st.markdown(f"### 📝 Notes")

st.write(details["notes"])

# =========================================================
# ZIP SEARCH
# =========================================================
search_section(details["csv"])