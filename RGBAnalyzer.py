from PIL import Image
import matplotlib.pyplot as plt
from tqdm import tqdm
import os
from operator import add
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np
from statistics import mean

def getRed(R): return '#%02x%02x%02x'%(R,0,0)
def getGreen(G): return '#%02x%02x%02x'%(0,G,0)
def getBlue(B):return '#%02x%02x%02x'%(0,0,B)

def getAggregatedData(data_list, step = 8):
    l_size = len(data_list)
    value = 0
    x_values = []

    while value <= l_size:
        x_values.append(value)
        value = value + step

    y_values = []
    for i in range(len(x_values)):
        sum = []
        if i < len(x_values) - 1:
            for j in range(x_values[i], x_values[i+1]):
                sum.append(data_list[j])
            y_values.append(mean(sum))

    x_values.pop(0)
    
    return x_values, y_values
        
def readDataset(path):
    r = []
    g = []
    b = []
    for image in tqdm(os.listdir(path)):
        i = Image.open(os.path.join(path, image))

        hst= i.histogram()

        Red = hst[0:256]      # indicates Red
        Green = hst[256:512]  # indicated Green
        Blue = hst[512:768]   # indicates Blue

        if len(r) == 0:
            r = Red
        else:
            r = list(map(add, r, Red))

        if len(g) == 0:
            g = Green
        else:
            g = list(map(add, g, Green))

        if len(b) == 0:
            b = Blue
        else:
            b = list(map(add, b, Blue))

    return r, g, b

def plotFigures(x_r, y_r, x_g, y_g, x_b, y_b, plot_file):
    plt.hist(x_r, y_r, color='red', label='Red')
    plt.plot(x_g, y_g, color='green', label='Green')
    plt.plot(x_b, y_b, color='blue', label='Blue')
    plt.xlabel('RGB Value')
    plt.ylabel('Count')
    plt.legend()
    # plot_file = "figures/rgb_plots/aggregated/" + "FCG_New_Textures.png"
    plt.savefig(plot_file)
    plt.show()

def normalize(arr_2d):
    norm = np.linalg.norm(arr_2d)
    matrix = arr_2d/norm  
    return matrix

def getXTicks(steps):
    tickVals = []
    initial = steps
    while(initial <= 256):
        tickVals.append(str(initial))
        initial = initial + steps

    return tickVals


def plotHist(r_vals, g_vals, b_vals, plot_file, title, width = 0.3, steps = 8):
    assert len(r_vals) == len(g_vals) == len(b_vals)
    # assert len(cr_vals) == len(cg_vals) == len(cb_vals)
    
    ind = len(r_vals)
    x_axis = np.arange(ind)
    plt.figure(figsize=(12, 4.8))
    
    bar1 = plt.bar(x_axis- 0.3, r_vals, width, color = 'tab:red') 
    # bar1x = plt.bar(x_axis- 0.3, cr_vals, width, color = 'maroon') 
    
    
    bar2 = plt.bar(x_axis, g_vals, width, color='tab:green') 
    # bar2x = plt.bar(x_axis, cg_vals, width, color = 'forestgreen') 
    
    
    bar3 = plt.bar(x_axis+0.3, b_vals, width, color = 'tab:blue') 
    # bar3x = plt.bar(x_axis+0.3, cb_vals, width, color = 'teal') 
    
    plt.xlabel("Grouped bins (Ex. 8 --> values from 0-7)") 
    plt.ylabel('Average RGB count every 8 bins') 
    plt.title("RGB Count for " + title) 
    # print(getXTicks(steps))
    xticks= getXTicks(steps)
    # print(len(xticks))
    # print(ind+width)

    plt.xticks(x_axis,xticks,fontsize=8) 
    plt.ylim(0, 0.3)
    # print(len(getXTicks(steps)))
    plt.legend( (bar1, bar2, bar3), ('Red Count', 'Green Count', 'Blue Count') ) 
    
    plt.savefig(plot_file)
    plt.show() 

def getDelta(y_City, y_Synth):
    assert len(y_City) == len(y_Synth)
    diff = []
    for i in range(len(y_City)):
        diff.append(abs(y_City[i] - y_Synth[i]))

    return diff



path_0 = 'datasets/cityscapes_256/images'
path = 'datasets/FCG_Base/images'

r_c, g_c,b_c = readDataset(path_0)
r, g, b = readDataset(path)

x_r , y_r = getAggregatedData(r, step=8)
x_g , y_g = getAggregatedData(g, step=8)
x_b , y_b = getAggregatedData(b, step=8)

# print(y_r)
# print(len(y_r))

x_rc , y_rc = getAggregatedData(r_c, step=8)
x_gc , y_gc = getAggregatedData(g_c, step=8)
x_bc , y_bc = getAggregatedData(b_c, step=8)

plot_file = "figures/delta/FCG_Bases_normalized.png"
title="UC-Gen: Base"
newData = normalize([y_r, y_g, y_b, y_rc, y_gc, y_bc])
y_r, y_g, y_b, y_rc, y_gc, y_bc = newData[0], newData[1], newData[2], newData[3], newData[4], newData[5]
plotHist(y_r, y_g, y_b, plot_file, title=title)
# plot_file = "figures/delta/cityscapes_normalized.png"
# title="Cityscapes"
# plotHist(y_rc, y_gc, y_bc, plot_file, title=title)

print(y_r[5])
print(y_rc[5])
# plotFigures(x_r, getDelta(y_rc, y_r), x_g, getDelta(y_gc, y_g), x_b, getDelta(y_bc, y_b), plot_file)


# r = np.array(r)
# r_size = np.arange(len(r))
# print(len(r))
# g_size = np.arange(len(r))
# b_size = np.arange(len(r))

# model_r = LinearRegression()
# model_g = LinearRegression()
# model_b = LinearRegression()

# model_r.fit(r.reshape(-1, 1), r_size)
# model_g.fit(g, g_size)
# model_b.fit(b, b_size)

# r_linspace = np.linspace(1, len(r), 10)
# y_new = model_r.predict(r.reshape(-1, 1))

# red_counts = []
# plt.figure(0)             # plots a figure to display RED Histogram
# for i in range(0, 255):
#     plt.bar(i, Red[i], color = getRed(i),alpha=0.3)
# plt.figure(1)             # plots a figure to display GREEN Histogram
# for i in range(0, 255):
#     plt.bar(i, Green[i], color = getGreen(i),alpha=0.3)
# plt.figure(2)             # plots a figure to display BLUE Histogram
# for i in range(0, 255):
#     plt.bar(i, Blue[i], color = getBlue(i),alpha=0.3)
# plt.show()


# plot lines

# ----------------------


# print(len(r))
# plt.figure(0) 
# plt.plot(r, label = "Red", color = "red")
# plt.plot(g, label = "Green", color = "green")
# plt.plot(b, label = "Blue", color = "blue")

# plt.legend()
# plot_file = "figures/rgb_plots/" + "cityscapes_256.png"
# plt.savefig(plot_file)
# plt.show()

# print(Red.index(max(Red)))
# print(Green.index(max(Green)))
# print(Blue.index(max(Blue)))


# ----------------------

# sns.set_theme()
# sns.displot(Red)
# plt.show()


# ax = plt.axes()
# ax.plot(r_linspace.reshape(-1, 1), y_new)

# plt.plot(r_size, y_new, color='red', label='Linear Regression Line')
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.legend()
# plt.show()
# print(y_new)
