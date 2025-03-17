import sqlite3
import json

# Database and JSON file setup
DB_NAME = "library.db"
JSON_FILE = "library.json"

def connect_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT,
                      author TEXT,
                      year INTEGER,
                      genre TEXT,
                      read_status BOOLEAN)''')
    conn.commit()
    return conn

def load_from_json():
    try:
        with open(JSON_FILE, "r") as file:
            books = json.load(file)
        conn = connect_db()
        cursor = conn.cursor()
        for book in books:
            cursor.execute("INSERT INTO books (title, author, year, genre, read_status) VALUES (?, ?, ?, ?, ?)",
                           (book["title"], book["author"], book["year"], book["genre"], book["read_status"]))
        conn.commit()
        conn.close()
    except FileNotFoundError:
        pass  # No JSON file exists yet, so no data to load

def save_to_json():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT title, author, year, genre, read_status FROM books")
    books = [{"title": row[0], "author": row[1], "year": row[2], "genre": row[3], "read_status": row[4]} for row in cursor.fetchall()]
    conn.close()
    with open(JSON_FILE, "w") as file:
        json.dump(books, file, indent=4)

def add_book():
    title = input("Enter book title: ")
    author = input("Enter author: ")
    year = int(input("Enter publication year: "))
    genre = input("Enter genre: ")
    read_status = input("Have you read this book? (yes/no): ").strip().lower() == "yes"
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, year, genre, read_status) VALUES (?, ?, ?, ?, ?)",
                   (title, author, year, genre, read_status))
    conn.commit()
    conn.close()
    save_to_json()
    print("Book added successfully!")

def remove_book():
    title = input("Enter book title to remove: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE title = ?", (title,))
    conn.commit()
    conn.close()
    save_to_json()
    print("Book removed successfully!")

def search_book():
    search_type = input("Search by Title (1) or Author (2)? Enter choice: ")
    query = input("Enter search query: ")
    conn = connect_db()
    cursor = conn.cursor()
    if search_type == "1":
        cursor.execute("SELECT * FROM books WHERE title LIKE ?", ('%' + query + '%',))
    else:
        cursor.execute("SELECT * FROM books WHERE author LIKE ?", ('%' + query + '%',))
    books = cursor.fetchall()
    conn.close()
    if books:
        for book in books:
            print(f"{book[1]} by {book[2]} ({book[3]}) - {book[4]} - {'Read' if book[5] else 'Unread'}")
    else:
        print("No books found.")

def display_books():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    if books:
        for book in books:
            print(f"{book[1]} by {book[2]} ({book[3]}) - {book[4]} - {'Read' if book[5] else 'Unread'}")
    else:
        print("No books in the library.")

def display_statistics():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM books WHERE read_status = 1")
    read_books = cursor.fetchone()[0]
    conn.close()
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
    print(f"Total books: {total_books}\nPercentage read: {percentage_read:.2f}%")

def main():
    load_from_json()  # Load JSON data at the start
    while True:
        print("\nPersonal Library Manager")
        print("1. Add a book")
        print("2. Remove a book")
        print("3. Search for a book")
        print("4. Display all books")
        print("5. Display statistics")
        print("6. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            add_book()
        elif choice == "2":
            remove_book()
        elif choice == "3":
            search_book()
        elif choice == "4":
            display_books()
        elif choice == "5":
            display_statistics()
        elif choice == "6":
            save_to_json()
            print("Library saved. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
