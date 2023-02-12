'''
Various dimensions, for display purposes.
'''

from ..config import Config, conf
from ..core.Dimension import dimensionless, Dimension
from ..core.fundamental import *
from ..core.UnitSet import display as I

# % Spacetime

area = I(length**2, 'area')
volume = I(length**3, 'volume')

velocity = speed = I(length / time, 'speed')
acceleration = I(speed / time, 'acceleration')
jerk = I(acceleration / time, 'jerk')
jounce = snap = I(jerk / time, 'jounce', 'snap')
crackle = I(snap / time, 'crackle')
pop = I(crackle / time, 'pop')

absement = I(length * time, 'absement')
absity = I(absement * time, 'absity')
abseleration = I(absity * time, 'abseleration')
abserk = I(abseleration * time, 'abserk')
absounce = I(abserk * time, 'absounce')

# % Angle

Config.register('DIMENSION_angle', True, '''\
Register angles as their own dimension, rather than dimensionless.''')

if conf.get('DIMENSION_angle'):
    angle = Dimension.new("angle", "φ", 200)
else:
    angle = dimensionless
solid_angle = I(angle**2, 'solid_angle')

frequency = I(time**-1, 'frequency')

# % Dynamics

force = weight = I(mass * acceleration, 'force', 'weight')
pressure = I(force / area, 'pressure')
energy = I(force * length, 'energy')
power = I(energy / time, 'power')

momentum = I(mass * speed, 'momentum')
yank = I(force / time, 'yank')

angular_momentum = I(length * momentum, 'angular_momentum')
angular_velocity = I(angle / time, 'angular_velocity')
angular_acceleration = I(angular_velocity / time, 'angular_acceleration')
angular_jerk = I(angular_acceleration / time, 'angular_jerk')

inertia = I(mass * angular_velocity, 'inertia')
torque = I(inertia * angular_acceleration, 'torque')

wavenumber = I(1 / length, 'wavenumber')
frequency_drift = gravitational_gradient = I(
    acceleration / length, 'frequency_drift', 'gravitational_gradient')

# % Electromagnetism

charge = I(current * time, 'charge')
voltage = I(power / current, 'voltage')
capacitance = I(charge / voltage, 'capacitance')
resistance = I(voltage / current, 'resistance')
inductance = I(resistance * time, 'inductance')
magnetic_flux = I(energy / current, 'magnetic_flux')
magnetic_flux_density = I(magnetic_flux / area, 'magnetic_flux_density')

conductance = I(resistance**-1, 'conductance')
resistivity = I(resistance * length, 'resistivity')
reluctance = I(1 / inductance, 'reluctance')

capicitive_reactance = I(
    capacitance * angular_velocity, 'capicitive_reactance')
inductive_reactance = I(inductance * angular_velocity, 'inductive_reactance')

permeability = I(inductance * length / area, 'permeability')
permittivity = I(capacitance * length / area, 'permittivity')
impedance = I(permeability * speed, 'impedance')
magnetic_moment = I(current * area, 'magnetic_moment')
magnetisation = I(magnetic_moment / volume, 'magnetisation')

# % Photometry

luminous_intensity = I(luminosity, 'luminous_intensity')
luminous_flux = luminous_power = I(luminosity * angle**2, 'luminous_power')

luminous_energy = I(luminous_flux * time, 'luminous_energy')
luminance = I(luminosity / area, 'luminance')
illuminance = luminous_exitance = luminous_emittance = I(
    luminous_flux / area, 'illuminance', 'luminous_exitance', 'luminous_emittance')

luminous_exposure = I(illuminance * time, 'luminous_exposure')
luminous_energy_density = I(
    luminous_energy / volume, 'luminous_energy_density')
luminous_efficiacy = I(luminosity / power, 'luminous_efficiacy')

irradiance = intensity = heat_flux = I(
    power / area, 'irradiance', 'intensity', 'heat_flux')

emission_coefficient = I(
    length / time**3 * solid_angle, 'emission_coefficient')

# % Material properties

flow = fluid_velocity = I(volume / time, 'fluid_velocity', 'flow')
catalytic_activity = I(substance / time, 'catalytic_activity')

linear_density = I(mass / length, 'linear_density')
area_density = I(mass / area, 'area_density')
density = I(mass / volume, 'density')
specific_volume = I(volume / mass, 'specific_volume')

number_density = I(1 / volume, 'number_density')
probability_density = I(1 / volume, 'probability_density')
reaction_rate = I(substance / (volume * time), 'reaction_rate')

specific_energy = dose = I(energy / mass, 'specific_energy', 'dose')
energy_density = I(energy / volume, 'energy_density')
molar_energy = I(energy / substance, 'molar_energy')

heat_capacity = entropy = I(energy / temperature, 'entropy')
specific_heat_capacity = I(heat_capacity / mass, 'specific_heat_capacity')
molar_heat_capacity = I(heat_capacity / substance, 'molar_heat_capacity')

surface_tension = I(force / length, 'surface_tension')
viscosity = I(pressure * time, 'viscosity')
kinematic_viscosity = I(viscosity / density, 'kinematic_viscosity')

# TODO: clear up moduli
bulk_modulus = I(volume * pressure / volume, 'bulk_modulus')

I(dimensionless, 'dimensionless')
proportion = I(dimensionless, 'proportion')
strain = I(dimensionless, 'strain')
reynolds_number = I(dimensionless, 'reynolds_number')

# % Thermal properties

gravity = I(acceleration * area / mass, 'gravity')
gravitational_parameter = I(gravity * mass, 'gravitational_parameter')

thermal_conductance = I(power / temperature, 'thermal_conductance')
thermal_conductivity = I(thermal_conductance *
                         length / area, 'thermal_conductivity')
thermal_resistance = I(temperature / power, 'thermal_resistance')
r_value = I(thermal_resistance * area, 'r_value')
thermal_resistivity = I(thermal_resistance * length /
                        area, 'thermal_resistivity')

# % Miscellaneous

distance = height = I(length, 'distance', 'height')
width = breadth = depth = I(length, 'width', 'breadth', 'depth')
body_mass_index = I(mass / height**2, 'body_mass_index')

vehicle_efficiency = I(distance / volume, 'vehicle_efficiency')
einstein_coefficient_b = I(volume / energy / time, 'einstein_coefficient_b')
