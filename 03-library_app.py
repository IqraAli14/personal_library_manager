import streamlit as st
import sqlite3

# Database connection
conn = sqlite3.connect("library.db", check_same_thread=False)
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        year INTEGER,
        genre TEXT,
        read_status BOOLEAN
    )
''')
conn.commit()

# Streamlit UI
st.title("📚 Personal Library Manager")
st.sidebar.header("Navigation")
menu = st.sidebar.radio("Go to", ["Add Book", "View Books", "Search Book", "Update Read Status", "Delete Book"])

# Add Book
if menu == "Add Book":
    st.subheader("➕ Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=1500, max_value=2050, step=1)
    genre = st.text_input("Genre")
    read_status = st.selectbox("Read Status", ["Not Read", "Read"])
    if st.button("Add Book"):
        cursor.execute("INSERT INTO books (title, author, year, genre, read_status) VALUES (?, ?, ?, ?, ?)",
                       (title, author, year, genre, 1 if read_status == "Read" else 0))
        conn.commit()
        st.success("✅ Book Added Successfully!")

# View Books
elif menu == "View Books":
    st.subheader("📖 View All Books")
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    for book in books:
        st.write(f"📘 **{book[1]}** by {book[2]} ({book[3]}) - Genre: {book[4]} - Read: {'✅' if book[5] else '❌'}")

# Search Book
elif menu == "Search Book":
    st.subheader("🔎 Search for a Book")
    search_query = st.text_input("Enter Book Title or Author")
    if st.button("Search"):
        cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", ('%'+search_query+'%', '%'+search_query+'%'))
        results = cursor.fetchall()
        if results:
            for book in results:
                st.write(f"📘 **{book[1]}** by {book[2]} ({book[3]}) - Genre: {book[4]} - Read: {'✅' if book[5] else '❌'}")
        else:
            st.warning("❌ No book found.")

# Update Read Status
elif menu == "Update Read Status":
    st.subheader("✅ Update Book Read Status")
    cursor.execute("SELECT id, title FROM books")
    books = cursor.fetchall()
    book_dict = {f"{book[0]} - {book[1]}": book[0] for book in books}
    selected_book = st.selectbox("Select a Book", list(book_dict.keys()))
    if st.button("Mark as Read"):
        cursor.execute("UPDATE books SET read_status = 1 WHERE id = ?", (book_dict[selected_book],))
        conn.commit()
        st.success("📖 Book marked as Read!")

# Delete Book
elif menu == "Delete Book":
    st.subheader("🗑️ Delete a Book")
    cursor.execute("SELECT id, title FROM books")
    books = cursor.fetchall()
    book_dict = {f"{book[0]} - {book[1]}": book[0] for book in books}
    selected_book = st.selectbox("Select a Book to Delete", list(book_dict.keys()))
    if st.button("Delete"):
        cursor.execute("DELETE FROM books WHERE id = ?", (book_dict[selected_book],))
        conn.commit()
        st.warning("🚨 Book Deleted Successfully!")

# Close the database connection
conn.close()
