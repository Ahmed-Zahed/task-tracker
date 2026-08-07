import datetime
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Ahmed's Financial Tracker",
    page_icon="💰",
    layout="centered",
)

# Initialize Session State
if "expenses" not in st.session_state:
    st.session_state.expenses = []

if "monthly_budget" not in st.session_state:
    st.session_state.monthly_budget = 5000.0

# Main Title
st.title("💰 Ahmed's Financial Tracker")
st.write(
    "Track your personal expenses easily and monitor where your money goes throughout the month."
)

---

# Sidebar for Settings and Quick Entry
st.sidebar.header("⚙️ Settings & Expense Entry")

# 1. Update Monthly Budget
new_budget = st.sidebar.number_input(
    "Set Monthly Budget:",
    min_value=0.0,
    value=st.session_state.monthly_budget,
    step=100.0,
)
if new_budget != st.session_state.monthly_budget:
    st.session_state.monthly_budget = new_budget
    st.sidebar.success("Budget updated successfully!")

st.sidebar.markdown("---")

# 2. Add Expense Form
st.sidebar.subheader("➕ Add New Expense")
with st.sidebar.form("expense_form"):
    amount = st.number_input("Amount:", min_value=0.0, step=10.0)
    category = st.selectbox(
        "Category:",
        ["Food & Drinks", "Gym & Supplements", "Transportation", "Bills & Utilities", "Entertainment", "Other"],
    )
    date = st.date_input("Date:", datetime.date.today())
    description = st.text_input("Notes (Optional):")

    submit_button = st.form_submit_button(label="Add Expense")

    if submit_button:
        if amount > 0:
            new_expense = {
                "Amount": amount,
                "Category": category,
                "Date": date,
                "Notes": description,
            }
            st.session_state.expenses.append(new_expense)
            st.success("Expense added successfully!")
        else:
            st.error("Please enter a valid amount greater than zero.")

---

# Financial Calculations and Summary
total_expenses = (
    sum([item["Amount"] for item in st.session_state.expenses])
    if st.session_state.expenses
    else 0.0
)
remaining_budget = st.session_state.monthly_budget - total_expenses

# Display Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Monthly Budget", f"{st.session_state.monthly_budget:,.2f}")
col2.metric("Total Expenses", f"{total_expenses:,.2f}")

delta_color = "normal" if remaining_budget >= 0 else "inverse"
col3.metric(
    "Remaining",
    f"{remaining_budget:,.2f}",
    delta=f"{remaining_budget:,.2f}",
    delta_color=delta_color,
)

if remaining_budget < 0:
    st.warning("⚠️ Warning: You have exceeded your monthly budget!")

st.markdown("---")

# Expense Table and Analytics
if st.session_state.expenses:
    df = pd.DataFrame(st.session_state.expenses)

    tab1, tab2 = st.tabs(["📋 Expense History", "📊 Analytics & Charts"])

    with tab1:
        st.subheader("Recorded Expenses")
        st.dataframe(df, use_container_width=True)

        if st.button("🗑️ Clear All Expenses"):
            st.session_state.expenses = []
            st.rerun()

    with tab2:
        st.subheader("Expenses by Category")
        category_df = df.groupby("Category")["Amount"].sum()
        st.bar_chart(category_df)
else:
    st.info("💡 No expenses recorded yet. Start by adding an expense from the sidebar.")