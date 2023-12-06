import streamlit as st

def data_file_upload():
    st.session_state.db_available = st.session_state.get("db_available", False)
    if not st.session_state.db_available:
        uploaded_file = st.file_uploader("Upload SQLite Database", type=["db"])
        if uploaded_file is not None:
            with open("database.db", "wb") as f:
                f.write(uploaded_file.getvalue())
            st.success("Database file uploaded successfully.")
            st.session_state.db_file_uploaded = True
    else:
        st.write("Database file already uploaded.")
    return st.session_state.db_available

def data_file_download():
    if st.session_state.db_available:
        with open("database.db", "rb") as f:
            contents = f.read()
        if st.download_button("Download", data=contents, file_name="downloaded_database.db", mime="application/octet-stream"):
            st.success("Database file downloaded successfully.")

# Streamlit app
def main():
    st.sidebar.header("Database")
    data_file_upload()
    if st.session_state.db_file_uploaded:
        # Determine the database type based on the file extension or other logic
        database_type = "sqlite"  # Placeholder, should be determined dynamically
        handler = DBHandler(database_type=database_type, database="database.db")
        handler.initialize_interface()
        # Perform actual database operations using the handler.interface methods
        # Example: handler.interface.execute_query("SELECT * FROM table_name")
        data_file_download()
    else:
        st.error("No database file uploaded.")

if __name__ == "__main__":
    main()