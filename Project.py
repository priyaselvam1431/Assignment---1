# 1. Total requests: distinct request identifiers in the filtered data.

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("UrbanPulse NYC_311")
st.header("Total Distinct Request Analysis.")

df = pd.read_csv(r"C:\Users\ADMIN\Downloads\nyc311_row_sample .csv")

total = df["unique_key"].nunique()
st.metric("Total Requests", total)
borough = df.groupby("borough")["unique_key"].nunique()

st.subheader("Total Requests by Borough")

fig, ax = plt.subplots()

borough.plot(kind="bar", ax=ax)

ax.set_xlabel("Borough")
ax.set_ylabel("Total Requests")
ax.set_title("Requests by Borough")

st.pyplot(fig)

st.subheader("Borough-wise Summary")
st.dataframe(borough.reset_index(name="Total Requests"))



# 2. Recorded closure: share of filtered rows marked closed.

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("UrbanPulse NYC_311")
st.header("Recorded closure: share of filtered rows marked closed.")

df = pd.read_csv(r"C:\Users\ADMIN\Downloads\nyc311_row_sample .csv")

closed = (df["status"].str.lower() == "closed").sum()
total = df["status"].notna().sum()
open_requests = total - closed

closure_rate = (closed / total * 100) if total > 0 else 0

col1, col2, col3 = st.columns(3)

col1.metric("Total Requests", total)
col2.metric("Closed Requests", closed)
col3.metric("Closure Rate", f"{closure_rate:.2f}%")

st.subheader("Closed vs Open Requests")

fig, ax = plt.subplots()

ax.pie(
    [closed, open_requests],
    labels=["Closed", "Open"],
    autopct="%1.1f%%"
)

st.pyplot(fig)


# 3. Open requests: filtered rows not marked closed

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("UrbanPulse NYC_311")
st.header("Open requests: filtered rows not marked closed.")

df = pd.read_csv(r"C:\Users\ADMIN\Downloads\nyc311_row_sample .csv")

closed = (df["status"].str.lower() == "closed").sum()
total = df["status"].notna().sum()
open_requests = total - closed

st.metric("Total Requests", total)
st.metric("Open Requests", open_requests)

fig, ax = plt.subplots()

ax.bar(["Open", "Closed"], [open_requests, closed])
ax.set_ylabel("Number of Requests")
ax.set_title("Open Requests Comparison")

st.pyplot(fig)


# 4. Median resolution: median valid resolution duration, in hours.


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("UrbanPulse NYC_311")
st.header("Median resolution: median valid resolution duration, in hours.")

df = pd.read_csv(r"C:\Users\ADMIN\Downloads\nyc311_row_sample .csv")

df["created_date"] = pd.to_datetime(df["created_date"])
df["closed_date"] = pd.to_datetime(df["closed_date"])

df["resolution_hours"] = (
    df["closed_date"] - df["created_date"]
).dt.total_seconds() / 3600

median_hours = df["resolution_hours"].median()
st.metric("Median Resolution Time", f"{median_hours:.2f} Hours")

st.subheader("Resolution Time Visualization")

fig, ax = plt.subplots()

ax.bar(
    ["Median Resolution"],
    [median_hours]
)

ax.set_ylabel("Hours")
ax.set_title("Median Resolution Duration")

st.pyplot(fig)

st.write("Median Resolution:", round(median_hours, 2), "Hours")

# 5. Over 72 hours: share of valid resolution durations exceeding the project’s illustrative 72-hour threshold.


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("UrbanPulse NYC_311")
st.header("Over 72 hours: share of valid resolution durations exceeding the project’s illustrative 72-hour threshold.")

df = pd.read_csv(r"C:\Users\ADMIN\Downloads\nyc311_row_sample .csv")

df["created_date"] = pd.to_datetime(df["created_date"], errors="coerce")
df["closed_date"] = pd.to_datetime(df["closed_date"], errors="coerce")
hours = (df["closed_date"] - df["created_date"]).dt.total_seconds() / 3600
hours = hours.dropna()
hours = hours[hours >= 0]

over_72 = (hours > 72).sum()
within_72 = (hours <= 72).sum()

percentage = (over_72 / len(hours) * 100) if len(hours) > 0 else 0

st.metric("Over 72 Hours", f"{percentage:.2f}%")

fig, ax = plt.subplots()

ax.pie(
    [over_72, within_72],
    labels=["Over 72 Hours", "Within 72 Hours"],
    autopct="%1.1f%%"
)

st.pyplot(fig)
