
# st.title("welcome to my streamlit")
# st.write("I am wrting something")
# st.title("This is a title")
# st.header("header")
# st.subheader("sub header")
# st.markdown("<h1>Heading-1</h1>",unsafe_allow_html=True)
# st.markdown("<marquee>News</marquee>",unsafe_allow_html=True)
# st.image("./img/images.jpg",caption="This is an elephant")
# st.checkbox("Python")
# st.checkbox("Cpp")
# st.button("Sigin")
# st.radio("Gender",options=["Male","Female"])
# st.selectbox()
# def signup():
#     st.text_input("Enter username:")
# signup()


import streamlit as st
import sqlite3 
from streamlit_option_menu import option_menu

def connect_db():
    conn = sqlite3.connect('mydb.db')
    return conn

def create_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("Create table if not exists student (Rollno INTEGER PRIMARY KEY, name TEXT, branch text, password text)")
    conn.commit()
    conn.close()

def addRecord(data):
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO student (Rollno, name, branch, password) VALUES (?, ?,?,?)", data)
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        st.error("Student already Registered")
        conn.close()

def viewRecord():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("Select * from student")
    result = cur.fetchall()
    conn.close()
    return result

def display():
    data = viewRecord()
    if data:
        st.table(data)
    else:
        st.write("No records found.")


def delete_record(data):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(f"select * from student where Rollno={data}")
    result=cur.fetchone()
    if result[0] == data and result != None:
        cur.execute(f"delete from student where Rollno = {data}",)
        st.write("Data successfully deleted")
    else:
        st.write("Data not available")
    conn.commit()
    conn.close()


def signup():
    st.title("Signup Page")
    
    name = st.text_input("Name:")
    rollno = st.number_input("Roll Number:", format="%d")
    branch = st.selectbox("Branch:", options=["CSE", "ECE", "EEE", "MECH", "AIML"])
    password = st.text_input("Password:", type='password')
    re_password = st.text_input("Rewrite Password:", type='password')
    if st.button("Signup"):
        if password != re_password:
            st.error("Passwords do not match")
        else:
            addRecord((rollno, name, branch, password))
            st.success("Signup Successfull")

create_table()  

with st.sidebar:
    selected = option_menu("Functions",["SignUp", "Display All record","Delete"])
if selected == "SignUp":
    signup()
elif selected == "Delete":
    r=st.number_input("Enter the roll no.:")
    delete_record(r)
else:
    display()

