import streamlit as st

if "expenses" not in st.session_state:
    st.session_state.expenses = []

st.sidebar.header("Sidebar Filters")
search_query = st.sidebar.text_input("Search by Name")
selected_category = st.sidebar.selectbox("Filter Category", ["All", "Food", "Travel", "Shopping", "Bills", "Other"])
max_amount = st.sidebar.slider("Maximum Amount (Rs)", 0.0, 10000.0, 1000.0)

st.title("Personal Expense Tracker")

st.header("Add New Expense")

with st.form("expense_form"):
    name = st.text_input("Expense Name")
    amount = st.number_input("Amount (Pkr)", min_value=0.0)
    category = st.selectbox("Category", ["Food", "Travel", "Shopping", "Bills", "Other"])
    date = st.date_input("Date")
    
    submitted = st.form_submit_button("Submit Expense")
    
    if submitted:
        if name == "":
            st.error("Expense name cannot be empty.")
        elif amount <= 0:
            st.error("Amount must be greater than zero.")
        else:
            new_expense = {
                "Name": name,
                "Amount": amount,
                "Category": category,
                "Date": str(date)
            }
            st.session_state.expenses.append(new_expense)
            st.success("Expense added successfully!")

st.markdown("---")

st.header("Dashboard Summary")

total_transactions = len(st.session_state.expenses)
total_expenses = 0.0
highest_amount = 0.0
highest_name = "None"

for item in st.session_state.expenses:
    total_expenses += item["Amount"]
    if item["Amount"] > highest_amount:
        highest_amount = item["Amount"]
        highest_name = item["Name"]

if highest_name != "None":
    highest_display = f"{highest_name} (Rs{highest_amount})"
else:
    highest_display = "N/A"

col1, col2, col3 = st.columns(3)
with col1:
    st.write("**Total Expenses**")
    st.subheader(f"Rs{total_expenses}")
with col2:
    st.write("**Total Transactions**")
    st.subheader(total_transactions)
with col3:
    st.write("**Highest Expense**")
    st.subheader(highest_display)

st.markdown("---")

filtered_expenses = []

for item in st.session_state.expenses:
    name_match = search_query.lower() in item["Name"].lower()
    
    if selected_category == "All":
        category_match = True
    else:
        category_match = (item["Category"] == selected_category)
        
    amount_match = (item["Amount"] <= max_amount)
    
    if name_match and category_match and amount_match:
        filtered_expenses.append(item)

st.header("Expense Records")

if len(st.session_state.expenses) == 0:
    st.warning("No expenses recorded yet. Please add one above.")
elif len(filtered_expenses) == 0:
    st.warning("No expenses match your search or filter.")
else:
    st.dataframe(filtered_expenses)
    
    st.subheader("Delete Expense")
    for item in filtered_expenses:
        col_a, col_b, col_btn = st.columns([3, 2, 1])
        col_a.write(f"**{item['Name']}** - Rs{item['Amount']}")
        col_b.write(item['Category'])
        
        original_index = st.session_state.expenses.index(item)
        if col_btn.button("Delete", key=f"del_{original_index}"):
            st.session_state.expenses.pop(original_index)
            st.success("Expense deleted successfully!")
            st.rerun()

st.markdown("---")

st.header("Category-wise Summary")

if len(st.session_state.expenses) > 0:
    food_total = 0.0
    travel_total = 0.0
    shopping_total = 0.0
    bills_total = 0.0
    other_total = 0.0
    
    for item in st.session_state.expenses:
        cat = item["Category"]
        if cat == "Food":
            food_total += item["Amount"]
        elif cat == "Travel":
            travel_total += item["Amount"]
        elif cat == "Shopping":
            shopping_total += item["Amount"]
        elif cat == "Bills":
            bills_total += item["Amount"]
        elif cat == "Other":
            other_total += item["Amount"]
            
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.write("**Food**")
        st.subheader(f"Rs{food_total}")
        st.write("**Travel**")
        st.subheader(f"Rs{travel_total}")
        
    with c2:
        st.write("**Shopping**")
        st.subheader(f"Rs{shopping_total}")
        st.write("**Bills**")
        st.subheader(f"Rs{bills_total}")
        
    with c3:
        st.write("**Other**")
        st.subheader(f"Rs{other_total}")
else:
    st.info("Add expenses to view the category summary.")