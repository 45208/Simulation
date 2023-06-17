class BatteryException(Exception):
    pass


class Battery:
    voltage = 110

    def __init__(self, capacity: float):
        self.capacity = capacity * self.voltage
        self.remaining = self.capacity

    def calculate(self, amount: float):
        if self.remaining < amount:
            raise BatteryException()
        self.remaining -= amount

class ContainerException(Exception):
    pass

class Container:
    def __init__(self, battery: Battery, ct: float, capacity: float,
                 remaining: float | None = None):
        self.ct = ct
        self.capacity = capacity
        self.remaining = capacity if remaining is None else remaining
        self.battery = battery

    def calculate(self, seconds: float, used: float):
        hours = seconds / 3600
        self.battery.calculate(self.ct * self.remaining * hours)
        if self.remaining < used:
            raise ContainerException
        self.remaining -= used


class Pump:
    def __init__(self, battery: Battery, container: Container,
                 cp: float, spray_range: float, max_flow: float, fp: float | None = None):
        self.battery, self.container = battery, container
        self.cp = cp
        self.max_flow = max_flow
        self.fp = self.max_flow if fp is None else fp
        self.spray_range = spray_range

    def change_fp(self, fp: float):
        assert self.max_flow >= self.fp
        self.fp = fp

    def change_range(self, spray_range: float):
        self.spray_range = spray_range

    def calculate(self, seconds: float):
        hours = seconds / 3600
        self.battery.calculate(self.cp * self.fp * hours)
        self.container.calculate(seconds, self.fp * hours)


class Drone:
    def __init__(self, battery: Battery, pump: Pump, c: float, max_speed: float, v: float | None = None):
        self.battery = battery
        self.pump = pump
        self.c = c
        self.max_speed = max_speed
        self.v = max_speed if v is None else v

    def change_speed(self, v: float):
        assert self.max_speed >= self.v
        self.v = v

    def change_speed_based_on_pump(self, concen: float):
        assert self.pump.fp != 0
        assert self.pump.spray_range != 0
        # Concen: L/ha
        # TODO

    def calculate(self, seconds: float):
        hours = seconds / 3600
        self.pump.calculate(seconds)
        self.battery.calculate(self.c * hours)

