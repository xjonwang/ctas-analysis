from typing import *

def perpetual_growth_dcf(
    free_cash_flow: float,
    discount_rate: List[float],
    growth_rate: List[float],
    duration: int,
    perpetual_rate: float,
    perpetural_discount_rate: float,
):
    future_cash_flows = [free_cash_flow]
    discount_factors = [1]

    for i in range(1, duration):
        future_cash_flows.append(future_cash_flows[-1] + (growth_rate[i-1] / 100) * future_cash_flows[-1])
    for i in range(1, duration):
        discount_factors.append(discount_factors[-1] * (1 + discount_rate[i-1] / 100))

    terminal_value = ((future_cash_flows[-1] / discount_factors[-1]) * (1 + perpetual_rate / 100) / (perpetural_discount_rate / 100 - perpetual_rate / 100))

    pvs = [round(cash_flow / discount_factor, 2) for cash_flow, discount_factor in zip(future_cash_flows, discount_factors)]
    pvs.append(terminal_value)
    print(future_cash_flows)
    print(discount_factors)

    dcf = sum(pvs)
    print("Fair value (according to Perpetual Growth Method DCF):", dcf)

# CTAS inputs
if __name__ == "__main__":
    free_cash_flow = 1295824
    discount_rate = []
    for i in range(5):
        discount_rate.append(7.48)
    # To account for maturity wall + renormalization of rates post-COVID
    for i in range(4):
        discount_rate.append(9)
    growth_rate = []
    for i in range(5):
        growth_rate.append(12.11)
    for i in range(4):
        growth_rate.append(10)
    duration = 10
    perpetual_rate = 3 # based on longer term inflation plus baseline real GDP growth
    perpetual_discount_rate = 9
    perpetual_growth_dcf(
        free_cash_flow=free_cash_flow,
        discount_rate=discount_rate,
        growth_rate=growth_rate,
        duration=duration,
        perpetual_rate=perpetual_rate,
        perpetural_discount_rate=perpetual_discount_rate
    )