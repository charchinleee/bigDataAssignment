import csv
from collections import defaultdict


def menu():
    options = [
        "Carrier Delay",
        "Weather Delay",
        "NAS Delay",
        "Security Delay",
        "Late Aircraft Delay",
        "Total Delay",
        "Average Carrier Delay",
        "Average Weather Delay",
        "Average NAS Delay",
        "Average Security Delay",
        "Average Late Aircraft Delay",
        "Average Total Delay",
        "Total Delay by Month",
        "Average Delay by Month",
        "Detailed Delay Analysis",
        "Origin Airport Delay Analysis",
        "Destination Airport Delay Analysis",
        "EXIT"
    ]
    print("-" * 30)
    print("Please Select an Option:")
    print("-" * 30)
    for i, option in enumerate(options[:-1], 1):
        print(f"{i}. {option}")
    print(f"0. {options[-1]}")
    return int(input("Input: "))


def calculate_delay(delay_column, average=False):
    dataset = open("DelayedFlights.csv", "r")
    next(dataset)
    airline_delays = {}
    airline_delay_counts = {}

    for line in csv.reader(dataset):
        airline = line[9]
        delay = float(line[delay_column] or 0.0)
        if delay > 0:
            airline_delays[airline] = airline_delays.get(airline, 0) + delay
            airline_delay_counts[airline] = airline_delay_counts.get(airline, 0) + 1

    print("\nTOTAL DELAY:" if not average else "\nAVERAGE DELAY:")
    for airline in airline_delays:
        delay = airline_delays[airline]
        if average:
            delay /= airline_delay_counts[airline]
        print([airline, delay])
    print("\n")

    dataset.close()


def total_delay(average=False):
    dataset = open("DelayedFlights.csv", "r")
    next(dataset)
    airline_delays = {}
    airline_delay_counts = {}

    for line in csv.reader(dataset):
        airline = line[9]
        delay = sum(float(line[i] or 0.0) for i in range(25, 30))
        if delay > 0:
            airline_delays[airline] = airline_delays.get(airline, 0) + delay
            airline_delay_counts[airline] = airline_delay_counts.get(airline, 0) + 1

    print("\nTOTAL DELAY:" if not average else "\nAVERAGE DELAY:")
    for airline in airline_delays:
        delay = airline_delays[airline]
        if average:
            delay /= airline_delay_counts[airline]
        print([airline, delay])
    print("\n")

    dataset.close()


def delay_by_month(average=False):
    dataset = open("DelayedFlights.csv", "r")
    next(dataset)
    month_delays = defaultdict(float)
    month_delay_counts = defaultdict(int)

    for line in csv.reader(dataset):
        month = int(line[2])  # Month column
        delay = sum(float(line[i] or 0.0) for i in range(25, 30))
        if delay > 0:
            month_delays[month] += delay
            month_delay_counts[month] += 1

    print("\nTOTAL DELAY BY MONTH:" if not average else "\nAVERAGE DELAY BY MONTH:")
    for month in sorted(month_delays.keys()):
        delay = month_delays[month]
        if average:
            delay /= month_delay_counts[month]
        print(f"Month {month}: {delay}")
    print("\n")

    dataset.close()


def detailed_delay_analysis():
    dataset = open("DelayedFlights.csv", "r")
    next(dataset)
    delays = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    counts = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    delay_types = ['Carrier', 'Weather', 'NAS', 'Security', 'Late Aircraft']

    for line in csv.reader(dataset):
        month = int(line[2])
        airline = line[9]
        for i, delay_type in enumerate(delay_types):
            delay = float(line[25 + i] or 0.0)
            if delay > 0:
                delays[month][delay_type][airline] += delay
                counts[month][delay_type][airline] += 1

    dataset.close()

    print("\nDETAILED DELAY ANALYSIS:")
    for month in sorted(delays.keys()):
        print(f"\nMonth {month}:")
        for delay_type in delay_types:
            print(f"  {delay_type} Delays:")
            sorted_airlines = sorted(delays[month][delay_type].items(), key=lambda x: x[1], reverse=True)
            for airline, total_delay in sorted_airlines:
                avg_delay = total_delay / counts[month][delay_type][airline]
                print(f"    {airline}: Total = {total_delay:.2f} minutes, Average = {avg_delay:.2f} minutes")

        print("  Summary:")
        type_totals = {dt: sum(delays[month][dt].values()) for dt in delay_types}
        sorted_types = sorted(type_totals.items(), key=lambda x: x[1], reverse=True)
        for delay_type, total in sorted_types:
            print(f"    {delay_type}: {total:.2f} minutes")


