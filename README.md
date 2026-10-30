# 🚗 Greedy Road Trip Fuel Optimizer

A Python-based web application that helps users minimize fuel expenses during a road trip using a **Greedy Algorithm**. Users can enter trip details, add fuel stations with different prices, and generate an optimized fuel-purchasing plan with step-by-step algorithm explanations.

## ✨ Features

- **Trip Configuration:** Set total trip distance, fuel tank capacity, starting fuel, and vehicle mileage.
- **Fuel Station Management:** Add multiple fuel stations with their respective distances and fuel prices.
- **Price Visualization:** View fuel prices across different stations using interactive charts.
- **Greedy Optimization:** Find an optimized fuel-purchasing strategy based on station prices and reachability.
- **Step-by-Step Explanation:** Understand why the algorithm chooses to buy fuel at each station.
- **Cost Analysis:** View total estimated fuel expenses and a detailed purchase summary.
- **Input Validation:** Detect situations where the trip cannot be completed due to insufficient fuel range.

## 🛠️ Tech Stack

- **Programming Language:** Python
- **Frontend:** Streamlit
- **Data Processing:** Pandas
- **Data Visualization:** Altair
- **Algorithm:** Greedy Algorithm
- **Concepts:** Data Structures and Algorithm Design

## ⚙️ How It Works

The application uses a Greedy Algorithm to make fuel-purchasing decisions at each station.

### Greedy Strategy

1. Check whether the current fuel is sufficient to reach the destination. If yes, skip purchasing fuel.
2. Identify fuel stations that are reachable within the maximum tank range.
3. Search for the nearest station offering a lower fuel price.
4. If a cheaper station is available, purchase only enough fuel to reach it.
5. If no cheaper station is reachable, fill the tank to its maximum capacity.
6. Calculate the fuel purchase cost and update the remaining fuel.

The application displays the decisions and reasoning behind each purchase.

## 📂 Project Structure

```text
fuel_optimizer_app/
│
├── app.py
│
├── core/
│   ├── __init__.py
│   ├── models.py
│   └── optimizer.py
│
└── requirements.txt
```

### File Description

- `app.py` – Streamlit interface, trip configuration, station management, charts, and optimization results.
- `core/models.py` – Defines the Station and PurchasePlan data models.
- `core/optimizer.py` – Implements the Greedy fuel optimization logic.
- `requirements.txt` – Contains project dependencies.

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone <your-repository-url>
```

### 2. Navigate to the Project Directory

```bash
cd fuel_optimizer_app
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
```

The application will open in your default browser.

## 📊 Example Inputs

| Parameter | Example Value |
|---|---:|
| Total Trip Distance | 500 km |
| Tank Capacity | 50 L |
| Starting Fuel | 10 L |
| Mileage | 15 km/L |
| Fuel Station Price | ₹100/L |

Users can add multiple stations at different distances and prices to generate an optimized purchase plan.

## 🎯 Learning Outcomes

- Practical implementation of the Greedy Algorithm.
- Understanding local optimization and decision-making.
- Applying algorithmic concepts to a real-world transportation problem.
- Working with Python data models and modular programming.
- Building interactive data-driven applications using Streamlit.

## 👩‍💻 Author

**Sneha Kedari**

GitHub: [@snehakedari06](https://github.com/snehakedari06)

---

*An academic project demonstrating the practical application of Greedy Algorithms to fuel-cost optimization.*
