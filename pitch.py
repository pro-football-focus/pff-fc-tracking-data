#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 11:19:26 2021

@author: apschram
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, Rectangle, ConnectionPatch 

plt.style.use('seaborn-v0_8-poster')
# plt.rcParams["font.family"] = "Roboto"

def drawPitch(ax=None, x=120, y=80, c1='black', c2='grey', linewidth1=2, linewidth2=1, pitchcolor=0):
    fig = plt.figure(dpi=330)
    
    if ax is None:
        ax = plt.gca()
        
    pitch = Rectangle((0,0), x, y, linewidth=linewidth1 * 2, color=c1, fill=False, zorder=0)
    
    goal1 = Rectangle((0, (y - y * 7.32/68)/2), -1.5, y * 7.32/68, linewidth=linewidth1 * 2, color=c1, fill=False, zorder=-1)
    goal2 = Rectangle((x, (y - y * 7.32/68)/2), +1.5, y * 7.32/68, linewidth=linewidth1 * 2, color=c1, fill=False, zorder=-1)

    fiveYard1 = Rectangle((x - x * 5.5/105, y * 24/68), x * 5.5/105, y * 20/68, linewidth=linewidth1, color=c1, fill=False, zorder=-1)
    fiveYard2 = Rectangle((0, y * 24/68), x * 5.5/105, y * 20/68, linewidth=linewidth1, color=c1, fill=False, zorder=-1)
    
    penBox1 = Rectangle((x - x * 16.5/105, y * 14/68), x * 16.5/105, y * 40/68, linewidth=linewidth1, color=c1, fill=False, zorder=-1)
    penBox2 = Rectangle((0, y * 14/68), x * 16.5/105, y * 40/68, linewidth=linewidth1, color=c1, fill=False, zorder=-1)
    penSpot1 = Circle((x - (11/105) * x, y/2),0.25,color="black")
    penSpot2 = Circle(((11/105) * x, y/2),0.25,color="black")
    penCircle1 = Arc((x - (11/105) * x, y/2), height = (20/68) * y, width = (20/68) * y, angle = -90, theta1 = 215, theta2 = 325, color = "black", lw=linewidth1)
    penCircle2 = Arc(((11/105) * x, y/2), height = (20/68) * y, width = (20/68) * y, angle = -90, theta1 = 35, theta2 = 145, color = "black", lw=linewidth1)
    
    centreCircle = Arc((x/2, y/2), height = (20/68) * y, width = (20/68) * y, angle = 360, theta1 = 0, theta2 = 360, color = "black", lw=linewidth1)
    halfWayLine = ConnectionPatch((x/2,0), (x/2, y), coordsA='data', linewidth=linewidth1, linestyle='solid', color=c1)
    
    # l1 = ConnectionPatch((x/3,0), (x/3, y), coordsA='data', linewidth=linewidth2, linestyle='--', color=c2, zorder=-2)
    # l2 = ConnectionPatch((2*x/3,0), (2*x/3,y), coordsA='data', linewidth=linewidth2, linestyle='--', color=c2, zorder=-2)

    # l3 = ConnectionPatch((0, y * 14/68), (x - x * 16.5/105, y * 14/68), coordsA='data', linewidth=linewidth2, linestyle='--', color=c2, zorder=-2)
    # l4 = ConnectionPatch((0, y * 24/68), (x - x * 5.5/105, y * 24/68), coordsA='data', linewidth=linewidth2, linestyle='--', color=c2, zorder=-2)
    # l5 = ConnectionPatch((0, y * 44/68), (x - x * 5.5/105, y * 44/68), coordsA='data', linewidth=linewidth2, linestyle='--', color=c2, zorder=-2)
    # l6 = ConnectionPatch((0, y * 54/68), (x - x * 16.5/105, y * 54/68), coordsA='data', linewidth=linewidth2, linestyle='--', color=c2, zorder=-2)

    court_elements = [pitch, 
                      goal1, goal2,
                      penBox1, penBox2, penSpot1, penSpot2, penCircle1, penCircle2,
                      fiveYard1, fiveYard2,
                      centreCircle, halfWayLine,]
                      # l1, l2, l3, l4, l5, l6]
    
    for element in court_elements:
        ax.add_patch(element)

    # Add zones
    num_zones_x = 6
    num_zones_y = 3
    for i in range(1, num_zones_x):
        plt.plot([i * x / num_zones_x, i * x / num_zones_x], [0, y], color=c2, linewidth=linewidth2, linestyle='--')
    for i in range(1, num_zones_y):
        plt.plot([0, x], [i * y / num_zones_y, i * y / num_zones_y], color=c2, linewidth=linewidth2, linestyle='--')

    if pitchcolor==1:
        plt.fill([x,0,0,x], [0,0,y,y], color = '#e5ece3', zorder=-5)
        plt.fill([2*x/3,x/3,x/3,2*x/3], [0,0,y/2 - (20/68) * y,y/2 - (20/68) * y], color = '#d0d9cd', zorder = -4)
        plt.fill([2*x/3,x/3,x/3,2*x/3], [y/2 - (10/68) * y,y/2 - (10/68) * y,y/2 + (10/68) * y,y/2 + (10/68) * y], color = '#d0d9cd', zorder = -4)
        plt.fill([2*x/3,x/3,x/3,2*x/3], [y/2 + (20/68) * y,y/2 + (20/68) * y,y,y], color = '#d0d9cd', zorder = -4)
        plt.fill([x,0,0,x], [y/2 + (10/68) * y,y/2 + (10/68) * y,y/2 + (20/68) * y,y/2 + (20/68) * y], color = '#d0d9cd', zorder = -4)
        plt.fill([x,0,0,x], [y/2 - (20/68) * y,y/2 - (20/68) * y,y/2 - (10/68) * y,y/2 - (10/68) * y], color = '#d0d9cd', zorder = -4)
        plt.fill([2*x/3,x/3,x/3,2*x/3], [y/2 - (20/68) * y,y/2 - (20/68) * y,y/2 - (10/68) * y,y/2 - (10/68) * y], color = '#b2c0aa', zorder = -3)
        plt.fill([2*x/3,x/3,x/3,2*x/3], [y/2 + (10/68) * y,y/2 + (10/68) * y,y/2 + (20/68) * y,y/2 + (20/68) * y], color = '#b2c0aa', zorder = -3)

    plt.axis('scaled')
    
    ax.set_xlim(-10, x + 10)
    ax.set_ylim(-10, y + 10)
    
    # fig.patch.set_facecolor('blue')
    # fig.patch.set_alpha(0)
    
    ax.axis('off')    
    return fig, ax

