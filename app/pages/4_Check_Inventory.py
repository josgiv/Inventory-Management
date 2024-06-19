import os
import sqlite3
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Menu Cek Inventaris", page_icon="📝")

class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, data):
        if not self.root:
            self.root = TreeNode(data)
        else:
            self._insert_recursive(self.root, data)

    def _insert_recursive(self, node, data):
        if data[0] < node.data[0]:
            if node.left:
                self._insert_recursive(node.left, data)
            else:
                node.left = TreeNode(data)
        else:
            if node.right:
                self._insert_recursive(node.right, data)
            else:
                node.right = TreeNode(data)

    def inorder_traversal(self, node, result):
        if node:
            self.inorder_traversal(node.left, result)
            result.append(node.data)
            self.inorder_traversal(node.right, result)

    def search(self, node, key, result):
        if node:
            if key in node.data:
                result.append(node.data)
            self.search(node.left, key, result)
            self.search(node.right, key, result)

def show_inventory_table(cursor):
    cursor.execute("SELECT ID, Tanggal, Nama_Barang, Kategori, Jumlah FROM Daftar_Inventaris")
    inventaris = cursor.fetchall()

    bst = BST()
    for item in inventaris:
        bst.insert(item)

    result = []
    bst.inorder_traversal(bst.root, result)

    df_inventaris = pd.DataFrame(result, columns=["ID", "Tanggal", "Nama Barang", "Kategori", "Jumlah"])

    st.sidebar.subheader("Filter Daftar Inventaris")
    selected_kategori = st.sidebar.multiselect("Kategori", options=df_inventaris["Kategori"].unique(), default=df_inventaris["Kategori"].unique(), key="inventory_kategori_multiselect")
    df_inventaris = df_inventaris[df_inventaris["Kategori"].isin(selected_kategori)]

    sort_by = st.sidebar.selectbox("Urutkan Berdasarkan", options=["ID", "Tanggal", "Nama Barang", "Kategori", "Jumlah"], key="inventory_sort_by_selectbox")
    sort_order = st.sidebar.radio("Urutan", options=["Ascending", "Descending"], key="inventory_sort_order_radio")

    if sort_order == "Ascending":
        df_inventaris = df_inventaris.sort_values(by=sort_by, ascending=True)
    else:
        df_inventaris = df_inventaris.sort_values(by=sort_by, ascending=False)

    st.dataframe(df_inventaris, height=400, use_container_width=True)
    
    st.write("## Hapus Data Inventaris")
    selected_id = st.selectbox("Pilih ID untuk dihapus:", df_inventaris["ID"].tolist(), key="delete_inventory_id_selectbox")
    if st.button("Hapus Inventaris"):
        cursor.execute("DELETE FROM Daftar_Inventaris WHERE ID = ?", (selected_id,))
        conn.commit()
        st.rerun()

def show_defective_table(cursor):
    cursor.execute("SELECT ID, Tanggal, Nama_Barang, Kategori, Jumlah, Alasan FROM Inventaris_Rusak")
    defective = cursor.fetchall()

    bst = BST()
    for item in defective:
        bst.insert(item)

    result = []
    bst.inorder_traversal(bst.root, result)

    df_defective = pd.DataFrame(result, columns=["ID", "Tanggal", "Nama Barang", "Kategori", "Jumlah", "Alasan"])

    st.sidebar.subheader("Filter Barang Rusak/Hilang")
    selected_kategori_def = st.sidebar.multiselect("Kategori", options=df_defective["Kategori"].unique(), default=df_defective["Kategori"].unique(), key="defective_kategori_multiselect")
    df_defective = df_defective[df_defective["Kategori"].isin(selected_kategori_def)]

    sort_by = st.sidebar.selectbox("Urutkan Berdasarkan", options=["ID", "Tanggal", "Nama Barang", "Kategori", "Jumlah", "Alasan"], key="defective_sort_by_selectbox")
    sort_order = st.sidebar.radio("Urutan", options=["Ascending", "Descending"], key="defective_sort_order_radio")

    if sort_order == "Ascending":
        df_defective = df_defective.sort_values(by=sort_by, ascending=True)
    else:
        df_defective = df_defective.sort_values(by=sort_by, ascending=False)

    st.write("## Daftar Inventaris Rusak")
    st.dataframe(df_defective, height=400, use_container_width=True)
    
    st.write("## Hapus Data Inventaris Rusak")
    selected_id_def = st.selectbox("Pilih ID untuk dihapus:", df_defective["ID"].tolist(), key="delete_defective_id_selectbox")
    if st.button("Hapus Inventaris Rusak"):
        cursor.execute("DELETE FROM Inventaris_Rusak WHERE ID = ?", (selected_id_def,))
        conn.commit()
        st.rerun()

def show_all_tables():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    os.chdir(current_dir)

    db_path = os.path.join('..', '..', 'database', 'inventaris.db')
    global conn  # Define conn globally to ensure it can be used in the show_inventory_table and show_defective_table functions
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    show_inventory_table(cursor)
    st.write("\n---\n")
    show_defective_table(cursor)

    conn.close()

    
def main():
    st.title("Daftar Inventaris CV. Dilobby Terus")
    st.markdown("""
    Aplikasi ini menampilkan daftar inventaris CV. Dilobby Terus, termasuk barang-barang yang rusak atau hilang.
    """)
    show_all_tables()

if __name__ == "__main__":
    main()
