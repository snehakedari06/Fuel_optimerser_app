from typing import List, Tuple
from .models import Station, PurchasePlan

def fuel_optimizer(
    tank_capacity: float,
    start_fuel: float,
    mileage: float,
    stations: List[Station],
    total_distance: float
) -> Tuple[List[PurchasePlan], float, str]:
    # sort stations by distance
    stations = sorted(stations, key=lambda s: s.distance)
    # add destination as a station with 0 price
    stations.append(Station(distance=total_distance, price=0.0))
    
    current_fuel = start_fuel
    total_cost = 0.0
    plan = []
    
    for i in range(len(stations) - 1):
        curr_dist = stations[i].distance
        curr_price = stations[i].price
        next_dist = stations[i+1].distance
        
        remaining_distance = total_distance - curr_dist
        if current_fuel * mileage >= remaining_distance:
            plan.append(PurchasePlan(
                station_num=i+1,
                location=curr_dist,
                price=curr_price,
                liters_bought=0.0,
                cost=0.0,
                reasoning=f"- **Current Fuel:** {round(current_fuel, 2)} L\n- **Decision:** We have enough fuel to reach the destination ({remaining_distance} km away). Bypassing this station entirely."
            ))
            break
            
        dist_to_next = next_dist - curr_dist
        fuel_to_next = dist_to_next / mileage
        
        if fuel_to_next > tank_capacity:
            return [], 0.0, f"IMPOSSIBLE: The gap between station {i+1} and station {i+2} ({dist_to_next} km) exceeds your tank's range ({tank_capacity * mileage} km)."
            
        # Identify reachable stations
        reachable_stations = []
        for j in range(i + 1, len(stations) - 1):
            if stations[j].distance - curr_dist <= tank_capacity * mileage:
                reachable_stations.append(j)

        cheaper_ahead = -1
        for j in reachable_stations:
            if stations[j].price < curr_price:
                cheaper_ahead = j
                break
                
        reasoning_lines = []
        reasoning_lines.append(f"- **Current Fuel:** {round(current_fuel, 2)} L")
        reasoning_lines.append(f"- **Max Reach:** {round(tank_capacity * mileage, 2)} km on a full tank.")
        
        if reachable_stations:
            reachable_str = ", ".join([f"Station {k+1} (Rs.{stations[k].price})" for k in reachable_stations])
            reasoning_lines.append(f"- **Stations in Reach:** {reachable_str}")
        else:
            reasoning_lines.append("- **Stations in Reach:** None (Destination is next)")

        buy = 0.0
        if cheaper_ahead != -1:
            dist_to_cheaper = stations[cheaper_ahead].distance - curr_dist
            fuel_needed = dist_to_cheaper / mileage
            buy = fuel_needed - current_fuel
            buy = max(buy, 0.0)
            buy = min(buy, tank_capacity - current_fuel)
            if buy > 0:
                reasoning_lines.append(f"- **Decision:** The nearest cheaper station is Station {cheaper_ahead+1} (Rs.{stations[cheaper_ahead].price}/L at {stations[cheaper_ahead].distance}km). Buying just enough (+{round(buy, 2)} L) to reach it.")
            else:
                reasoning_lines.append(f"- **Decision:** The nearest cheaper station is Station {cheaper_ahead+1}. We already have enough fuel to reach it. Buying 0 L.")
        else:
            buy = tank_capacity - current_fuel
            if buy > 0:
                reasoning_lines.append(f"- **Decision:** No cheaper station found within reach. This station is the cheapest available. Filling up tank to max capacity (+{round(buy, 2)} L).")
            else:
                reasoning_lines.append("- **Decision:** Tank is already full. Buying 0 L.")
            
        if current_fuel + buy < fuel_to_next:
            old_buy = buy
            buy = fuel_to_next - current_fuel
            if buy > old_buy:
                reasoning_lines.append(f"- **Correction:** Must buy at least {round(buy, 2)} L to reach the very next station to avoid stranding.")
            
        buy = round(buy, 2)
        
        cost = buy * curr_price
        total_cost += cost
        plan.append(PurchasePlan(
            station_num=i+1,
            location=curr_dist,
            price=curr_price,
            liters_bought=buy,
            cost=round(cost, 2),
            reasoning="\n".join(reasoning_lines)
        ))
            
        current_fuel = current_fuel + buy - fuel_to_next
        
    return plan, round(total_cost, 2), ""
