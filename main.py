import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import pickle
import datetime

# Загрузка данных из pickle файла
with open("pulse_data.pickle", "rb") as f:
    data = pickle.load(f)

# Создание приложения Streamlit
st.title("Панель управления пульсом")

# Преобразование даты из строки в datetime
data["date"] = pd.to_datetime(data["date"])

# Выбор диапазона дат
start_date, end_date = st.sidebar.date_input(
    "Выберите диапазон дат:", [data["date"].min(), data["date"].max()]
)
# Преобразование дат из Streamlit к типу datetime64[ns] с учетом временной зоны
start_date = pd.to_datetime(start_date).tz_localize(data["date"].dt.tz)
end_date = pd.to_datetime(end_date).tz_localize(data["date"].dt.tz)
filtered_data = data[(data["date"] >= start_date) & (data["date"] <= end_date)]


# Рассчет статистик
min_pulse = filtered_data["value"].min()
max_pulse = filtered_data["value"].max()
avg_pulse = filtered_data["value"].mean()
measurements_per_day = (
    filtered_data.groupby(filtered_data["date"].dt.date)["value"].count().mean()
)
std_dev = filtered_data["value"].std()

# Нахождение времени максимального и минимального пульса
time_of_max_pulse = filtered_data[filtered_data["value"] == max_pulse]["date"].iloc[0]
time_of_min_pulse = filtered_data[filtered_data["value"] == min_pulse]["date"].iloc[0]
pulse_variability = max_pulse - min_pulse

# Отображение статистик
st.sidebar.markdown(
    f"**Минимальный пульс:** {min_pulse:.2f} уд/мин (Время: {time_of_min_pulse})"
)
st.sidebar.markdown(
    f"**Максимальный пульс:** {max_pulse:.2f} уд/мин (Время: {time_of_max_pulse})"
)
st.sidebar.markdown(f"**Средний пульс:** {avg_pulse:.2f} уд/мин")
st.sidebar.markdown(f"**Измерений в день:** {measurements_per_day:.2f}")
st.sidebar.markdown(f"**Стандартное отклонение:** {std_dev:.2f}")
st.sidebar.markdown(f"**Вариабельность пульса:** {pulse_variability:.2f} уд/мин")

# Рассчет скользящего среднего
window_size = 7
filtered_data["rolling_avg"] = (
    filtered_data["value"].rolling(window_size, min_periods=1).mean()
)

# Визуализация данных
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=filtered_data["date"], y=filtered_data["value"], mode="markers", name="Пульс"
    )
)
fig.add_trace(
    go.Scatter(
        x=filtered_data["date"],
        y=filtered_data["rolling_avg"],
        mode="lines",
        name="Скользящее среднее",
    )
)

fig.update_layout(
    title="Динамика пульса", xaxis_title="Дата и время", yaxis_title="Пульс (уд/мин)"
)

st.plotly_chart(fig)
