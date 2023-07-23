'''
Composed dimensions from the base 7 (SI) dimensions.
'''

from ..config import Config, conf
from noether.core.Dimension import dimensionless, Dimension
from noether.core import display

from .fundamental import *


def D(d: Dimension, *n: str):
    return display(Dimension(d, *n))

# % Spacetime


area = D(length**2, 'area')
volume = D(length**3, 'volume')

speed = velocity = D(length / time, 'speed', 'velocity')
acceleration = D(speed / time, 'acceleration')
jerk = D(acceleration / time, 'jerk')
snap = jounce = D(jerk / time, 'jounce', 'snap')
crackle = D(snap / time, 'crackle')
pop = D(crackle / time, 'pop')

absement = D(length * time, 'absement')
absity = D(absement * time, 'absity')
abseleration = D(absity * time, 'abseleration')
abserk = D(abseleration * time, 'abserk')
absounce = D(abserk * time, 'absounce')

# % Angle

Config.register('DIMENSION_angle', True, '''\
Register angles as their own dimension, rather than dimensionless.''')

if conf.get('DIMENSION_angle'):
    angle = Dimension.new("angle", "φ", 200)
else:
    angle = dimensionless
solid_angle = D(angle**2, 'solid_angle')

frequency = D(time**-1, 'frequency')

# % Dynamics

force = weight = D(mass * acceleration, 'force', 'weight')
pressure = D(force / area, 'pressure')
energy = D(force * length, 'energy')
power = D(energy / time, 'power')

momentum = D(mass * speed, 'momentum')
yank = D(force / time, 'yank')

angular_momentum = D(length * momentum, 'angular_momentum')
angular_velocity = D(angle / time, 'angular_velocity')
angular_acceleration = D(angular_velocity / time, 'angular_acceleration')
angular_jerk = D(angular_acceleration / time, 'angular_jerk')

inertia = D(mass * angular_velocity, 'inertia')
torque = D(inertia * angular_acceleration, 'torque')

wavenumber = D(1 / length, 'wavenumber')
frequency_drift = gravitational_gradient = D(
    acceleration / length, 'frequency_drift', 'gravitational_gradient')

# % Electromagnetism

charge = D(current * time, 'charge')
voltage = D(power / current, 'voltage')
capacitance = D(charge / voltage, 'capacitance')
resistance = D(voltage / current, 'resistance')
inductance = D(resistance * time, 'inductance')
magnetic_flux = D(energy / current, 'magnetic_flux')
magnetic_flux_density = D(magnetic_flux / area, 'magnetic_flux_density')

conductance = D(resistance**-1, 'conductance')
resistivity = D(resistance * length, 'resistivity')
reluctance = D(1 / inductance, 'reluctance')

capicitive_reactance = D(
    capacitance * angular_velocity, 'capicitive_reactance')
inductive_reactance = D(inductance * angular_velocity, 'inductive_reactance')

permeability = D(inductance * length / area, 'permeability')
permittivity = D(capacitance * length / area, 'permittivity')
impedance = D(permeability * speed, 'impedance')
magnetic_moment = D(current * area, 'magnetic_moment')
magnetisation = D(magnetic_moment / volume, 'magnetisation')

# % Photometry

luminous_intensity = D(luminosity, 'luminous_intensity')
luminous_flux = luminous_power = D(luminosity * angle**2, 'luminous_power')

luminous_energy = D(luminous_flux * time, 'luminous_energy')
luminance = D(luminosity / area, 'luminance')
illuminance = luminous_exitance = luminous_emittance = D(
    luminous_flux / area, 'illuminance', 'luminous_exitance', 'luminous_emittance')

luminous_exposure = D(illuminance * time, 'luminous_exposure')
luminous_energy_density = D(
    luminous_energy / volume, 'luminous_energy_density')
luminous_efficiacy = D(luminosity / power, 'luminous_efficiacy')

irradiance = intensity = heat_flux = D(
    power / area, 'irradiance', 'intensity', 'heat_flux')

emission_coefficient = D(
    length / time**3 * solid_angle, 'emission_coefficient')

# % Material properties

flow = fluid_velocity = D(volume / time, 'fluid_velocity', 'flow')
catalytic_activity = D(substance / time, 'catalytic_activity')

linear_density = D(mass / length, 'linear_density')
area_density = D(mass / area, 'area_density')
density = D(mass / volume, 'density')
specific_volume = D(volume / mass, 'specific_volume')

number_density = D(1 / volume, 'number_density')
probability_density = D(1 / volume, 'probability_density')
reaction_rate = D(substance / (volume * time), 'reaction_rate')

specific_energy = dose = D(energy / mass, 'specific_energy', 'dose')
energy_density = D(energy / volume, 'energy_density')
molar_energy = D(energy / substance, 'molar_energy')

heat_capacity = entropy = D(energy / temperature, 'entropy')
specific_heat_capacity = D(heat_capacity / mass, 'specific_heat_capacity')
molar_heat_capacity = D(heat_capacity / substance, 'molar_heat_capacity')

surface_tension = D(force / length, 'surface_tension')
viscosity = D(pressure * time, 'viscosity')
kinematic_viscosity = D(viscosity / density, 'kinematic_viscosity')

# TODO: clear up moduli
bulk_modulus = D(volume * pressure / volume, 'bulk_modulus')

D(dimensionless, 'dimensionless')
proportion = D(dimensionless, 'proportion')
strain = D(dimensionless, 'strain')
reynolds_number = D(dimensionless, 'reynolds_number')

# % Thermal properties

gravity = D(acceleration * area / mass, 'gravity')
gravitational_parameter = D(gravity * mass, 'gravitational_parameter')

thermal_conductance = D(power / temperature, 'thermal_conductance')
thermal_conductivity = D(thermal_conductance *
                         length / area, 'thermal_conductivity')
thermal_resistance = D(temperature / power, 'thermal_resistance')
r_value = D(thermal_resistance * area, 'r_value')
thermal_resistivity = D(thermal_resistance * length /
                        area, 'thermal_resistivity')

# % Miscellaneous

# HACK: best done with .units.py
length.names.extend(['distance', 'height', 'width', 'breadth', 'depth'])
distance = height = width = breadth = depth = length

body_mass_index = D(mass / height**2, 'body_mass_index')

vehicle_efficiency = D(distance / volume, 'vehicle_efficiency')
einstein_coefficient_b = D(volume / energy / time, 'einstein_coefficient_b')
