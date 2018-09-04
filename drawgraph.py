import json
import glob
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.style.use('default')
plt.title('GA Results (K=200, a=0.8, b=0.2, e=0.1)')
plt.xlabel('Generations')
plt.ylabel('Fitness')
Datas = [x for x in range(350,361)]
for i in range(min(10,len(Datas))):
    with open('logs/N'+str(Datas[i])+'K200.txt') as file:
        data = json.load(file)
    plt.plot(range(len(data[1][2])),data[1][2],'C'+str(i),label='N='+str(Datas[i]))
if len(Datas)>10:
    for i in range(10,len(Datas)):
        with open('logs/N'+str(Datas[i])+'K200.txt') as file:
            data = json.load(file)
        plt.plot(range(len(data[1][2])),data[1][2],'--',color='C'+str(i-10),label='N='+str(Datas[i]))
plt.legend()
plt.show()

# import gui
# gui.update(gui.turn(gui.solved,data[1][1]))
