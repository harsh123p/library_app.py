import streamlit as st
import pandas as pd
from datetime import datetime
import os
import csv
from streamlit_option_menu import option_menu


import db 

st.set_page_config(page_title="Library Managemane", layout="centered")
db.create_tables()

STUDENT_FILE = "students.csv"

def save_student_to_csv(student):
    file_exists = os.path.isfile(STUDENT_FILE)
    with open(STUDENT_FILE, mode='a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=student.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(student)

def load_students_from_csv():
    if not os.path.exists(STUDENT_FILE):
        return []
    with open(STUDENT_FILE, mode='r') as f:
        return list(csv.DictReader(f))

st.title("📚 Library Management System")
with st.sidebar:
    selected=option_menu("Select Action", ["Add Book", "View Books","Issue Book","Return Book", "Manage Students"])

if selected =="Add Book":
    st.header("➕ Add a New Book")
    with st.form("add_book_form"):
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        category = st.text_input("category")
        copies = st.number_input("Copies", min_value=0, step=10)
        submit = st.form_submit_button("Add Book")
        if submit:
            db.add_book(title, author, category, copies)
            st.success(f"Book '{title}' added successfully!")

elif selected== "View Books":
    st.header("📓 All Books")
    books = db.get_all_books()
    st.dataframe(books)

    with st.expander("🗑 Delete Book"):
        book_id = st.number_input("Enter Book ID to delete", step=1)
        if st.button("Delete Book"):
            db.delete_book(book_id)
            st.warning(f"Book ID {book_id} deleted.")

elif selected=="Issue Book":
    st.header("📤 Issue a Book")
    books = db.get_all_books()
    st.dataframe(books[['id', 'title', 'copies']])

    with st.form("issue_book_form"):
        book_id = st.number_input("Enter Book ID", step=1)
        borrower = st.text_input("Borrower Name (Student ID or Name)")
        submit = st.form_submit_button("Issue Book")
        if submit:
            db.issue_book(book_id, borrower)
            st.success(f"Issued Book ID {book_id} to {borrower}")

elif selected=="Return Book":
    st.header("📥 Return a Book")
    issued_books = db.get_issued_books()
    st.dataframe(issued_books)

    with st.form("return_book_form"):
        transaction_id = st.number_input("Transaction ID", step=1)
        submit = st.form_submit_button("Return Book")
        if submit:
            db.return_book(transaction_id)
            st.success(f"Returned book for Transaction ID {transaction_id}")

elif selected== "Manage Students":
    st.header("🧑🏻‍🎓 Manage Students")

    with st.form("add_student_form"):
        student_id = st.text_input("Student ID")
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        course = st.text_input("Course")

        submit = st.form_submit_button("Add Student")
        if submit:
            if student_id and name and email and course:
                student = {
                    "Student ID": student_id,
                    "Name": name,
                    "Email": email,
                    "Course": course,
                    "Join Date": datetime.now().strftime('%d-%m-%y')
                }
                save_student_to_csv(student)
                st.success(f"Added student: {name}")
            else:
                st.warning("Please fill out all fields.")

    st.markdown("---")
    st.subheader("📋 All Students")
    students = load_students_from_csv()
    if students:
        st.dataframe(pd.DataFrame(students))
    else:
        st.info("No students found.")
# elif selected=="About Developers":
#     st.header("👨🏼‍💻 About Developers")


st.markdown("""
    <style>
        .footer {position: fixed; bottom: 0; left: 0;width: 100%;background:09122C ; text-align: center; padding: 2px; font-size: 12px; border-top:1px dashed ;
        }
    </style>

    <div class="footer">
        📚 Library Management System | Developed by <i><b>Harsh</b></i>
    </div>
""", unsafe_allow_html=True)
