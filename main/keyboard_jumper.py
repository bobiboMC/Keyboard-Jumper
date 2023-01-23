import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd
import constants
import random
import time
import math
from decimal import Decimal, ROUND_UP
import rotation as rtt

font_primary=constants.FONT_PRIMARY
G=10.0 
V_0=60 
MODE='NORMAL' #SPIN -jumping and spinning rect,NORMAL-only jumping rect
words_to_type=['dad','mom','back','snake','rock']
total_height=0
temp_height=0
my_state='ground'
t=0
t_down=0

def on_closing(top):
        top.destroy()

#play again the game
def play_again(frame,canvas,id_rect,showed_label,L_wrong,area_typing,height_canvas,num_of_edges,event):
    area_typing.delete('1.0',tk.END)
    area_typing.config(state= "disabled")
    s = ttk.Style()
    s.configure('my.TButton', font=font_primary)
    play_again = ttk.Button(frame,text='Play Again?',style='my.TButton') #padding=-5 for example reduce padding
    play_again.grid(row=0,column=2)

    #disable +1 -1 tags
    mode_tag(frame,'disable',None,'inc','dec')
    play_again.bind("<Button-1>",lambda event:activate_game(frame,canvas,id_rect,height_canvas,
                                                            showed_label,L_wrong,area_typing,
                                                            time.time(),num_of_edges,event))

#check I the typed word is correct to the word that is showing on screen    
def check(event,word,canvas,frame,id_rect,showed_label,
          area_typing,L_wrong,removable_words_to_type,start_typing,height_canvas,num_of_edges):
    global t_add
    global to_add_total
    global my_state
    global temp_height
    global total_height
    global universal_t
    global t
    if word[:len(word)-1]==showed_label.cget('text')[:len(word)-1]: #start of word
        if word[:len(word)-1]==showed_label.cget('text'):#same word
            if word==showed_label.cget('text')+'\n': #write correct word
                if my_state=='ground':
                        t=0
                        temp_height=0
                        my_state='air'
                        animate_up(canvas,id_rect,height_canvas,temp_height)
                elif my_state=='air':
                        t=0
                        temp_height+=total_height
                elif my_state=='falling':
                        my_state='air'
                        temp_height=0
                        t=0
                        temp_height+=total_height
                        temp_height=467.5-temp_height
                #remove word from the word's list
                removable_words_to_type.remove(showed_label.cget('text'))
                #check how many words left to game over
                if len(removable_words_to_type)==0:
                    area_typing.unbind('<KeyRelease>')
                    end_typing=time.time()                    
                    showed_label.config(text=round( (end_typing-start_typing),5))
                    play_again(frame,canvas,id_rect,showed_label,L_wrong,area_typing,height_canvas,num_of_edges,event)
                else:
                        #set new label
                        ind_words=random.randint(0,len(removable_words_to_type)-1)
                        showed_label.config(text=removable_words_to_type[ind_words])

                        #create new binding of new word and reset old typing
                        area_typing.delete('1.0',tk.END) #1.0=from first line to tk.END=end line
                        area_typing.unbind('<KeyRelease>')
                        area_typing.bind('<KeyRelease>',lambda event:check(event,area_typing.get("1.0",tk.END),canvas,frame,
                                                                           id_rect,showed_label,area_typing,L_wrong,
                                                                           removable_words_to_type,start_typing,height_canvas,num_of_edges))
    elif event.keysym!='BackSpace': #wrong start of word,not earasing word
            num_wrong=int(L_wrong.cget('text'))+1
            L_wrong.config(text=str(num_wrong))
            if num_wrong==3: #number of wrong typing to fail,show game over+(clear,disable) area typing
                showed_label.config(text='GAME OVER')
                play_again(frame,canvas,id_rect,showed_label,L_wrong,area_typing,height_canvas,num_of_edges,event)
                

