import sys
from Experiment import ExperimentFactory


if len(sys.argv) < 2:
    print("Usage: src/main.py EXPERIMENT")

else:
    try:
        experiment = ExperimentFactory(sys.argv[1])
        experiment.run()
    except RuntimeError as e:
        print(e)
