# 🗺️ U.S. Income Heatmap Explorer

This interactive Streamlit app allows users to explore **median household income** data across U.S. states and counties from **1989 to 2015**, along with the dominant **income source** and a vibe-based **quote** for each state.

Created as part of **Assignment 3** for **AGEN 892** by **Ishrat Jandu**, this project visualizes economic data geographically to provide an engaging and informative experience.

---

## 📌 Features

- **State-wise and county-wise median income visualization**
- **Vibrant choropleth heatmap** (red = low income, green = high income)
- Quotes capturing the **"vibe"** of each state based on its primary income source
- Embedded tooltips for easy interpretation
- Responsive layout using Streamlit and Folium

---

## 🖥️ Demo

▶️ Live Website: [https://<your-streamlit-app-url>](https://<your-streamlit-app-url>)

📁 GitHub Repo: [https://github.com/<your-username>/<your-repo-name>](https://github.com/<your-username>/<your-repo-name>)

> **Note**: Replace these links with your actual deployment URL and repo URL.

---

## 📂 Files

- `app.py`: Main Streamlit application script
- `requirements.txt`: Python dependencies for running the app on Streamlit Cloud

---

## 📈 Data Sources

- 📊 Income Data: [https://raw.githubusercontent.com/pri-data/50-states/master/data/income-counties-states-national.csv](https://raw.githubusercontent.com/pri-data/50-states/master/data/income-counties-states-national.csv)
- 🌐 State GeoJSON: [https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_states.json](https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_states.json)
- 🧾 State Abbreviations: [https://gist.githubusercontent.com/tvpmb/4734703/raw/...](https://gist.githubusercontent.com/tvpmb/4734703/raw/...)

---

## 🚀 Run Locally

1. Clone this repository:
   ```bash
   git clone https://github.com/<your-username>/<your-repo-name>.git
   cd <your-repo-name>
