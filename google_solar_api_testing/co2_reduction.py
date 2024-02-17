# carbon_intensity: average grams of co2 emitted per kWh, which depends on country. (Japan: 482.87 grams of CO2e/kWh)
# monthly_kwh: average amount of electricity used per month. (Tokyo area, 4 family detached house: 436)
# time_span: defined in months

def co2_calculator(carbon_intensity, monthly_kwh, time_span):
    return (carbon_intensity*monthly_kwh*time_span)/1000