def origin_airport_delay_analysis():
    dataset = open("DelayedFlights.csv", "r")
    next(dataset)
    origin_delays = defaultdict(float)
    origin_counts = defaultdict(int)

    for line in csv.reader(dataset):
        origin = line[17]
        delay = sum(float(line[i] or 0.0) for i in range(25, 30))

        if delay > 0:
            origin_delays[origin] += delay
            origin_counts[origin] += 1

    dataset.close()

    print("\nORIGIN AIRPORT DELAY ANALYSIS:")
    print("\nTop 10 Origin Airports by Total Delay:")
    sorted_origins = sorted(origin_delays.items(), key=lambda x: x[1], reverse=True)[:10]
    for airport, total_delay in sorted_origins:
        avg_delay = total_delay / origin_counts[airport]
        print(f"{airport}: Total Delay = {total_delay:.2f} minutes, Average Delay = {avg_delay:.2f} minutes")


def destination_airport_delay_analysis():
    dataset = open("DelayedFlights.csv", "r")
    next(dataset)
    dest_delays = defaultdict(float)
    dest_counts = defaultdict(int)

    for line in csv.reader(dataset):
        dest = line[18]
        delay = sum(float(line[i] or 0.0) for i in range(25, 30))

        if delay > 0:
            dest_delays[dest] += delay
            dest_counts[dest] += 1

    dataset.close()

    print("\nDESTINATION AIRPORT DELAY ANALYSIS:")
    print("\nTop 10 Destination Airports by Total Delay:")
    sorted_dests = sorted(dest_delays.items(), key=lambda x: x[1], reverse=True)[:10]
    for airport, total_delay in sorted_dests:
        avg_delay = total_delay / dest_counts[airport]
        print(f"{airport}: Total Delay = {total_delay:.2f} minutes, Average Delay = {avg_delay:.2f} minutes")


delay_functions = [
    lambda: calculate_delay(25),  # Carrier Delay
    lambda: calculate_delay(26),  # Weather Delay
    lambda: calculate_delay(27),  # NAS Delay
    lambda: calculate_delay(28),  # Security Delay
    lambda: calculate_delay(29),  # Late Aircraft Delay
    total_delay,
    lambda: calculate_delay(25, average=True),  # Average Carrier Delay
    lambda: calculate_delay(26, average=True),  # Average Weather Delay
    lambda: calculate_delay(27, average=True),  # Average NAS Delay
    lambda: calculate_delay(28, average=True),  # Average Security Delay
    lambda: calculate_delay(29, average=True),  # Average Late Aircraft Delay
    lambda: total_delay(average=True),  # Average Total Delay
    lambda: delay_by_month(average=False),  # Total Delay by Month
    lambda: delay_by_month(average=True),  # Average Delay by Month
    detailed_delay_analysis,  # Detailed Delay Analysis
    origin_airport_delay_analysis,  # Origin Airport Delay Analysis
    destination_airport_delay_analysis  # Destination Airport Delay Analysis
]

while True:
    selection = menu()
    if selection == 0:
        print("Bye Bye")
        break
    elif 1 <= selection <= len(delay_functions):
        print("loading......")
        delay_functions[selection - 1]()
    else:
        print("Invalid selection. Please try again.")