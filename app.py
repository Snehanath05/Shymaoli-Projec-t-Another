import streamlit as st
import nbformat
from nbconvert import HTMLExporter
from streamlit.components.v1 import html
import os
from io import StringIO

st.set_page_config(page_title="Notebook Viewer", layout="wide")

st.title("📒 Jupyter Notebook Viewer")

# Sidebar
option = st.sidebar.radio(
    "Choose Option",
    ["Upload Notebook", "Open Local Notebook"]
)

def render_notebook(nb_content):
    try:
        notebook = nbformat.reads(nb_content, as_version=4)
        html_exporter = HTMLExporter()
        body, _ = html_exporter.from_notebook_node(notebook)
        html(body, height=800, scrolling=True)
    except Exception as e:
        st.error(f"Error rendering notebook: {e}")

# -------- OPTION 1: Upload Notebook --------
if option == "Upload Notebook":
    uploaded_file = st.file_uploader("Upload .ipynb file", type=["ipynb"])

    if uploaded_file is not None:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        nb_content = stringio.read()
        render_notebook(nb_content)

# -------- OPTION 2: Open Local Notebook --------
elif option == "Open Local Notebook":
    file_path = st.text_input("Enter notebook path (example: notebook.ipynb)")

    if st.button("Open Notebook"):
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                nb_content = f.read()
                render_notebook(nb_content)
        else:
            st.error("File not found. Check the path.")
