import streamlit as st   
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
import calendar
from datetime import datetime
import database as db


# st.title("Best Sedans in India")

#/
# with st.sidebar:
  


incomes = ["Salary", "Freelancing", "Teaching" ]
expenses = ["Rent", "Travelling", "Gym", "Diet", "Savings"]
currency = "Rs"
page_title = "Income and Expense Tracker"
page_icon = ":📑:"
layout = "centered"

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)


years = [datetime.today().year, datetime.today().year + 1]
months = list(calendar.month_name[1: ])

# Hide the unnecesary style
hide_st_style = """
           <style>
           footer {visibility: hidden;}
           header {visibility: hidden;}
           </style>
           """

st.markdown(hide_st_style, unsafe_allow_html=True)



# Navigation Menu

selected = option_menu (
      menu_title="Menu",
      options=["Data Entry", "Data Visualization" ],
      icons=["pencil-fill", "bar-chart-line-fill"],
      orientation="horizontal",
    )



# --------input the data -------------
if selected == "Data Entry" :
 st.header(f"Data Entry in {currency}")
with st.form("entry_form", clear_on_submit= True) :
    col1, col2 = st.columns(2)
    col1.selectbox("select Month:", months, key="month")
    col2.selectbox("select Year: ", years, key="year")

    "---"
    with st.expander("Income"):
        for income in incomes:
            st.number_input(f"{income}:", min_value=0, format="%i", step=5, key=income)
    with st.expander("Expenses"):
        for expense in expenses:
            st.number_input(f"{expense}:", min_value=0, format="%i", step=1, key=expense)
            
    "---"

    submitted = st.form_submit_button("Save Data")
    if submitted :
      period = str(st.session_state["year"]) + "_" + str(st.session_state["month"])
      incomes = {income: st.session_state[income] for income in incomes}
      expenses = {expense: st.session_state[expense] for expense in expenses}
      db.insert_period(period, incomes, expenses)
      st.write(f"incomes: {incomes}")
      st.write(f"expenses: {expenses}")
      st.success("Data saved")

st.header ("data Visualization")
with st.form("save_periods") :

    period = st.selectbox("Select Period: ", ["2022_March"])
    submitted = st.form_submit_button("Plot period")
    if submitted :
        comment = "Some Comment"
        incomes = {'Salary': 20, 'Freelancing':2, 'Teaching': 5 }
        expenses = {'Rent': 5, 'Travelling': 2, 'Gym': 5, 'Diet': 1, 'Savings':5 }


        # create matrics
        total_income = sum(incomes.values())
        total_expense = sum(expenses.values())
        remaining_budget = total_income - total_expense
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Income", f"{total_income} {currency}")
        col2.metric("Total Expense ", f"{total_expense} {currency}")
        col3.metric("Remaining budget ", f"{remaining_budget} {currency}")
        st.text(f"Comment: {comment}")

        # Create sankey chart
        label = list(incomes.keys()) + ["Total Income"] + list(expenses.keys())
        source = list(range(len(incomes))) + [len(incomes)] * len(expenses)
        target = [len(incomes)] * len(incomes) + [label.index(expense) for expense in expenses.keys()]
        value = list(incomes.values()) + list(expenses.values())


        link = dict(source=source, target=target, value=value)
        node = dict(label=label, pad=20, thickness=30, color="#E694FF")
        data = go.Sankey(link=link, node=node)

        # Plot it!
        fig = go.Figure(data)
        fig.update_layout(margin=dict(l=0, r=0, t=5, b=5))
        st.plotly_chart(fig, use_container_width=True)





'''  
if selected == "Hatchback" :
    st.title(f"You have selected {selected}")

if selected == "Sedan" :
    st.title(f"You have selected {selected}")

if selected == "SUV" :
    st.title(f"You have selected {selected}")    

if selected == "4X4" :
    st.title(f"You have selected {selected}")   
'''
# st.title("Segment Sedan")