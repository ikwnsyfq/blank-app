import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

start_date = datetime(2025, 6, 25)
end_date = datetime(2025, 6, 30)
goal = 3600
initial_count = 2795

date_list = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
date_str_list = [d.strftime("%Y-%m-%d") for d in date_list]

st.title("📦 Parcel Delivery Tracker (June 25–30)")
st.subheader("📝 Enter Parcel Counts")

parcels = {}
for date_str in date_str_list:
    parcels[date_str] = st.number_input(f"{date_str}", min_value=0, value=0, step=1)

running_total = initial_count
remaining_list = []
target_per_day_list = []

for i, date_str in enumerate(date_str_list):
    delivered = parcels[date_str]
    running_total += delivered
    remaining = max(goal - running_total, 0)
    days_left = max(len(date_str_list) - i - 1, 1)
    target_per_day_list.append(remaining // days_left if remaining > 0 else 0)
    remaining_list.append(remaining)

df = pd.DataFrame({
    "Date": date_str_list,
    "Parcels Delivered": list(parcels.values()),
    "Running Total": initial_count + pd.Series(list(parcels.values())).cumsum(),
    "Remaining to 3600": remaining_list,
    "Target per Day Needed": target_per_day_list
})

st.dataframe(df)
st.subheader("📌 Summary")
st.write(f"**Total Delivered:** {running_total}")
st.write(f"**Remaining to Reach 3600:** {max(goal - running_total, 0)}")
