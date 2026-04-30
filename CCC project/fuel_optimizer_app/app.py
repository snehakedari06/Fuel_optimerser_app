import streamlit as st
import pandas as pd
import altair as alt
from core.models import Station
from core.optimizer import fuel_optimizer

st.set_page_config(page_title="Greedy Fuel Optimizer", layout="wide", page_icon="🚗")

st.title("🚗 Greedy Road Trip Fuel Optimizer")

with st.expander("💡 How does the Greedy Algorithm work here?", expanded=False):
    st.markdown("""
    **This application uses a Greedy Algorithm to minimize total fuel cost.**
    At each station, it makes the locally optimal choice without calculating every possible combination. 
    
    **The Greedy Rules:**
    1. **Check Reachability:** Can we reach the destination from here? If yes, buy nothing!
    2. **Look Ahead:** Find the next *cheaper* station within our maximum tank range.
    3. **Cheaper Station Found?** Buy *just enough* fuel to reach that cheaper station. 
    4. **No Cheaper Station Found?** Since this is the cheapest fuel around, fill the tank to the absolute maximum!
    
    By always making these locally optimal "greedy" decisions, the algorithm mathematically guarantees the overall cheapest road trip.
    """)

st.sidebar.header("Trip Configuration")
total_distance = st.sidebar.number_input("Total Trip Distance (km)", min_value=1.0, value=500.0)
tank_capacity = st.sidebar.number_input("Tank Capacity (liters)", min_value=1.0, value=50.0)
start_fuel = st.sidebar.number_input("Starting Fuel (liters)", min_value=0.0, max_value=float(tank_capacity), value=min(10.0, float(tank_capacity)))
mileage = st.sidebar.number_input("Mileage (km/liter)", min_value=0.1, value=15.0)

st.header("Gas Stations along the Route")
if "stations" not in st.session_state:
    st.session_state.stations = []

with st.form("add_station_form"):
    col1, col2 = st.columns(2)
    with col1:
        dist = st.number_input("Distance from start (km)", min_value=0.0, max_value=float(total_distance-0.1), value=0.0)
    with col2:
        price = st.number_input("Fuel Price (Rs./liter)", min_value=0.1, value=100.0)
    
    submitted = st.form_submit_button("Add Station")
    if submitted:
        st.session_state.stations.append({"distance": dist, "price": price})
        st.success(f"Added station at {dist}km with price Rs.{price}/L")

if st.session_state.stations:
    st.subheader("Current Stations")
    df_stations = pd.DataFrame(st.session_state.stations)
    df_stations = df_stations.sort_values(by="distance").reset_index(drop=True)
    
    col_table, col_chart = st.columns([1, 2])
    with col_table:
        st.dataframe(df_stations, use_container_width=True)
        if st.button("Clear All Stations"):
            st.session_state.stations = []
            st.rerun()
            
    with col_chart:
        # Visualizing the stations
        chart = alt.Chart(df_stations).mark_line(point=True, color="#ff4b4b").encode(
            x=alt.X('distance:Q', title="Distance (km)"),
            y=alt.Y('price:Q', title="Price (Rs./L)", scale=alt.Scale(zero=False)),
            tooltip=['distance', 'price']
        ).properties(
            title="Station Prices Over Distance"
        )
        st.altair_chart(chart, use_container_width=True)

st.header("Greedy Optimizer Result")
if st.button("Run Greedy Optimizer", type="primary"):
    if not st.session_state.stations:
        st.warning("Please add at least one gas station.")
    else:
        stations = [Station(distance=s["distance"], price=s["price"]) for s in st.session_state.stations]
        plan, total_cost, error_msg = fuel_optimizer(
            tank_capacity=tank_capacity,
            start_fuel=start_fuel,
            mileage=mileage,
            stations=stations,
            total_distance=total_distance
        )
        
        if error_msg:
            st.error(error_msg)
        else:
            st.success("Optimization Run Complete!")
            
            st.metric("Total Optimal Fuel Cost", f"Rs. {total_cost}")
            
            st.subheader("Step-by-Step Greedy Logic")
            for idx, p in enumerate(plan):
                with st.container():
                    st.markdown(f"### Stop {idx + 1}: Station at {p.location} km")
                    col_stats, col_logic = st.columns([1, 2])
                    with col_stats:
                        st.info(f"**Bought:** {p.liters_bought} L\n\n**Price:** Rs.{p.price}/L\n\n**Cost:** Rs.{p.cost}")
                    with col_logic:
                        st.success(f"**Algorithm Reasoning:**\n{p.reasoning}")
                    st.divider()
            
            # Summary Table
            st.subheader("Purchase Summary")
            plan_data = [{
                "Station #": p.station_num,
                "Location (km)": p.location,
                "Price (Rs./L)": p.price,
                "Liters Bought": p.liters_bought,
                "Cost (Rs.)": p.cost
            } for p in plan]
            st.dataframe(pd.DataFrame(plan_data), use_container_width=True)

