import re

unit_milliseconds = 'ms'
unit_seconds = 's'
unit_minutes = 'n'
unit_hours = 'h'
unit_days = 'd'
unit_dict = {
    unit_milliseconds: "millisecond(s)",
    unit_seconds: "second(s)",
    unit_minutes: "minute(s)",
    unit_hours: "hour(s)",
    unit_days: "day(s)"
}


class Duration:
    duration_time: int
    duration_unit: str

    def __init__(self, duration_str):
        re_duration_units = f"({'|'.join([f'({unit})' for unit in unit_dict.keys()])})"
        if re.fullmatch(f"[0-9]+{re_duration_units}", duration_str) is None:
            raise Exception("Duration string could not be parsed.")

        self.duration_time = int(re.search("[0-9]+", duration_str)[0])
        self.duration_unit = re.search(re_duration_units, duration_str)[0]

    def __repr__(self):
        return f"{self.duration_time} {unit_dict[self.duration_unit]}"

    def get_seconds(self) -> float:
        if self.duration_unit == unit_milliseconds:
            return self.duration_time / 1000
        elif self.duration_unit == unit_seconds:
            return self.duration_time
        elif self.duration_unit == unit_minutes:
            return self.duration_time * 60
        elif self.duration_unit == unit_hours:
            return self.duration_time * 60 * 60
        elif self.duration_unit == unit_days:
            return self.duration_time * 60 * 60 * 24
