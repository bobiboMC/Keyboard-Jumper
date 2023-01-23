import tkinter as tk
import math

def rotate(points, angle, center):
    angle = math.radians(angle)
    cos_val = math.cos(angle)
    sin_val = math.sin(angle)
    cx, cy = center
    new_points =[]
    for x_old, y_old in points:
        x_old -= cx
        y_old -= cy
        x_new = x_old * cos_val - y_old * sin_val
        y_new = x_old * sin_val + y_old * cos_val
        new_points.append([x_new + cx, y_new + cy])
    return new_points

#platform placing fixing after rotate,with height platform 470
def rotate_fixed(points, angle, center):
    angle = math.radians(angle)
    cos_val = math.cos(angle)
    sin_val = math.sin(angle)
    cx, cy = center
    new_points =[]
    i=0 #index for inc
    inc=0 #init
    for x_old, y_old in points:
        x_old -= cx
        y_old -= cy
        x_new = x_old * cos_val - y_old * sin_val
        y_new = x_old * sin_val + y_old * cos_val
        if i==0:
            inc=467.5-(y_new + cy) #width=5,line start from center,2.5px each side
            i+=1
        new_points.append([x_new + cx, y_new + cy+inc])
    return new_points

def symmetric_polygon(start_point_x,canvas,amount_points,len_edge):
    #create points of polygon
    start_point_y=0
    angle = math.radians(360/amount_points)
    cos_val = math.cos(angle)
    sin_val = math.sin(angle)
    new_points = []
    for i in range(0,amount_points):
        if i==0:
           start_point_y=467.5-math.sin(angle * (i+1)) * len_edge
           py = math.sin(angle * (i+1)) * len_edge + start_point_y
        else:
           py = math.sin(angle * (i+1)) * len_edge + start_point_y
        px = math.cos(angle * (i+1)) * len_edge + start_point_x
        new_points.append([px,py])


    center=(start_point_x,start_point_y)
    angle_for_roatate=(180-(360/amount_points))/2
    new_rotated_poly=rotate_fixed(new_points ,angle_for_roatate,center)
    id_obj=canvas.create_polygon(new_rotated_poly,fill='red')
    return id_obj


