import streamlit as st
import pandas as pd
import json
from pathlib import Path
from datetime import date, datetime, timedelta


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Continental | Travel Reimbursement",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CONTINENTAL STYLE
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', Arial, sans-serif;
}

.stApp {
    background: #F3F4F5;
    color: #171717;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.4rem;
    padding-bottom: 3rem;
}


/* HEADER */

.conti-header {
    background: #171717;
    border-radius: 16px;
    padding: 30px 34px;
    margin-bottom: 22px;
    border-left: 8px solid #FFD000;
    box-shadow: 0 6px 18px rgba(0,0,0,0.12);
}

.conti-header h1 {
    margin: 0;
    color: #FFD000 !important;
    font-size: 31px;
    font-weight: 800;
}

.conti-header p {
    margin: 8px 0 0 0;
    color: #DADADA !important;
    font-size: 14px;
}


/* SECTION */

.section-title {
    display: flex;
    align-items: center;
    background: #FFFFFF;
    color: #171717 !important;
    border-left: 6px solid #FFD000;
    border-radius: 9px;
    padding: 13px 17px;
    margin: 24px 0 14px 0;
    font-size: 16px;
    font-weight: 800;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}


/* CARDS */

.info-card {
    background: #FFFFFF;
    border: 1px solid #D8D8D8;
    border-radius: 10px;
    padding: 15px 18px;
    margin: 8px 0;
    box-shadow: 0 2px 7px rgba(0,0,0,0.04);
}

.yellow-card {
    background: #FFF8D6;
    border: 1px solid #E0C200;
    border-left: 5px solid #FFD000;
    border-radius: 10px;
    padding: 15px 18px;
    margin: 8px 0 15px 0;
}


/* RATE */

.rate-card {
    background: #171717;
    border-radius: 12px;
    padding: 19px 22px;
    margin: 4px 0 15px 0;
    border-left: 5px solid #FFD000;
    box-shadow: 0 5px 13px rgba(0,0,0,0.12);
}

.rate-label {
    color: #BDBDBD !important;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.rate-value {
    color: #FFD000 !important;
    font-size: 25px;
    font-weight: 800;
}


/* EXPENSE */

.expense-card {
    background: #FFFFFF;
    border: 1px solid #D9D9D9;
    border-radius: 11px;
    padding: 15px 17px;
    margin: 12px 0 4px 0;
    box-shadow: 0 2px 7px rgba(0,0,0,0.04);
}

.expense-title {
    font-size: 13px;
    font-weight: 800;
    color: #171717 !important;
}


/* TOTAL */

.total-card {
    background: #171717;
    border: 2px solid #FFD000;
    border-radius: 15px;
    padding: 23px;
    margin: 16px 0;
    text-align: center;
    box-shadow: 0 6px 16px rgba(0,0,0,0.13);
}

.total-card h2 {
    margin: 0;
    color: #FFFFFF !important;
    font-size: 15px;
}

.total-card h1 {
    margin: 8px 0 0 0;
    color: #FFD000 !important;
    font-size: 34px;
    font-weight: 800;
}

.total-card p {
    margin: 7px 0 0 0;
    color: #CFCFCF !important;
    font-size: 12px;
}


/* INPUTS */

.stTextInput input,
.stNumberInput input,
.stDateInput input {
    border-radius: 7px !important;
    border: 1px solid #CCCCCC !important;
    background: #FFFFFF !important;
    color: #171717 !important;
}

.stSelectbox div[data-baseweb="select"] {
    border-radius: 7px !important;
    background: #FFFFFF !important;
}

.stTextInput input:focus,
.stNumberInput input:focus,
.stDateInput input:focus {
    border-color: #FFD000 !important;
    box-shadow: 0 0 0 1px #FFD000 !important;
}

label {
    font-weight: 600 !important;
    color: #292929 !important;
}


/* NUMBER INPUT BUTTONS */

div[data-testid="stNumberInput"] button {
    background: #FFFFFF !important;
    color: #171717 !important;
    border-left: 1px solid #CCCCCC !important;
}

div[data-testid="stNumberInput"] button:hover {
    background: #FFD000 !important;
    color: #171717 !important;
}


/* BUTTONS */

