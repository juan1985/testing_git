
import binascii
import json
from pprint import pprint
import base64
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.lines import Line2D
import copy
import binascii


def generateFallDetection(impact, wait):
    fall = copy.deepcopy(fall_detection_defaults)
    print('post copy: ' + fall.hex())
    fall[fall_detection_offset_map['impact']
         ] = impact_threshold_choices[impact]
    fall[fall_detection_offset_map['stillness']] = wait_period_choices[wait]
    return fall


with open('test.json') as data_file:
    data = json.load(data_file)

graph_data_ppg = ''
graph_sample_i = 0
graph_data_acc = ''
master_acc = []
master_ppg = []


for entry in data:
    print("entry: " + repr(entry))
    v = entry["v"]
    pair_i = 0
    # for each entry in the ppg register reading pairs
    for tmpData in v:
        if pair_i == 0:
            pair_bytes = [0 for i in range(40)]
        ppg_v = [0 for i in range(5)]       # 5 ppg sample words per pair
        # 5 x,y,z sample vectors per pair
        acc_v = [[0, 0, 0] for i in range(5)]
        sample_i = 0
        ppg_i = 0
        #print("reading: "+repr(tmpData))
        tmpData = base64.b64decode(tmpData)
        tmpDataArr = bytearray(tmpData)
        tmpDataArr.reverse()
        #print("tmpData: "+repr(tmpDataArr))
        for i in range(0, len(tmpDataArr)):
            pair_bytes[pair_i * 20 + i] = tmpDataArr[i]
        if pair_i == 0:
            pair_i += 1
            continue
        pair_i = 0
        #print("pair_bytes collected: "+repr(pair_bytes))

        # each pair_bytes has 5 samples
        #  each sample has 8 bytes with:
        #    byte[0] = ppg lsb
        #    byte[1] = ppg msb
        #    byte[2] = acc x lsb
        #    byte[3] = acc x msb
        #    byte[4] = acc y lsb
        #    byte[5] = acc y msb
        #    byte[6] = acc z lsb
        #    byte[7] = acc z msb
        #print("ta length: "+str(len(pair_bytes)))
        for sample_i in range(5):
            ind = sample_i * 8
            #print("loop: "+str(ind)+" "+str(sample_i)+" "+str(ppg_i))
            ppg_v[ppg_i] = pair_bytes[ind] + (pair_bytes[ind + 1] << 8)
            graph_data_ppg += str(graph_sample_i) + "," + \
                str(ppg_v[ppg_i]) + "\n"
            master_ppg.append([graph_sample_i, ppg_v[ppg_i]])
            graph_sample_i += 1
            acc_x = pair_bytes[ind + 2] + (pair_bytes[ind + 3] << 8)
            acc_y = pair_bytes[ind + 4] + (pair_bytes[ind + 5] << 8)
            acc_z = pair_bytes[ind + 6] + (pair_bytes[ind + 7] << 8)
            acc_v[ppg_i] = [acc_x, acc_y, acc_z]
            graph_data_acc += str(acc_v[ppg_i]) + ',' + "\n"
            master_acc.append(acc_v[ppg_i])
            ppg_i += 1
            #print("end loop: "+repr(ppg_v))
        sample_conversion = {"ppg_v": ppg_v, "acc_v": acc_v}
        print("sample conversion: " + repr(sample_conversion))

file = open("ppgfile.csv", "w")
file.write(graph_data_ppg)
file.close()

graph_data_acc = '[' + graph_data_acc + ']'

file = open("accfile.csv", "w")
file.write(graph_data_acc)
file.close()

x, y, z = zip(*master_acc)
fig = plt.figure()

#ax = plt.subplot2grid((2, 2), (0, 0))

ax = fig.add_subplot(421, projection='3d')
ax.scatter(x, y, z)
ax.set_title("3d acceleration")

t = [i for i in range(len(x))]

line = Line2D(t, x)
az = fig.add_subplot(412)
az.add_line(line)
az.set_xlim(min(t), max(t))
az.set_ylim(min(x), max(x))
az.set_title('acc x')

line = Line2D(t, y)
az = fig.add_subplot(413)
az.add_line(line)
az.set_xlim(min(t), max(t))
az.set_ylim(min(y), max(y))
az.set_title('acc y')

line = Line2D(t, z)
az = fig.add_subplot(414)
az.add_line(line)
az.set_xlim(min(t), max(t))
az.set_ylim(min(z), max(z))
az.set_title('acc z')


x, y = zip(*master_ppg)  # ppg data plot

az = fig.add_subplot(422)
line = Line2D(x, y)
az.add_line(line)
az.set_xlim(min(x), max(x))
az.set_ylim(min(y), max(y))
az.set_title('ppg')

fig.subplots_adjust(hspace=.8, wspace=.43)
# plt.tight_layout()

# these are the UI choices

fall_detection_offset_map = {"free_fall": 0, "impact": 1,
                             "time_to_impact": 2, "fall_duration": 3, "stillness": 4, "wait": 5}

impact_threshold_choices = {"low": 0x28, "medium": 0x14, "high": 0x0a}
wait_period_choices = {"0": 0x00, "5": 0x0a, "15": 0x1e}

fall_detection_defaults = bytearray([0x60, 0x0a, 0x3d, 0x3d, 0x17, 0x00])

fall_detection_update = generateFallDetection("medium", "5")

print("fall_detection_update: " + fall_detection_update.hex())

# plt.show()


def generateFallDetection(impact, wait):
    fall = fall_detection_defaults.deepCopy()
    fall[fall_detection_offset_map['impact']
         ] = impact_threshold_choices[impact]
    fall[fall_detection_offset_map['stillnes']] = wait_period_choices[wait]
    return fall
