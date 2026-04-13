# 🏏 T20 World Cup 2024 Analytics Dashboard

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?logo=pandas&logoColor=white)

An interactive, data-driven web application built with Streamlit and Pandas that provides deep insights into the T20 World Cup. This dashboard analyzes over 50,000 data points to visualize team performances, evaluate player impact, and algorithmically generate the optimal "Best XI" tournament team.

## ✨ Features

- **Batting & Bowling Analysis:** Deep dives into strike rates, economy, phase-wise performance (Powerplay, Middle, Death overs), and run distributions.
- **MVP Tracking:** Objective scoring systems to rank the Most Valuable Players per team based on a composite score of batting impact and bowling efficiency.
- **Algorithmic 'Best XI' Selector:** Automatically constructs the optimal tournament team using custom logic balancing openers, middle-order batters, all-rounders, and bowlers, while respecting team-limit constraints.
- **Advanced Visualizations:** Interactive plots covering run trajectories, dismissal types, and player matchups.

## 📸 Dashboard Previews

### Batting Insights
![Batting Analysis](https://github.com/user-attachments/assets/c56c6584-9f6b-424e-b548-9635fa82caf0)
*Phase-wise run accumulation and strike rate analysis.*

<br>

### Best XI Selector
![Best XI Selector](https://github.com/user-attachments/assets/79302bec-c4f8-4808-8a67-72ab5263508d)
*Algorithmic generation of the tournament's optimal team.*

## 🏗️ Technical Architecture

The project is built with modularity in mind, separating data processing pipelines from the frontend application components:

```text
├── app.py                      # Main Streamlit application entry point
├── data/                       # Raw and cleaned CSV datasets
├── modules/                    # Distinct analytical modules 
│   ├── batting_analysis.py
│   ├── bowling_analysis.py
│   ├── mvp_analysis.py
│   └── best_xi_selector.py
├── utils/
│   └── data_cleaning.py        # Data preprocessing and feature engineering script
└── requirements.txt            # Project dependencies



## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.9+ installed.

### Installation

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/yourusername/T20-World-Cup-Analysis.git](https://github.com/yourusername/T20-World-Cup-Analysis.git)
    cd T20-World-Cup-Analysis
    ```

2.  **Create a Virtual Environment (Recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Prepare the Data:**
    Run the cleaning utility to format the raw data and engineer necessary features (like phase categorization).

    ```bash
    python utils/data_cleaning.py
    ```

5.  **Launch the Dashboard:**

    ```bash
    streamlit run app.py
    ```

## 🧠 Core Logic Highlight: Best XI Algorithm

The `Best XI Selector` doesn't just pick the top run-scorers. It calculates a composite `all_round_score`, limits selections to a maximum of 4 players per real-world team, and explicitly fills designated roles (2 Openers, 3 Middle Order, 2 All-Rounders, 4 Bowlers) to create a realistic, balanced cricket squad.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome\! Feel free to check the [issues page](https://www.google.com/search?q=https://github.com/yourusername/T20-World-Cup-Analysis/issues).

```
```