# drawPitch()

def drawOffHalfPitch(ax=None, x=120, y=80, c1='black', c2='grey', linewidth1=2, linewidth2=1, pitchcolor=1):
    fig = plt.figure()
    
    if ax is None:
        ax = plt.gca()
        
    halfPitch = Rectangle((0,0), y, x/2, linewidth=linewidth1 * 2, color=c1, fill=False, zorder = -1)
    
    goal = Rectangle(((y - y * 7.32/68)/2, x/2), y * 7.32/68, 1.5, linewidth=linewidth1 * 2, color=c1, fill=False, zorder = -1)
    
    penBox = Rectangle((y * 14/68, x/2 - x * 16.5/105), y * 40/68, x * 16.5/105, linewidth=linewidth1, color=c1, fill=False, zorder = -1)
    fiveYard = Rectangle((y * 24/68, x/2 - x * 5.5/105), y * 20/68, x * 5.5/105, linewidth=linewidth1, color=c1, fill=False, zorder = -1)

    penSpot = Circle((y/2, x/2 - (11/105) * x),0.25,color=c1, zorder = -1)
    penCircle = Arc((y/2, x/2 - (11/105) * x), height = (20/68) * y, width = (20/68) * y, angle = 360, theta1 = 215, theta2 = 325, color = c1, lw=linewidth1, zorder = -1)
    centreCircle = Arc((y/2, 0), height = (20/68) * y, width = (20/68) * y, angle = 180, theta1 = 180, theta2 = 360, color = c1, lw=linewidth1, zorder = -1)
    
    l1 = ConnectionPatch((0,x/6), (y, x/6), coordsA='data', linewidth=linewidth2, linestyle='--', color=c2, zorder = -2)
    l2 = ConnectionPatch((y * 14/68, 0), (y * 14/68, x/2 - x * 16.5/105), coordsA='data', linewidth=linewidth2, linestyle='--', color=c2, zorder = -2)
    l3 = ConnectionPatch((y * 24/68, 0), (y * 24/68, x/2 - x * 5.5/105), coordsA='data', linewidth=linewidth2, linestyle='--', color=c2, zorder = -2)
    l4 = ConnectionPatch((y * 44/68, 0), (y * 44/68, x/2 - x * 5.5/105), coordsA='data', linewidth=linewidth2, linestyle='--', color=c2, zorder = -2)
    l5 = ConnectionPatch((y * 54/68, 0), (y * 54/68, x/2 - x * 16.5/105), coordsA='data', linewidth=linewidth2, linestyle='--', color=c2, zorder = -2)

    court_elements = [halfPitch, goal, penBox, fiveYard, penSpot, penCircle, centreCircle,
                      l1, l2, l3, l4, l5]
    
    for element in court_elements:
        ax.add_patch(element)
    
    if pitchcolor==1:
        plt.fill([y,0,0,y], [0,0,x/2,x/2], color = '#e5ece3', zorder=-5)
        plt.fill([0,0,y,y], [0,x/6,x/6,0], color = '#d0d9cd', zorder = -4)
        plt.fill([y/2 - (10/68) * y,y/2 - (10/68) * y,y/2 - (20/68) * y,y/2 - (20/68) * y], [0,x/2,x/2,0], color = '#d0d9cd', zorder = -4)
        plt.fill([y/2 + (10/68) * y,y/2 + (10/68) * y,y/2 + (20/68) * y,y/2 + (20/68) * y], [0,x/2,x/2,0], color = '#d0d9cd', zorder = -4)
        plt.fill([y/2 - (10/68) * y,y/2 - (10/68) * y,y/2 - (20/68) * y,y/2 - (20/68) * y], [0,x/6,x/6,0], color = '#b2c0aa', zorder = -3)
        plt.fill([y/2 + (10/68) * y,y/2 + (10/68) * y,y/2 + (20/68) * y,y/2 + (20/68) * y], [0,x/6,x/6,0], color = '#b2c0aa', zorder = -3)
        
    plt.axis('scaled')

    ax.set_xlim(-5, y + 5)
    ax.set_ylim(-5, x/2 + 5)
    
    # fig.patch.set_facecolor('blue')
    # fig.patch.set_alpha(0)
    
    ax.axis('off')    
    return fig, ax

# drawOffHalfPitch()
