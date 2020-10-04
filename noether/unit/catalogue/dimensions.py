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

# TODO: differentiate Dimension and Physical Quantity
# (for when symbols overlap!!)

# # Spacetime

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

# # Angle

frequency = time**-1
angle = Dimension.new("angle", dimsym="φ", unitsym="rad", order=200)
solid_angle = angle**2

# # Dynamics

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

gravitational_gradient = acceleration / distance

# # Electromagnetism

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

# # Photometry

luminous_intensity = luminosity
luminous_flux = luminous_power = luminosity * angle**2

luminous_energy = luminous_flux * time
luminance = luminosity / area
illuminance = luminous_exitance = luminous_emittance = luminous_flux / area

luminous_exposure = illuminance * time
luminous_energy_density = luminous_energy / volume
luminous_efficiacy = luminosity / power

dose = energy / mass

irradiance = intensity = heat_flux = power / area

emission_coefficient = length / time**3 * solid_angle

# # Material properties

flow = fluid_velocity = volume / time
catalytic_activity = substance / time

linear_density = mass / length
area_density = mass / area
density = mass / volume
specific_volume = volume / mass

number_density = 1 / volume
probability_density = 1 / volume
reaction_rate = substance / (volume * time)

specific_energy = energy / mass
energy_density = energy / volume
molar_energy = energy / substance

heat_capacity = entropy = energy / temperature
specific_heat_capacity = heat_capacity / mass
molar_heat_capacity = heat_capacity / substance

surface_tension = force / length
viscosity = pressure * time
kinematic_viscosity = viscosity / density

# TODO: clear up moduli
bulk_modulus = volume * pressure / volume
strain = length / length


# # Medical dimensions

height = length
width = breadth = length
depth = length
body_mass_index = mass / height**2

# # Miscellaneous

vehicle_efficiency = distance / volume
einstein_coefficient_b = volume / energy / time
