from mrjob.job import MRJob
from mrjob.step import MRStep
import csv


class AirlineDelayAnalysis(MRJob):

    def mapper(self, _, line):
        reader = csv.reader([line])
        fields = next(reader)

        if len(fields) < 30 or fields[0] == 'Year':
            return

        try:
            airline = fields[9]
            carrier_delay = float(fields[25] or 0)
            weather_delay = float(fields[26] or 0)
            nas_delay = float(fields[27] or 0)
            security_delay = float(fields[28] or 0)
            late_aircraft_delay = float(fields[29] or 0)

            total_delay = carrier_delay + weather_delay + nas_delay + security_delay + late_aircraft_delay

            if total_delay > 0:
                yield (airline, 'total'), total_delay
                yield (airline, 'count'), 1
        except (ValueError, IndexError):
            self.increment_counter('warn', 'invalid_line', 1)

    def reducer(self, key, values):
        yield key, sum(values)

    def reducer_calculate_average(self, key, values):
        airline, metric = key
        total = sum(values)
        yield airline, (metric, total)

    def reducer_final(self, airline, values):
        total_delay = 0
        flight_count = 0
        for metric, value in values:
            if metric == 'total':
                total_delay = value
            elif metric == 'count':
                flight_count = value

        if flight_count > 0:
            average_delay = total_delay / flight_count
            yield airline, (total_delay, flight_count, average_delay)

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),
            MRStep(reducer=self.reducer_calculate_average),
            MRStep(reducer=self.reducer_final)
        ]


if __name__ == '__main__':
    AirlineDelayAnalysis.run()