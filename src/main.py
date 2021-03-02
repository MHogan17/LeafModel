import sys
from Experiment import ExperimentFactory

if len(sys.argv) < 2:
    print("Usage: src/main.py EXPERIMENT_TYPE [-s]")
    sys.exit()

else:
    try:
        experiment = ExperimentFactory(sys.argv[1])
    except RuntimeError as e:
        print(e)
        sys.exit()
if len(sys.argv) > 2:
    if sys.argv[2] == '-s':
        experiment.environment.set_total_intensity(float((input('Set the total intensity (W/(m^2)): '))))
        experiment.environment.set_blue_intensity(float(input('Set the blue intensity (%): ')))
        experiment.environment.set_ambient_temperature(float(input('Set the temperature (K): ')))
        experiment.environment.set_ambient_water(float(input('Set the humidity (ppt): ')))
        experiment.environment.set_ambient_carbon(float(input('Set the carbon dioxide level (ppm): ')))
    else:
        print("Usage: src/main.py EXPERIMENT_TYPE [-s]")
        sys.exit()
try:
    experiment.run()
except RuntimeError as e:
    print(e)
    sys.exit()

sys.exit()


