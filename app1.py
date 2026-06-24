import streamlit as st
import pandas as pd

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title=" Campaign Details",
    layout="wide"
)

st.title(" Campaign Details ")

page = st.sidebar.selectbox(
    "Select Campaign",
    ["GRS DEFENCE","GRS REVERSE","SMS REV-UNDER-6K+","SMS REV OVER-10K+","GRS Tax 10k"]
)

if page == "GRS DEFENCE":
    # =========================
    # CSV FILE PATH
    # =========================
    CSV_FILE = "GRS DEFENCE SHEET.csv"
    st.markdown("<H3>GRS DEFENCE</H3>", unsafe_allow_html=True)
    st.markdown("<H3>Phone : 8775060274</H3>", unsafe_allow_html=True)
    st.markdown("<H3>Hours: 8am -8pm EST Monday-Friday</H3>", unsafe_allow_html=True)
    st.markdown("<H3>Bad States-AK,AK,AR,CA,DE,HI,ID,IA,KS,LA,ME,MD,MN,MT,NE,NV,NC,ND,OR,RI,SD,SC,TN,UT,VT,WV,WY</H3>", unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)


    # =========================
    # LOAD CSV DATA
    # =========================
    @st.cache_data(ttl=2)
    def load_data():
        df = pd.read_csv(CSV_FILE, dtype=str)

        # Clean column names
        df.columns = df.columns.str.strip()

        # Fill NaN
        df = df.fillna("")

        return df

    # Load dataframe
    df = load_data()

    # =========================
    # SEARCH BAR
    # =========================
    search_zip = st.text_input(
        "Enter ZIP Code",
        placeholder="Search ZIP code..."
    )

    # =========================
    # SEARCH LOGIC
    # =========================
    if search_zip:

        # Make sure ZipCode column exists
        if "ZipCode" not in df.columns:
            st.error("CSV file must contain a column named 'ZipCode'")

        else:

            # Filter matching ZIPs
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
                st.warning("No matching ZIP code found.")

    else:
        st.info("Type ZIP code in search bar.")

    # =========================
    # OPTIONAL: SHOW TOTAL DATA
    # =========================
    st.write(f"Total Records: {len(df)}")

elif page == "GRS REVERSE":

    st.markdown("<H3>GRS REVERSE</H3>", unsafe_allow_html=True)
    st.markdown("<H3>Phone : 4848044448</H3>", unsafe_allow_html=True)
    st.markdown("<H3>Nationwide- Bad States: AK, GA, HI, MA, ME, NY, RI, VT, VA,MO,DC</H3>", unsafe_allow_html=True)
    st.markdown("<H3>Hours: Mon-Fri 6am-5pm-PST</H3>", unsafe_allow_html=True)
    st.markdown("<H3>Call Filters:</H3>", unsafe_allow_html=True)
    st.markdown("\n* Age 62\n* $120K minimum home value\n* LTV less than 40%\n* Must not be investment Property\n", unsafe_allow_html=True)
    st.markdown("<H3>Link: https://www.bankrate.com/home-equity/home-equity-calculator/</H3>", unsafe_allow_html=True)

elif page == "SMS REV OVER-10K+":
    st.markdown("<H3>SMS REV OVER-10K+</H3>", unsafe_allow_html=True)
    st.markdown("<H3>Phone : 2544427086</H3>", unsafe_allow_html=True)
    st.markdown("<H3>Nationwide- Bad States: OR</H3>", unsafe_allow_html=True)
    st.markdown("<H3>Campaign Hours: 9am to 7.30pm EST</H3>", unsafe_allow_html=True)
    st.markdown("<H3>AFFORDABILITY- 250$-300$</H3>", unsafe_allow_html=True)
    st.markdown("<H3>Link: https://infutive.in/apiform/Debt-RevShare//</H3>", unsafe_allow_html=True)



elif page == "SMS REV-UNDER-6K+":
    st.markdown("<H3>SMS REV-UNDER-6K+</H3>", unsafe_allow_html=True)
    st.markdown("<H3>Phone : 2543293489</H3>", unsafe_allow_html=True)
    st.markdown("<H3>NATIONWIDE</H3>", unsafe_allow_html=True)
    st.markdown("<H3>Campaign Hours: 9am to 7.30pm EST</H3>", unsafe_allow_html=True)
    st.markdown("<H3>AFFORDABILITY- 220$</H3>", unsafe_allow_html=True)
    st.markdown("<H3>Link: https://infutive.in/apiform/Sub10Debt-RevShare/index.php</H3>", unsafe_allow_html=True)


elif page == "GRS Tax 10k":
    CSV_FILE = "GRS TAX 10k.csv"
    st.markdown("<H3>GRS Tax 10k</H3>", unsafe_allow_html=True)
    st.markdown("<H3>Phone : 8776840537</H3>", unsafe_allow_html=True)
    st.markdown("<H3>Call Buffer: 120 Seconds</H3>", unsafe_allow_html=True)
    
    # =========================
    # LOAD CSV DATA
    # =========================
    @st.cache_data(ttl=2)
    def load_data():
        df = pd.read_csv(CSV_FILE, dtype=str)

        # Clean column names
        df.columns = df.columns.str.strip()

        # Fill NaN
        df = df.fillna("")

        return df

    # Load dataframe
    df = load_data()

    # =========================
    # SEARCH BAR
    # =========================
    search_zip = st.text_input(
        "Enter ZIP Code",
        placeholder="Search ZIP code..."
    )

    # =========================
    # SEARCH LOGIC
    # =========================
    if search_zip:

        # Make sure ZipCode column exists
        if "ZipCode" not in df.columns:
            st.error("CSV file must contain a column named 'ZipCode'")

        else:

            # Filter matching ZIPs
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
                st.warning("No matching ZIP code found.")

    else:
        st.info("Type ZIP code in search bar.")

    # =========================
    # OPTIONAL: SHOW TOTAL DATA
    # =========================
    st.write(f"Total Records: {len(df)}")
