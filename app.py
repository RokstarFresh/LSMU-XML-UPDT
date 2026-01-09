import streamlit as st
import re
from io import StringIO

# Page configuration
st.set_page_config(page_title="XML Updater Tool", page_icon="📂")

st.title("XML File Updater")
st.markdown("""
This tool appends missing issue/volume data to your XML file.

1. Upload your XML file.
2. Enter the required details.
3. Download the corrected file.
""")

# --- 1. File Upload ---
uploaded_file = st.file_uploader("Upload XML file", type="xml")

# --- 2. User Inputs ---
st.subheader("Enter Details")

with st.form("user_inputs"):
    col1, col2 = st.columns(2)
    with col1:
        vol = st.text_input("Volume", placeholder="e.g., 105")
        iss = st.text_input("Issue", placeholder="e.g., 2")
    with col2:
        year = st.text_input("Year", placeholder="e.g., 2024")
        date = st.text_input("Date (YYYY-MM-DD)", placeholder="e.g., 2024-03-20")

    submitted = st.form_submit_button("Process File", type="primary")

# --- 3. Processing Logic ---
if submitted:
    if uploaded_file is None:
        st.warning("⚠️ Please upload an XML file first.")
    else:
        # Validation
        errors = []
        if not vol.isdigit(): errors.append("❌ Volume must be a number.")
        if not iss.isdigit(): errors.append("❌ Issue must be a number.")
        if not year.isdigit(): errors.append("❌ Year must be a number.")
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date): errors.append("❌ Date must be in YYYY-MM-DD format.")

        if errors:
            for err in errors:
                st.error(err)
        else:
            # Read file
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            content = stringio.read()

            # The data block to insert
            new_block = f"""
        <issue-title content-type="ISSUE">Volumes {vol}, Issues {iss}, ({year}): Veterinarija ir Zootechnika</issue-title>
        <volume>{vol}</volume>
        <issue>{iss}</issue>
        <pub-date iso-8601-date="{date}"/>
        <pub-date pub-type="ppub">
            <year>{year}</year>
        </pub-date>"""

            target_tag = "</lpage>"

            if target_tag in content:
                # Modify content
                modified_content = content.replace(target_tag, target_tag + new_block)

                st.success("✅ Success! Missing lines added.")

                # Create Download Button
                new_filename = f"corrected_vol{vol}_iss{iss}.xml"
                st.download_button(
                    label="Download Corrected XML",
                    data=modified_content,
                    file_name=new_filename,
                    mime="text/xml"
                )
            else:
                st.error(f"❌ Error: Could not find the tag '{target_tag}' in the uploaded file.")
