from Array import Array
from Environment import Environment
from openpyxl import Workbook
from matplotlib import pyplot

wb = Workbook()
ws = wb.active
array = Array(5)
water = Array(5)
wheel = {}
env = Environment()
t = 0
time = []
temp = []
avg_temp = []
wue = []
avg_wue = []
array.randomize()
env.set_total_intensity(0)
env.set_blue_intensity(0)
env.set_ambient_water(10)
while t < 300:
    temp.clear()
    wue.clear()
    wheel[t % 7] = Array()
    if t >= 7:
        array.calculate_next(env, water, wheel[(t - 6) % 7], t)
    else:
        array.calculate_next(env, water, wheel[t], t)
    if t == 20:
        env.set_total_intensity(900)
    if t == 200:
        env.set_blue_intensity(5)

    for i in range(5):
        for unit in array[i]:
            temp.append(unit.get_temperature())
            wue.append((env.get_ambient_carbon() - unit.get_carbon_dioxide()) /
                       (unit.get_es_water_vapor() - env.get_ambient_water()))

    avg_temp.append(sum(temp) / len(temp))
    avg_wue.append(sum(wue) / len(wue))
    time.append(t)
    t += 1

plot = pyplot
fig, ax1 = plot.subplots()
color = 'tab:red'
ax1.set_xlabel('Time (min)')
ax1.set_ylabel('Average Temperature (K)')
ax1.plot(time[25:], avg_temp[25:], color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('Average WUE (μmol CO2/mmol H2O)')
ax2.plot(time[25:], avg_wue[25:])
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
plot.show()
