from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import database


def insert_data():
    vendor_name = entry_vendor_name.get()
    transaction_details = entry_transaction_details.get()
    date = entry_date.get()
    amount_sent = entry_amount_sent.get()
    amount_received = entry_amount_received.get()

    if vendor_name and date and (amount_sent or amount_received):
        database.insert_data(vendor_name, transaction_details, date, float(amount_sent or 0), float(amount_received or 0))
        messagebox.showinfo("Success", "Transaction added successfully!")
        clear_entries()
        view_all_transactions()
    else:
        messagebox.showerror("Error", "Please fill in the required fields")

def update_data():
    selected_item = tree.selection()[0]
    transaction_id = tree.item(selected_item)['values'][0]
    vendor_name = entry_vendor_name.get()
    transaction_details = entry_transaction_details.get()
    date = entry_date.get()
    amount_sent = entry_amount_sent.get()
    amount_received = entry_amount_received.get()

    if vendor_name and date and (amount_sent or amount_received):
        database.update_data(transaction_id, vendor_name, transaction_details, date, float(amount_sent or 0), float(amount_received or 0))
        messagebox.showinfo("Success", "Transaction updated successfully!")
        clear_entries()
        view_all_transactions()
    else:
        messagebox.showerror("Error", "Please fill in the required fields")

def calculate_totals_by_person():
    vendor_name = entry_vendor_name.get()
    if vendor_name:
        totals = database.calculate_totals_by_person(vendor_name)
        lbl_totals.config(text=f"Total Sent: {totals[0]}\nTotal Received: {totals[1]}")
    else:
        messagebox.showerror("Error", "Please enter a vendor name")

def calculate_monthly_totals():
    year = entry_year.get()
    month = entry_month.get()
    if year and month:
        totals = database.calculate_monthly_totals(year, month)
        lbl_totals.config(text=f"Total Sent in {month}/{year}: {totals[0]}\nTotal Received in {month}/{year}: {totals[1]}")
    else:
        messagebox.showerror("Error", "Please enter both year and month")

def view_all_transactions():
    for item in tree.get_children():
        tree.delete(item)
    conn = database.create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    conn.close()

def view_history():
    vendor_name = entry_vendor_name.get()
    if vendor_name:
        history = database.view_history(vendor_name)
        for item in tree.get_children():
            tree.delete(item)
        for row in history:
            tree.insert("", "end", values=row)
    else:
        messagebox.showerror("Error", "Please enter a vendor name")

def clear_entries():
    entry_vendor_name.delete(0, END)
    entry_transaction_details.delete(0, END)
    entry_date.set_date('')
    entry_amount_sent.delete(0, END)
    entry_amount_received.delete(0, END)

def main():
    root = Tk()
    root.title("Vendor Dealer Transactions")
    root.geometry("1300x700")

    frame_input = Frame(root)
    frame_input.pack(pady=10)

    lbl_vendor_name = Label(frame_input, text="Vendor Name")
    lbl_vendor_name.grid(row=0, column=0)
    global entry_vendor_name
    entry_vendor_name = Entry(frame_input)
    entry_vendor_name.grid(row=0, column=1, padx=10)

    lbl_transaction_details = Label(frame_input, text="Online") #Transaction Details
    lbl_transaction_details.grid(row=1, column=0)
    global entry_transaction_details
    entry_transaction_details = Entry(frame_input)
    entry_transaction_details.grid(row=1, column=1, padx=10)

    lbl_date = Label(frame_input, text="Date")
    lbl_date.grid(row=2, column=0)
    global entry_date
    entry_date = DateEntry(frame_input, date_pattern='yyyy-mm-dd')
    entry_date.grid(row=2, column=1, padx=10)

    lbl_amount_sent = Label(frame_input, text="Amount Sent")
    lbl_amount_sent.grid(row=3, column=0)
    global entry_amount_sent
    entry_amount_sent = Entry(frame_input)
    entry_amount_sent.grid(row=3, column=1, padx=10)

    lbl_amount_received = Label(frame_input, text="Amount Received")
    lbl_amount_received.grid(row=4, column=0)
    global entry_amount_received
    entry_amount_received = Entry(frame_input)
    entry_amount_received.grid(row=4, column=1, padx=10)

    btn_insert = Button(frame_input, text="Insert", command=insert_data)
    btn_insert.grid(row=5, column=0, pady=10)

    btn_update = Button(frame_input, text="Update", command=update_data)
    btn_update.grid(row=5, column=1, pady=10)

    frame_display = Frame(root)
    frame_display.pack(pady=10)

    global tree
    tree = ttk.Treeview(frame_display, columns=("ID", "Vendor", "Details", "Date", "Sent", "Received"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Vendor", text="Vendor")
    tree.heading("Details", text="Details")
    tree.heading("Date", text="Date")
    tree.heading("Sent", text="Sent")
    tree.heading("Received", text="Received")
    tree.pack()

    frame_statistics = Frame(root)
    frame_statistics.pack(pady=10)

    lbl_year = Label(frame_statistics, text="Year")
    lbl_year.grid(row=0, column=0)
    global entry_year
    entry_year = Entry(frame_statistics)
    entry_year.grid(row=0, column=1, padx=10)

    lbl_month = Label(frame_statistics, text="Month")
    lbl_month.grid(row=1, column=0)
    global entry_month
    entry_month = Entry(frame_statistics)
    entry_month.grid(row=1, column=1, padx=10)

    btn_calculate_totals = Button(frame_statistics, text="Calculate Totals by Person", command=calculate_totals_by_person)
    btn_calculate_totals.grid(row=2, column=0, pady=10)

    btn_calculate_monthly_totals = Button(frame_statistics, text="Calculate Monthly Totals", command=calculate_monthly_totals)
    btn_calculate_monthly_totals.grid(row=2, column=1, pady=10)

    btn_view_history = Button(frame_statistics, text="View History", command=view_history)
    btn_view_history.grid(row=3, column=0, pady=10)

    global lbl_totals
    lbl_totals = Label(frame_statistics, text="")
    lbl_totals.grid(row=4, column=0, columnspan=2)

    view_all_transactions()
    root.mainloop()

if __name__ == "__main__":
    database.create_table()
    main()
