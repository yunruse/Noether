"""
Dimensions of measure.

The top 'paragraph' of each section contains dimensions with
corresponding SI units defined in si.py.
"""

from .fundamental import (
    U, Dimension,
    distance, time, length, mass,
    current, luminosity, substance, temperature
)

# spacetime

area = length**2
volume = length**3

velocity = speed = distance / time
acceleration = speed / time
jerk = acceleration / time
jounce = snap = jerk / time
crackle = snap / time
pop = crackle / time
lock = pop / time
drop = pop / time

absement = distance * time
absity = absement * time
abseleration = absity * time
abserk = abseleration * time
absounce = abserk * time

# rotation

frequency = time**-1
angle = Dimension.new(3.2, "angle", "φ", "rad")

# dynamics

force = weight = mass * acceleration
pressure = force / area
energy = force * distance
power = energy / time

momentum = mass * speed
angular_momentum = length * momentum
angular_velocity = angle / time
angular_acceleration = angular_velocity / time
angular_jerk = angular_acceleration / time

inertia = mass * angular_velocity
torque = inertia * angular_acceleration

# electromagnetism

charge = current * time
voltage = power / current
capacitance = charge / voltage
resistance = voltage / current
inductance = resistance * time
magnetic_flux = energy / current
magnetic_flux_density = magnetic_flux / area

conductance = resistance**-1
resistivity = resistance / length
reluctance = 1 / inductance

capicitive_reactance = capacitance * angular_velocity
inductive_reactance = inductance * angular_velocity

permeability = inductance * length / area
permittivity = capacitance * length / area
impedance = permeability * speed
magnetic_moment = current * area
magnetisation = magnetic_moment / volume

# radiation

luminous_flux = luminosity * angle**2
illuminance = luminosity / area
dose = energy / mass

irradiance = intensity = heat_flux = power / area

# material properties

flow = fluid_velocity = volume / time
catalytic_activity = substance / time

linear_density = mass / length
area_density = mass / area
density = mass / volume
specific_volume = volume / mass

number_density = 1 / volume
reaction_rate = substance / (volume * time)

specific_energy = energy / mass
molar_energy = energy / substance

heat_capacity = entropy = energy / temperature
specific_heat_capacity = heat_capacity / mass
molar_heat_capacity = heat_capacity / substance

surface_tension = force / length
viscosity = pressure * time


# various dimensions

body_mass_index = mass / area
vehicle_efficiency = distance / volume
