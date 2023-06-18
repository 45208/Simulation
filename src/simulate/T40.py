from ..drone import Drone, Battery, Container, Pump

# Constants
DEFAULT_SPRAY_RANGE = 10
MAX_FLOW = 720

battery = Battery(30)
container = Container(battery, ct=857.14, capacity=40)
pump = Pump(battery, container, cp=0.42,
            max_spray_range=DEFAULT_SPRAY_RANGE, max_flow=MAX_FLOW)
default_drone = Drone(battery, pump, c=11000, max_speed=10)
