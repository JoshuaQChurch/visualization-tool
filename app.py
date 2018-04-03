import pandas as pd
from plotly.offline import plot as plt
import plotly.graph_objs as go
from tkinter import filedialog
from tkinter import *
import os


# Main menu / upload file
def menu():
    destroy()
    geometry(250, 250)
    Label(root, text="Histogram Tool", font=("Arial", 18, "bold")).pack()
    Button(root, text="Select File", height=250, width=250, command=lambda: upload(), font=("Arial", 15)).pack()

# Handler for uploading a file 
def upload():

    # Set the path to the datasets folder 
    initialdir = os.path.normpath(os.getcwd())

    title = "Select your file"
    filetypes = (("Comma Separated Values", "*.csv"), ("Excel Workbook", "*.xlsx"), 
                ("Legacy Excel Worksheets", "*.xls"))

    path_to_file = filedialog.askopenfilename(initialdir=initialdir, title=title, filetypes=filetypes)
    
    # If 'cancel' is not clicked
    if path_to_file:

        # Extract the filename from the path
        filename = os.path.basename(path_to_file)
        split = filename.split('.')
        if len(split) >= 2:
            filename = '.'.join(split[0:-1])
            
            # Check the extension of the file
            extension = split[-1]

            # CSV files
            if extension.lower() == "csv":
                df = pd.read_csv(path_to_file, low_memory=False)
                select_columns(df)
            
            # Excel files
            elif extension.lower() in ["xls", "xlsx"]:
                df = pd.read_excel(path_to_file, low_memory=False)
                select_columns(df)


# Add column to the list
def add_column(selection, columns, listbox):
    if selection not in listbox.get(0, END):
        if selection in columns:
            listbox.insert(END, selection)


# Filter search results
def filter_columns(query, columns, search_results):
    search_results.delete(0, END)

    if query != '':
        results = [i for i in columns if query.lower() in i.lower()]
        for r in results:
            search_results.insert(END, r)

def add_search_results(search_results, selected_columns, columns):
    
    try:
        # Get the index location of the selected element
        indices = search_results.curselection()

        # Get the value from the index
        selected = [search_results.get(i) for i in indices]

        # Exclude any whitespace
        selected = [i for i in selected if i.strip() != '']

        # Only select results from the allowed columns
        selected = [i for i in selected if i in columns]

        # Select only non-duplicated results
        selected = [i for i in selected if i not in selected_columns.get(0, END)] 

        # Results found
        if selected:
            for i in selected:
                selected_columns.insert(END, i)

    except: 
        return 


def select_columns(df):
    destroy()
    columns = sorted(df.columns)

    geometry(550, 450)
    root.resizable(True, True)

    font = ("Arial", 18, "bold")

    # Search
    query = StringVar()
    Label(root, text="Search for column", font=font).place(x=30, y=10)
    query.trace('w', lambda name, index, mode, query=query: filter_columns(query.get(), columns, search_results))
    Entry(root, textvariable=query).place(x=20, y=40)

    # Search Results
    Label(root, text="Search Results", font=font).place(x=30, y=100)
    search_results = Listbox(selectmode=MULTIPLE)
    search_results.place(x=20, y=135)
    Button(root, text="Add Selected", command=lambda: add_search_results(search_results, currently_selected, columns)).place(x=20, y=320)
    Button(root, text="Clear", command=lambda: query.set('')).place(x=140, y=320)

    # Dropdown
    dropdown = StringVar()
    dropdown.set(columns[0])
    Label(root, text="Select Column", font=font).place(x=300, y=10)
    OptionMenu(root, dropdown, *columns).place(x=300, y=35)
    Button(root, text="Add", command=lambda: add_column(dropdown.get(), columns, currently_selected)).place(x=300, y=60)

    # Currently selected values
    Label(root, text="Selected Columns", font=font).place(x=310, y=100)
    currently_selected = Listbox()
    currently_selected.place(x=300, y=135)
    Button(root, text="Plot Selected", command=lambda: plot(currently_selected.get(0, END), df)).place(x=260, y=320)
    Button(root, text="Delete", command=lambda currently_selected=currently_selected: currently_selected.delete(ANCHOR)).place(x=370, y=320)
    Button(root, text="Delete All", command=lambda currently_selected=currently_selected: currently_selected.delete(0, END)).place(x=440, y=320)

    # Main menu 
    Label(root, text="Back to Main Menu", font=font).place(x=20, y=370)
    Button(root, text="Change File", command=lambda: menu()).place(x=20, y=400)


# Set the dimensions of the GUI
def geometry(height, width):
    root.geometry(str(height) + "x" + str(width))


# Remove all widgets from the current frame
def destroy():
    for widget in root.winfo_children():
        widget.destroy()


# Plot the selected values
def plot(selected, df):
    columns = list(selected)
    filename = "histogram.html"

    if len(columns) > 0:
        traces = []
        for column in columns:
            print(df[column])
            traces.append(
                go.Histogram(
                    x = df[column],
                    name = column
                )
            )

        plt(traces, filename=filename)


if __name__ == "__main__":
    root = Tk()
    menu()
    root.mainloop()
