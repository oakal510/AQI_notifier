import aqi as pyaqi


class EPA_AQI:

    def __init__(self, aqi):
        self.aqi = aqi

    @classmethod
    def from_pm_raw(cls, raw_data):
        aqi = pyaqi.to_iaqi(pyaqi.POLLUTANT_PM25, raw_data, algo=pyaqi.ALGO_EPA)
        return cls(aqi)

    @property
    def status(self) -> str:
        if self.aqi < 51:
            return "good"
        elif self.aqi < 101:
            return "moderate"
        elif self.aqi < 151:
            return "unhealthy for sensitive groups"
        elif self.aqi < 201:
            return "unhealthy"
        elif self.aqi < 301:
            return "very unhealthy"
        else:
            return "hazardous"

    @property
    def recommendations(self) -> str:
        if self.aqi < 51:
            return "Enjoy time outdoors! Breathe the fresh air."
        elif self.aqi < 101:
            return "Spend time outside."
        elif self.aqi < 151:
            return "Limit time outdoors."
        elif self.aqi < 201:
            return "Exercise caution if you need to go outside today."
        elif self.aqi < 301:
            return "Health alert! Severely limit outdoor activitie"
        else:
            return "It's fine. You are a cartoon dog drinking coffee while being engulfed in flames."

    def __str__(self):
        return f"Air Quality Index: {self.aqi}: {self.status}"