#active/reactive the typing game
def activate_game(frame,canvas,id_rect,height_canvas,L_to_type,L_wrong_type,
                  T_to_type,start_typing,num_of_edges,event=None):
        global my_state
        global t
        global temp_height
        global counter
        
        #print(canvas.coords(id_rect)[1],'activ')
        if event:
                if '1' not in (event.widget)['text']:
                        event.widget.destroy()
                        mode_tag(frame,'normal',
                                 lambda event:activate_game(frame,canvas,id_rect,
                                 height_canvas,L_to_type,L_wrong_type,
                                 T_to_type,start_typing,num_of_edges,
                                 event),
                                 'inc','dec')
                else:
                        x0_poly=(300+400)/2
                        canvas.delete(id_rect)
                        if '+' in (event.widget)['text']:
                                id_rect=rtt.symmetric_polygon(x0_poly,canvas,num_of_edges+1,50)
                                num_of_edges+=1
                        elif '-' in (event.widget)['text']:
                                id_rect=rtt.symmetric_polygon(x0_poly,canvas,num_of_edges-1,50)
                                num_of_edges-=1
                        

                        mode_tag(frame,'normal',
                                 lambda event:activate_game(frame,canvas,id_rect,
                                 height_canvas,L_to_type,L_wrong_type,
                                 T_to_type,start_typing,num_of_edges,
                                 event),
                                 'inc','dec')

        counter=0
        temp_height=0
        t=0
        my_state=='ground'
        canvas.move(id_rect,0,467.5-canvas.coords(id_rect)[1])
        
        root.bind("<space>",lambda event:animate_up(canvas,id_rect,0,height_canvas))                            
        removable_words_to_type=list(words_to_type)
        ind_words=random.randint(0,len(removable_words_to_type)-1)
        L_to_type.config(text= removable_words_to_type[ind_words])
        L_wrong_type.config(text= '0')
        T_to_type.config(state='normal')
        T_to_type.unbind('<KeyRelease>')
        T_to_type.bind('<KeyRelease>',lambda event:check(event,T_to_type.get("1.0",tk.END),canvas,frame,
                                                                         id_rect,L_to_type,T_to_type,
                                                                         L_wrong_type,removable_words_to_type,
                                                                         start_typing,height_canvas,
                                                                         num_of_edges))

#start screen of game passive(not changed)        
def game_design(event,frame,to_delete_1,to_delete_2,num_of_edges):
    width_canvas=700
    height_canvas=500
    to_delete_1.destroy()
    to_delete_2.destroy()
    width_screen= root.winfo_screenwidth() -200  #get my_screen_width-200            
    height_screen= root.winfo_screenheight()-200 #get my_screen_height-200
    root.geometry("%dx%d" % (width_screen, height_screen))
        
    canvas = tk.Canvas(frame, bg='black',width=width_canvas,height=height_canvas)
    canvas.grid(row=2,column=0,columnspan=6)
    #jumper polygon or rectangle
    x0_poly,y0_poly=(300+400)/2,(370+470)/2 #350,420
    id_rect=rtt.symmetric_polygon(x0_poly,canvas,num_of_edges,50)
    #platform
    canvas.create_line(0, 0.5*height_canvas+220, width_canvas, 0.5*height_canvas+220,fill="green", width=5)

    #show word to type
    L_to_type = tk.Label(frame,font=font_primary,borderwidth=2,relief="solid",padx=2)
    L_to_type.grid(row=0,column=3)
    #show wrong answers
    L_wrong_type = tk.Label(frame,font=font_primary,borderwidth=2,relief="solid",fg='red')
    L_wrong_type.grid(row=0,column=0)
    #area to type
    T_to_type = tk.Text(frame, height = 1, width = 10,font=font_primary)
    T_to_type.grid(row=0,column=1)
    T_to_type.bind('<KeyRelease>',lambda event:check(event,T_to_type.get("1.0",tk.END),canvas,frame,
                        id_rect,num_off,L_to_type,T_to_type,L_wrong_type,removable_words_to_type,start_typing,height_canvas))
        
    #increase and decrease edges,update canvas
    increase_edge = tk.Button(frame,borderwidth=2,text='+1',font=font_primary,relief="solid")
    increase_edge.grid(row=0, column=4,sticky='news')

    decrease_edge = tk.Button(frame,borderwidth=2,text='-1',font=font_primary,relief="solid")
    decrease_edge.grid(row=0, column=5,sticky='news')

    increase_edge.tag='inc' #create attr for recognize +1
    decrease_edge.tag='dec' #create attr for recognize -1

    increase_edge.bind("<Button-1>",lambda event:activate_game(frame,canvas,id_rect,height_canvas,
                                                                   L_to_type,L_wrong_type,T_to_type,
                                                                   start_typing,num_of_edges,event
                                                                   ))
    decrease_edge.bind("<Button-1>",lambda event:activate_game(frame,canvas,id_rect,height_canvas,
                                                                   L_to_type,L_wrong_type,T_to_type,
                                                                   start_typing,num_of_edges,event,
                                                                   ))

    root.bind("<space>",lambda event:animate_up(canvas,id_rect,0,height_canvas))    
    #start timer of current game
    start_typing = time.time()
    activate_game(frame,canvas,id_rect,height_canvas,L_to_type,L_wrong_type,T_to_type,start_typing,num_of_edges)


