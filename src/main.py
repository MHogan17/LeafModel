import sys
from Experiment import ExperimentFactory

if len(sys.argv) < 2:
    print("Usage: src/main.py EXPERIMENT_TYPE")
    sys.exit()

else:
    try:
        experiment = ExperimentFactory(sys.argv[1])
    except RuntimeError as e:
        print(e)
        sys.exit()
'''
if sys.argv[2] == 's':
    experiment.environment.set_total_intensity((input('Set the total intensity (W/(m^2)): ')))
    experiment.environment.set_blue_intensity(input('Set the blue intensity (%): '))
    experiment.environment.set_ambient_temperature(input('Set the temperature (K): '))
    experiment.environment.set_ambient_water(input('Set the humidity (ppt): '))
    experiment.environment.set_ambient_carbon(input('Set the carbon dioxide level (ppm): '))
'''
try:
    experiment.run()
except RuntimeError as e:
    print(e)
    sys.exit()

sys.exit()


