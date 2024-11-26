import matplotlib.pyplot as plt
import numpy as np
from math import *
from matplotlib.widgets import Button, Slider, TextBox
import matplotlib.patches as patches
from enum import Enum

x_min = -5
x_max = 5
y_min = 0
y_max = 40
x = np.linspace(x_min, x_max, 1000)

class RiemannSumType():
    LRS = 1 
    RRS = 2
    MRS = 3
    TRS = 4
    currentType = LRS
    def setType(self, type):
        self.currentType = type
    def getType(self):
        return self.currentType
        
    

def quad(x):
    return x**2

def RiemannSum(rect_num = 2):
    width = (x_max - x_min)/rect_num
    heights = []
    
    if RSType.getType() == RiemannSumType.LRS:
        x_of_bar = [x_min+width/2]
        eval_at = [x_min]
    elif RSType.getType() == RiemannSumType.MRS:
        x_of_bar = [x_min+width/2]
        eval_at = [x_min+width/2]
    elif RSType.getType() == RiemannSumType.RRS:
        x_of_bar = [x_min+width/2]
        eval_at = [x_min+width]
    elif RSType.getType() == RiemannSumType.TRS:
        x_of_bar = [x_min]
        eval_at = [x_min]
        
        
    for x in range(rect_num):
        next_x = x_of_bar[-1] + width
        next_eval = eval_at[-1] + width
        x_of_bar.append(next_x)
        eval_at.append(next_eval)
        
    if RSType.getType() != RiemannSumType.TRS:
        x_of_bar.pop()
        eval_at.pop()
    
    for x in eval_at:
        heights.append(quad(x))
        
    area = 0
    for h in range(len(heights)):
        if RSType.getType() != RiemannSumType.TRS:
            area += heights[h] * width
        else:
            if h == 0:
                area += heights[h] 
            elif h == len(heights)-1:
                area += heights[h]
            else:
                area += 2 * heights[h]
    if RSType.getType() == RiemannSumType.TRS:
        area *= .5 * width 
    area = round(area, 5)
    return(x_of_bar, heights, width, area)
    
    
RSType = RiemannSumType()    

init_rects = 2

fig, ax = plt.subplots()
ax.autoscale(False)
ax.set_xbound(x_min, x_max)
ax.set_ybound(y_min, y_max)
line, = ax.plot(x, quad(x))

areaLabel = fig.text(.5, .9, "Area: ")

axRects = fig.add_axes([0.25, 0.01, 0.65, 0.03])
rect_slider = Slider(
    ax=axRects,
    label='Number of Rectangles',
    valmin=2,
    valmax=100,
    valinit=init_rects,
    valstep=1
)
axLRSButton = fig.add_axes([0.1, .9, 0.09, 0.09])
LRS_button = Button(
    ax=axLRSButton,
    label = "LRS"
)
axMRSButton = fig.add_axes([0.2, .9, 0.09, 0.09])
MRS_button = Button(
    ax=axMRSButton,
    label = "MRS"
)
axRRSButton = fig.add_axes([0.3, .9, 0.09, 0.09])
RRS_button = Button(
    ax=axRRSButton,
    label = "RRS"
)
axTRSButton = fig.add_axes([0.4, .9, 0.09, 0.09])
TRS_button = Button(
    ax=axTRSButton,
    label = "TRS"
)


def update(val):
    graph_vals = RiemannSum(rect_slider.val)
    ax.bar([y_min],[y_max],[x_max-x_min], color="#FFFFFF")
    if RSType.getType() != RiemannSumType.TRS:
        ax.bar(graph_vals[0],graph_vals[1],graph_vals[2],color="Blue")
    else:
        x = graph_vals[0]
        y = graph_vals[1]
        x_of_points = []
        for i in range(len(x)-1):
            x_of_points = [x[i], x[i], x[i+1], x[i+1]]
            y_of_points = [y_min, y[i], y[i+1], y_min]
            ax.add_patch(patches.Polygon(xy=list(zip(x_of_points, y_of_points)), fill=True))
    areaLabel.set_text(f"Area: {graph_vals[3]}")
    fig.canvas.draw_idle()
    
    
def LRSClicked(val):
    RSType.setType(RiemannSumType.LRS)
    update(rect_slider.val)
def RRSClicked(val):
    RSType.setType(RiemannSumType.RRS)
    update(rect_slider.val)
def MRSClicked(val):
    RSType.setType(RiemannSumType.MRS)
    update(rect_slider.val)
def TRSClicked(val):
    RSType.setType(RiemannSumType.TRS)
    update(rect_slider.val)
    
#RiemannSum()
rect_slider.on_changed(update)
LRS_button.on_clicked(LRSClicked)
RRS_button.on_clicked(RRSClicked)
MRS_button.on_clicked(MRSClicked)
TRS_button.on_clicked(TRSClicked)
update(rect_slider.val)

plt.show()