#change state of  buttons/items and rebind buttons/items if needed        
def mode_tag(frame,mode,callback,*tags): #get unknown list of tags
        for child in frame.winfo_children():
            for tag in tags:
                    if hasattr(child, 'tag') and child.tag == tag:
                        if mode=='disable': #unbind button
                                child.unbind("<Button-1>")
                        elif mode=='normal': #bund button
                                child.bind("<Button-1>",callback)
                        child.configure(state=mode)


#jumping                
def animate_up(canvas,id_rect,height_canvas,old_h_t):
    global total_height
    global my_state
    global temp_height
    global t
    global t_down
    if t<V_0/G : #jumping,max height   
        t+=(V_0/G)/30 #18=60*t-10*(0.5)*t^2 --> 36-120t+10t^2=0
        t=round(t,2)      
        new_h_t=temp_height+V_0*t-G*(t**2)/2
        diff_h_t=new_h_t-old_h_t #diff heights 
        total_height=new_h_t
        canvas.move(id_rect,0,-diff_h_t)
        old_h_t=new_h_t
        #spin rect
        if MODE=='SPIN': #spinning in the air               
                spin(canvas,id_rect)      
        root.after(10,lambda:animate_up(canvas,id_rect,height_canvas,old_h_t))      
    else: #calc time to fall down and activate fall down  
        t_to_fall=math.sqrt(old_h_t/(0.5*G))
        my_state='falling'
        t_down=0
        animate_down(canvas,id_rect,height_canvas,t_to_fall)        

#falling
def animate_down(canvas,id_rect,height_canvas,t_to_fall,old_h_t=0):
    global my_state
    global t_down
    global total_height
    if my_state=='falling':
            if t_down<t_to_fall and t_to_fall-t_down>0.1: #falling   
                t_down+=t_to_fall/30
                t_down=round(t_down,15)
                new_h_t=G*(t_down**2)/2
                h_t=new_h_t-old_h_t #diff heights
                old_h_t=new_h_t
                canvas.move(id_rect,0,h_t)
                total_height=canvas.coords(id_rect)[1]
                if MODE=='SPIN': #spinning in the air
                        spin(canvas,id_rect)   
                for k in range(0,len(canvas.coords(id_rect))-1,2):
                        if canvas.coords(id_rect)[k+1]>466.5:
                                break        
                root.after(10,lambda:animate_down(canvas,id_rect,height_canvas,t_to_fall,old_h_t))
            else:
                  my_state='ground'
                  return  
    elif my_state=='air':
        animate_up(canvas,id_rect,height_canvas,467.5-canvas.coords(id_rect)[1])
        

#spinning polygon
def spin(canvas,id_rect):
        vertices=[]
        for k in range(0,len(canvas.coords(id_rect))-1,2):
                x=canvas.coords(id_rect)[k]
                y=canvas.coords(id_rect)[k+1]
                vertices.append([x,y])

        _x_list = [vertex [0] for vertex in vertices]
        _y_list = [vertex [1] for vertex in vertices]
        len_vertices = len(vertices)
        mid_x_rect = sum(_x_list) / len_vertices
        mid_y_rect = sum(_y_list) / len_vertices

        center = (mid_x_rect, mid_y_rect)
        new_square = rtt.rotate(vertices, 18, center)
        squares=[]
        for p in range(0,len(new_square)):
                x=new_square[p][0]
                y=new_square[p][1]
                squares.append(x)
                squares.append(y)

        canvas.coords(id_rect, squares)

#opening_screen
def main():
    frame = tk.Frame(root)
    frame.pack(side=tk.BOTTOM)
    opening_game = tk.Label(frame, text= 'Welcome To Keyboard Jumper!',font=font_primary,borderwidth=2,relief="solid")
    opening_game.grid(row=0, column=0,sticky='news')

    enter_game = tk.Button(frame,borderwidth=2,text='Click Here To Enter The Game',relief="solid")
    enter_game.bind("<Button-1>",lambda event,:game_design(event,frame,opening_game,enter_game,4))
    enter_game.grid(row=1, column=0,sticky='news')
    
    
    #start count of typing speed        
    root.mainloop()

    
if __name__ == '__main__':
    #basic config root
    root = tk.Tk()
    root.configure(bg='gray')
    root.title("main menu")    
    main()    


#https://codereview.stackexchange.com/questions/175813/python-tkinter-bouncing-ball-animation  