.stButton > button {
    background: #171717 !important;
    color: #FFD000 !important;
    border: 1px solid #171717 !important;
    border-radius: 7px !important;
    min-height: 42px;
    font-weight: 700 !important;
}

.stButton > button:hover {
    background: #FFD000 !important;
    color: #171717 !important;
    border: 1px solid #171717 !important;
}


/* EXPANDER */

.streamlit-expanderHeader {
    background: #FFFFFF !important;
    border: 1px solid #D8D8D8 !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
}


/* DATAFRAME */

[data-testid="stDataFrame"] {
    border: 1px solid #D8D8D8;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}


/* FOOTER */

.footer {
    text-align: center;
    padding: 28px 10px 10px 10px;
    margin-top: 40px;
    border-top: 1px solid #D5D5D5;
    color: #777777 !important;
    font-size: 12px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# FILE
# ============================================================

BASE = Path(__file__).parent
EMPLOYEE_FILE = BASE / "employees.json"


# ============================================================
# EMPLOYEES
# ============================================================

DEFAULT_EMPLOYEES = {
    "Select Employee": {
        "epf": "",
        "department": ""
    },
    "Piyumika Perera": {
        "epf": "EMP001",
        "department": "Finance"
    },
    "Employee 2": {
        "epf": "EMP002",
        "department": "Finance"
    }
}


def load_employees():

    try:

        if EMPLOYEE_FILE.exists():

            with open(
                EMPLOYEE_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

                if isinstance(data, dict):
                    return data

    except Exception:
        pass

    return DEFAULT_EMPLOYEES.copy()


def save_employees(data):

    with open(
        EMPLOYEE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2
        )


def money(value):

    return f"{float(value):,.2f}"


# ============================================================
# COUNTRY / CURRENCY
# ============================================================

COUNTRY_CURRENCY = {
    "Sri Lanka": "LKR",
    "Germany": "EUR",
    "France": "EUR",
    "Italy": "EUR",
    "United Kingdom": "GBP",
    "United States": "USD",
    "Japan": "JPY",
    "United Arab Emirates": "AED",
    "Singapore": "SGD",
    "India": "INR"
}


# ============================================================
# DEFAULT EXCHANGE RATES
# ============================================================

DEFAULT_RATES = {
    "LKR": 1.00,
    "USD": 331.02,
    "EUR": 390.00,
    "GBP": 450.00,
    "JPY": 2.20,
    "AED": 90.00,
    "SGD": 260.00,
    "INR": 3.95
}


# ============================================================
# TIME OPTIONS
# ============================================================

TIME_OPTIONS = [
    f"{hour:02d}:{minute:02d}"
    for hour in range(24)
    for minute in (0, 30)
]


def time_from_string(value):

    return datetime.strptime(
        value,
        "%H:%M"
    ).time()


def mins(t):

    return t.hour * 60 + t.minute


# ============================================================
# MEAL CALCULATION
# ============================================================

def calculate_meals(
    departure_date,
    departure_time,
    arrival_date,
    arrival_time
):

    result = []

    current_date = departure_date

    while current_date <= arrival_date:

        if (
            current_date == departure_date
            and current_date == arrival_date
        ):

            breakfast = mins(departure_time) < 480

            lunch = (
                mins(departure_time) < 780
                and mins(arrival_time) >= 720
            )

            dinner = mins(arrival_time) >= 1080

        elif current_date == departure_date:

            breakfast = mins(departure_time) < 480
            lunch = mins(departure_time) < 780
            dinner = mins(departure_time) < 1080

        elif current_date == arrival_date:

            breakfast = True
            lunch = mins(arrival_time) >= 720
            dinner = mins(arrival_time) >= 1080

        else:

            breakfast = True
            lunch = True
            dinner = True

        result.append(
            (
                current_date,
                breakfast,
                lunch,
                dinner
            )
        )

        current_date += timedelta(days=1)

    return result


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="conti-header">

    <h1>Continental | Travel Reimbursement</h1>

    <p>
        Employee Travel • Meal Allowance • Expense Management
    </p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# EMPLOYEE DETAILS
# ============================================================

st.markdown(
    '<div class="section-title">👤 Employee Details</div>',
    unsafe_allow_html=True
)


with st.expander("➕ Register New Employee"):

    c1, c2, c3 = st.columns(3)

    new_name = c1.text_input(
        "Employee Name",
        key="new_employee_name"
    )

    new_epf = c2.text_input(
        "EPF Number",
        key="new_employee_epf"
    )

    new_department = c3.text_input(
        "Department",
        key="new_employee_department"
    )

    if st.button(
        "Save Employee",
        key="save_employee"
    ):

        employees = load_employees()

        if not new_name.strip():

            st.error(
                "Please enter the employee name."
            )

        elif new_name in employees:

            st.warning(
                "This employee already exists."
            )

        else:

            employees[new_name] = {
                "epf": new_epf,
                "department": new_department
            }

            save_employees(employees)

            st.success(
                "Employee added successfully."
            )

            st.rerun()


employees = load_employees()


employee = st.selectbox(
    "Employee Name",
    list(employees.keys()),
    key="employee_select"
)


# ============================================================
# REMOVE EMPLOYEE
# ============================================================

if "confirm_remove_employee" not in st.session_state:

    st.session_state.confirm_remove_employee = False


if employee != "Select Employee":

    if st.button(
        "✕ Remove Employee",
        key="remove_employee"
    ):

        st.session_state.confirm_remove_employee = True


if (
    st.session_state.confirm_remove_employee
    and employee != "Select Employee"
):

    st.warning(
        f"Are you sure you want to remove **{employee}**?"
    )

    c1, c2 = st.columns(2)

    with c1:

        if st.button(
            "Yes, Remove",
            key="yes_remove_employee"
        ):

            employee_to_remove = employee

            employees = load_employees()

            if employee_to_remove in employees:

                del employees[employee_to_remove]

                save_employees(employees)

            st.session_state.confirm_remove_employee = False

            st.rerun()

    with c2:

        if st.button(
            "Cancel",
            key="cancel_remove_employee"
        ):

            st.session_state.confirm_remove_employee = False

            st.rerun()


employee_info = employees.get(
    employee,
    {
        "epf": "",
        "department": ""
    }
)


c1, c2 = st.columns(2)


c1.text_input(
    "EPF Number",
    value=employee_info.get(
        "epf",
        ""
    ),
    disabled=True
)


c2.text_input(
    "Department",
    value=employee_info.get(
        "department",
        ""
    ),
    disabled=True
)


# ============================================================
# TRAVEL DETAILS
# ============================================================

st.markdown(
    '<div class="section-title">✈️ Travel Details</div>',
    unsafe_allow_html=True
)


c1, c2 = st.columns(2)


country = c1.selectbox(
    "Travel Country",
    list(COUNTRY_CURRENCY.keys()),
    key="travel_country"
)


travel_reason = c2.text_input(
    "Travel Reason",
    key="travel_reason"
)


currency = COUNTRY_CURRENCY[country]


# ============================================================
# DEPARTURE / ARRIVAL
# ============================================================

st.markdown(
    '<div class="section-title">📅 Departure & Arrival</div>',
    unsafe_allow_html=True
)


c1, c2 = st.columns(2)


departure_date = c1.date_input(
    "Departure Date",
    value=date.today(),
    key="departure_date"
)


departure_time_text = c1.selectbox(
    "Departure Time",
    TIME_OPTIONS,
    index=14,
    key="departure_time"
)


arrival_date = c2.date_input(
    "Arrival Date",
    value=date.today(),
    key="arrival_date"
)


arrival_time_text = c2.selectbox(
    "Arrival Time",
    TIME_OPTIONS,
    index=34,
    key="arrival_time"
)


departure_time = time_from_string(
    departure_time_text
)


arrival_time = time_from_string(
    arrival_time_text
)


valid_travel = True


if arrival_date < departure_date:

    st.error(
        "Arrival Date cannot be earlier than Departure Date."
    )

    valid_travel = False


elif (
    arrival_date == departure_date
    and arrival_time <= departure_time
):

    st.error(
        "Arrival Time must be later than Departure Time."
    )

    valid_travel = False


# ============================================================
# EXCHANGE RATE
# ============================================================

st.markdown(
    '<div class="section-title">💱 Exchange Rate</div>',
    unsafe_allow_html=True
)


if currency == "LKR":

    rate = 1.00

    st.markdown(
        """
        <div class="rate-card">

            <div class="rate-label">
                Exchange Rate
            </div>

            <div class="rate-value">
                1 LKR = LKR 1.00
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

else:

    rate_key = f"exchange_rate_{currency}"

    if rate_key not in st.session_state:

        st.session_state[rate_key] = (
            DEFAULT_RATES[currency]
        )


    rate = st.number_input(
        f"1 {currency} = LKR",
        min_value=0.0001,
        value=float(
            st.session_state[rate_key]
        ),
        step=0.01,
        format="%.2f",
        key=rate_key
    )


    st.markdown(
        f"""
        <div class="rate-card">

            <div class="rate-label">
                Exchange Rate
            </div>

            <div class="rate-value">
                1 {currency} = LKR {money(rate)}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DAILY MEAL ALLOWANCE
# ============================================================

st.markdown(
    '<div class="section-title">🍽️ Daily Meal Allowance</div>',
    unsafe_allow_html=True
)


c1, c2, c3 = st.columns(3)


breakfast_rate = c1.number_input(
    "Breakfast Rate",
    min_value=0.0,
    value=0.0,
    step=0.01,
    format="%.2f",
    key="breakfast_rate"
)


lunch_rate = c2.number_input(
    "Lunch Rate",
    min_value=0.0,
    value=0.0,
    step=0.01,
    format="%.2f",
    key="lunch_rate"
)


dinner_rate = c3.number_input(
    "Dinner Rate",
    min_value=0.0,
    value=0.0,
    step=0.01,
    format="%.2f",
    key="dinner_rate"
)


meal_total = 0.0


if valid_travel:

    meal_days = calculate_meals(
        departure_date,
        departure_time,
        arrival_date,
        arrival_time
    )


    for i, (
        travel_day,
        breakfast_allowed,
        lunch_allowed,
        dinner_allowed
    ) in enumerate(meal_days):

        c1, c2, c3, c4, c5 = st.columns(
            [2, 1.3, 1.3, 1.3, 1.5]
        )


        c1.markdown(
            f"""
            <div style="
                padding-top:8px;
                font-weight:700;
            ">
                {travel_day.strftime("%d %b %Y")}
            </div>
            """,
            unsafe_allow_html=True
        )


        breakfast = c2.checkbox(
            "Breakfast",
            value=breakfast_allowed,
            key=f"breakfast_{i}"
        )


        lunch = c3.checkbox(
            "Lunch",
            value=lunch_allowed,
            key=f"lunch_{i}"
        )


        dinner = c4.checkbox(
            "Dinner",
            value=dinner_allowed,
            key=f"dinner_{i}"
        )


        day_total = 0.0


        if breakfast:
            day_total += breakfast_rate


        if lunch:
            day_total += lunch_rate


        if dinner:
            day_total += dinner_rate


        meal_total += day_total


        c5.markdown(
            f"""
            <div style="
                padding-top:8px;
                font-weight:700;
                text-align:right;
            ">
                {currency} {money(day_total)}
            </div>
            """,
            unsafe_allow_html=True
        )


meal_lkr = meal_total * rate


st.markdown(
    f"""
    <div class="info-card">

        <b>Total Meal Allowance</b>

        <span style="float:right;">
            <b>{currency} {money(meal_total)}</b>
            &nbsp;&nbsp;→&nbsp;&nbsp;
            <b>LKR {money(meal_lkr)}</b>
        </span>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TRANSPORT
# ============================================================

st.markdown(
    '<div class="section-title">🚕 Transport Expenses</div>',
    unsafe_allow_html=True
)


c1, c2, c3, c4 = st.columns(4)


taxi = c1.number_input(
    f"Taxi ({currency})",
    min_value=0.0,
    value=0.0,
    step=0.01,
    format="%.2f",
    key="taxi_expense"
)


train = c2.number_input(
    f"Train ({currency})",
    min_value=0.0,
    value=0.0,
    step=0.01,
    format="%.2f",
    key="train_expense"
)


bus = c3.number_input(
    f"Bus ({currency})",
    min_value=0.0,
    value=0.0,
    step=0.01,
    format="%.2f",
    key="bus_expense"
)


other_transport = c4.number_input(
    f"Other Transport ({currency})",
    min_value=0.0,
    value=0.0,
    step=0.01,
    format="%.2f",
    key="other_transport_expense"
)


transport_total = (
    taxi
    + train
    + bus
    + other_transport
)


transport_lkr = transport_total * rate


st.markdown(
    f"""
    <div class="info-card">

        <b>Transport Total</b>

        <span style="float:right;">
            <b>{currency} {money(transport_total)}</b>
            &nbsp;&nbsp;→&nbsp;&nbsp;
            <b>LKR {money(transport_lkr)}</b>
        </span>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HOTEL
# ============================================================

st.markdown(
    '<div class="section-title">🏨 Hotel Expenses</div>',
    unsafe_allow_html=True
)


hotel = st.number_input(
    f"Hotel Expense ({currency})",
    min_value=0.0,
    value=0.0,
    step=0.01,
    format="%.2f",
    key="hotel_expense"
)


hotel_lkr = hotel * rate


st.markdown(
    f"""
    <div class="info-card">

        <b>Hotel Total</b>

        <span style="float:right;">
            <b>{currency} {money(hotel)}</b>
            &nbsp;&nbsp;→&nbsp;&nbsp;
            <b>LKR {money(hotel_lkr)}</b>
        </span>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# OTHER EXPENSES
# ============================================================

st.markdown(
    '<div class="section-title">🧾 Other Expenses</div>',
    unsafe_allow_html=True
)


if "other_rows" not in st.session_state:

    st.session_state.other_rows = []


# ============================================================
# EXPENSE ROWS
# ============================================================

for i, row in enumerate(
    st.session_state.other_rows
):

    st.markdown(
        f"""
        <div class="expense-card">

            <div class="expense-title">
                EXPENSE {i + 1}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    c1, c2, c3, c4 = st.columns(
        [1.2, 3, 1.5, 1.3]
    )


    row["date"] = c1.date_input(
        "Date",
        value=row["date"],
        key=f"other_date_{i}"
    )


    row["description"] = c2.text_input(
        "Description",
        value=row["description"],
        key=f"other_description_{i}"
    )


    row["amount"] = c3.number_input(
        f"Amount ({currency})",
        min_value=0.0,
        value=float(row["amount"]),
        step=0.01,
        format="%.2f",
        key=f"other_amount_{i}"
    )


    if c4.button(
        "🗑 Remove",
        key=f"remove_other_{i}"
    ):

        st.session_state.other_rows.pop(i)

        st.rerun()


# ============================================================
# ADD EXPENSE
# ============================================================

if st.button(
    "➕ Add Expense",
    key="add_other_expense"
):

    st.session_state.other_rows.append(
        {
            "date": date.today(),
            "description": "",
            "amount": 0.0
        }
    )

    st.rerun()


other_total = sum(
    float(row["amount"])
    for row in st.session_state.other_rows
)


other_lkr = other_total * rate


if other_total > 0:

    st.markdown(
        f"""
        <div class="info-card">

            <b>Other Expenses Total</b>

            <span style="float:right;">
                <b>{currency} {money(other_total)}</b>
                &nbsp;&nbsp;→&nbsp;&nbsp;
                <b>LKR {money(other_lkr)}</b>
            </span>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# CONTINENTAL PAID EXPENSES
# ============================================================

st.markdown(
    '<div class="section-title">🏢 Other Expenses Paid by Continental</div>',
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="info-card">

        These expenses are paid directly by Continental
        and are not included in the employee reimbursement.

    </div>
    """,
    unsafe_allow_html=True
)


company_expenses = []


for label, key in [
    ("Flight Ticket", "flight"),
    ("Visa Service", "visa"),
    ("Travel Allowance", "travel_allowance")
]:

    c1, c2 = st.columns([1.5, 2.5])


    paid = c1.selectbox(
        f"{label} Paid by Continental?",
        ["No", "Yes"],
        key=f"{key}_paid"
    )


    amount = c2.number_input(
        f"{label} Amount (LKR)",
        min_value=0.0,
        value=0.0,
        step=0.01,
        format="%.2f",
        key=f"{key}_amount"
    )


    if paid == "No":

        amount = 0.0


    company_expenses.append(
        {
            "expense": label,
            "paid": paid,
            "amount": amount
        }
    )


company_total_lkr = sum(
    item["amount"]
    for item in company_expenses
)


st.markdown(
    f"""
    <div class="info-card">

        <b>Total Paid by Continental</b>

        <span style="float:right;">
            <b>LKR {money(company_total_lkr)}</b>
        </span>

        <br><br>

        <small>
            Excluded from employee Net Amount Payable.
        </small>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FINAL CLAIM
# ============================================================

claim_lkr = (
    meal_lkr
    + transport_lkr
    + hotel_lkr
    + other_lkr
)


# ============================================================
# FINAL CLAIM SUMMARY
# ============================================================

st.markdown(
    '<div class="section-title">💰 Final Claim Summary</div>',
    unsafe_allow_html=True
)


st.markdown(
    f"""
    <div class="total-card">

        <h2>
            TOTAL CLAIMABLE EMPLOYEE EXPENSES
        </h2>

        <h1>
            LKR {money(claim_lkr)}
        </h1>

        <p>
            Continental-paid expenses are excluded.
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ADVANCE / SETTLEMENT
# ============================================================

st.markdown(
    '<div class="section-title">💵 Advance & Settlement</div>',
    unsafe_allow_html=True
)


c1, c2 = st.columns(2)


advance = c1.number_input(
    "Advance Given to Employee (LKR)",
    min_value=0.0,
    value=0.0,
    step=0.01,
    format="%.2f",
    key="advance_lkr"
)


returned_cash = c2.number_input(
    "Returned Cash (LKR)",
    min_value=0.0,
    value=0.0,
    step=0.01,
    format="%.2f",
    key="returned_cash_lkr"
)


net_amount = (
    claim_lkr
    - advance
    - returned_cash
)


# ============================================================
# NET RESULT
# ============================================================

if net_amount > 0:

    st.markdown(
        f"""
        <div class="total-card">

            <h2>
                NET AMOUNT PAYABLE TO EMPLOYEE
            </h2>

            <h1>
                LKR {money(net_amount)}
            </h1>

        </div>
        """,
        unsafe_allow_html=True
    )


elif net_amount < 0:

    st.markdown(
        f"""
        <div class="total-card">

            <h2>
                AMOUNT TO BE RETURNED TO COMPANY
            </h2>

            <h1>
                LKR {money(abs(net_amount))}
            </h1>

        </div>
        """,
        unsafe_allow_html=True
    )


else:

    st.markdown(
        """
        <div class="total-card">

            <h2>
                NET AMOUNT PAYABLE
            </h2>

            <h1>
                LKR 0.00
            </h1>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# EXPENSE BREAKDOWN
# ============================================================

st.markdown(
    '<div class="section-title">📊 Expense Breakdown</div>',
    unsafe_allow_html=True
)


breakdown = pd.DataFrame(
    {
        "Expense Category": [
            "Meal Allowance",
            "Transport",
            "Hotel",
            "Other Expenses"
        ],

        f"Amount ({currency})": [
            meal_total,
            transport_total,
            hotel,
            other_total
        ],

        "LKR Equivalent": [
            meal_lkr,
            transport_lkr,
            hotel_lkr,
            other_lkr
        ]
    }
)


st.dataframe(
    breakdown,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# CONTINENTAL PAID BREAKDOWN
# ============================================================

st.markdown(
    '<div class="section-title">🏢 Continental-Paid Breakdown</div>',
    unsafe_allow_html=True
)


company_breakdown = pd.DataFrame(
    {
        "Expense": [
            item["expense"]
            for item in company_expenses
        ],

        "Paid by Continental": [
            item["paid"]
            for item in company_expenses
        ],

        "Amount (LKR)": [
            item["amount"]
            for item in company_expenses
        ]
    }
)


st.dataframe(
    company_breakdown,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        <b>Continental | Travel Reimbursement System</b>

        <br>

        Finance Department

    </div>
    """,
    unsafe_allow_html=True
)
