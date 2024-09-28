from tkinter import *
from tkinter import ttk, messagebox  # TreeView source
import psycopg2


def runQuery(query, parameters=()):
    conn = psycopg2.connect(
        dbname="StudentDB",
        user="",
        password="",
        host="",
        port="")
    cur = conn.cursor()  # Cursor for database manipulation
    queryResult = None
    try:
        cur.execute(query, parameters)  # Run the SQL command
        if query.lower().startswith("select"):
            queryResult = cur.fetchall()  # Store all that match the query into queryResult variable
        conn.commit()
    except psycopg2.Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        cur.close()
        conn.close()
    return queryResult  # Return the SQL query results


def refreshTreeview():
    # Clear the treeview
    for item in tree.get_children():  # For loop that goes through the contents of treeview
        tree.delete(item)  # Remove tree item
    # Fill the treeview
    records = runQuery("SELECT * FROM students;")  # Get everything from students table
    for record in records:
        tree.insert('', END, values=record)  # Put everything into the treeview


def insertData():
    query = "INSERT INTO students(NAME, ADDRESS, AGE, NUMBER) VALUES (%s, %s, %s, %s);"
    parameters = (nameEntry.get(), addressEntry.get(), ageEntry.get(), phoneEntry.get())  # Get student info
    runQuery(query, parameters)  # Run the insertion command
    refreshTreeview()  # Update the treeview

    # Clear the entry fields
    nameEntry.delete(0, END)
    addressEntry.delete(0, END)
    ageEntry.delete(0, END)
    phoneEntry.delete(0, END)

    messagebox.showinfo("Information", "Data inserted successfully")


def deleteData():
    selectedItem = tree.selection()[0]  # Returns the database form id number of the selected student (blue highlight) from the treeview ex: I003
    studentId = tree.item(selectedItem)['values'][0]  # Returns the useful number part ex: 3
    query = "DELETE FROM students WHERE ID = %s;"
    parameters = (studentId,)  # Comma is to signify tuple not function call
    runQuery(query, parameters)  # Run deletion command
    refreshTreeview()  # Update the treeview
    messagebox.showinfo("Information", "Data deleted successfully")


def updateData():
    selectedItem = tree.selection()[0]  # Returns the database form id number of the selected student (blue highlight) from the treeview ex: I003
    studentId = tree.item(selectedItem)['values'][0]  # Returns the useful number part ex: 3
    query = "UPDATE students SET NAME = %s, ADDRESS = %s, AGE = %s, NUMBER = %s WHERE ID = %s;"
    parameters = (nameEntry.get(), addressEntry.get(), ageEntry.get(), phoneEntry.get(), studentId)  # Supply student info with id# to query
    runQuery(query, parameters)  # Run update command
    refreshTreeview()  # Update the treeview

    # Clear the entry fields
    nameEntry.delete(0, END)
    addressEntry.delete(0, END)
    ageEntry.delete(0, END)
    phoneEntry.delete(0, END)

    messagebox.showinfo("Information", "Data updated successfully")


def createTable():
    query = "CREATE TABLE IF NOT EXISTS students(ID SERIAL, NAME TEXT, ADDRESS TEXT, AGE INT, NUMBER INT);"
    runQuery(query)
    messagebox.showinfo("Information", "Table created successfully")
    refreshTreeview()  # Update the treeview


root = Tk()
root.title("Student Management System GUI")

frame = LabelFrame(root, text="Student Data", font=('Times', 14))
frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")


# Widgets
# NAME
Label(frame, text="Name:", font=('Times', 12)).grid(row=0, column=0, padx=2, sticky="w")
nameEntry = Entry(frame, width=54, font='Times 12')
nameEntry.grid(row=0, column=1, pady=2, sticky="ew")

# ADDRESS
Label(frame, text="Address:", font=('Times', 12)).grid(row=1, column=0, padx=2, sticky="w")
addressEntry = Entry(frame, width=54, font='Times 12')
addressEntry.grid(row=1, column=1, pady=2, sticky="ew")

# AGE
Label(frame, text="Age:", font=('Times', 12)).grid(row=2, column=0, padx=2, sticky="w")
ageEntry = Entry(frame, width=54, font='Times 12')
ageEntry.grid(row=2, column=1, pady=2, sticky="ew")

# PHONE NUMBER
Label(frame, text="Phone #:", font=('Times', 12)).grid(row=3, column=0, padx=2, sticky="w")
phoneEntry = Entry(frame, width=54, font='Times 12')
phoneEntry.grid(row=3, column=1, pady=2, sticky="ew")

# BUTTONS
buttonFrame = Frame(root)
buttonFrame.grid(row=1, column=0, pady=5, sticky="ew")

Button(buttonFrame, text="Create Table", font=('Times', 12), command=createTable).grid(row=0, column=0, padx=5)
Button(buttonFrame, text="Add Data", font=('Times', 12), command=insertData).grid(row=0, column=1, padx=5)
Button(buttonFrame, text="Update Data", font=('Times', 12), command=updateData).grid(row=0, column=2, padx=5)
Button(buttonFrame, text="Delete Data", font=('Times', 12), command=deleteData).grid(row=0, column=3, padx=5)

# DATA DISPLAY
treeFrame = Frame(root)
treeFrame.grid(row=2, column=0, padx=10, sticky="nsew")

treeScroll = Scrollbar(treeFrame)
treeScroll.pack(side=RIGHT, fill=Y)

tree = ttk.Treeview(treeFrame, yscrollcommand=treeScroll.set, selectmode="browse")  # Browse means one item can be selected at a time
tree.pack()
treeScroll.config(command=tree.yview)

# DISPLAY AREA COLUMNS
tree['columns'] = ("Student_ID", "Name", "Address", "Age", "Phone #")
tree.column("#0", width=0, stretch=NO)  # Remove first column
tree.column("Student_ID", anchor=CENTER, width=80)
tree.column("Name", anchor=CENTER, width=120)
tree.column("Address", anchor=CENTER, width=120)
tree.column("Age", anchor=CENTER, width=50)
tree.column("Phone #", anchor=CENTER, width=120)

# DISPLAY AREA HEADINGS
tree.heading("Student_ID", text="ID", anchor=CENTER)
tree.heading("Name", text="Name", anchor=CENTER)
tree.heading("Address", text="Address", anchor=CENTER)
tree.heading("Age", text="Age", anchor=CENTER)
tree.heading("Phone #", text="Phone #", anchor=CENTER)

refreshTreeview()  # Reveal database contents right from the start

root.mainloop()
