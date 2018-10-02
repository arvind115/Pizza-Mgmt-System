try:                        # for Python 3
    from tkinter import *
    from tkinter import messagebox
    from tkinter.tix import *
except ImportError:         # for Python 2
    from Tkinter import *
    from Tkinter import messagebox
    from Tkinter.tix import *
from PIL import ImageTk,Image
from sqlite3 import *
import requests,json #for location
import smtplib  # for email
import math
from functools import partial # for mouse events

s=Tk()
s.title('Pizza Palace')
s.geometry("1900x900")

class Login:
    def __init__(sf):
        #######################      connect to database     #############################
        sf.c=connect("mydata.db")
        sf.cur=sf.c.cursor()
        try:
            sf.cur.execute("create table staff(name varchar(50),user varchar(50),passw varchar(50),email varchar(50))")
        except:
            pass
        #####################       flush list []           #############################
        sf.l=[] # It keeps all the widgets & destroys them whenever user moves to a new window
        ########################     GUI window             #############################
        sf.scr=s
        sf.scr.configure(bg='white')
        sf.f=Frame(sf.scr,bg='white')
        sf.f.place(x=0,y=0,width=1900,height=900)
       
        #   CANVAS  for image
        sf.canvas=Canvas(sf.f,bg='PeachPuff',bd=-2)
        sf.canvas.place(x=0,y=36,width=1900,height=705)  # previous height=125 
        sf.img=ImageTk.PhotoImage(Image.open('background_.jpg'))
        sf.canvas.create_image(681,405,image=sf.img)
        sf.l.append(sf.canvas)
   
        #   USERNAME label
        sf.username=Label(sf.f,text='Username')
        sf.username.place(x=300,y=130,width=110,height=25)
        sf.l.append(sf.username)

        #  USERNAME entry_field
        sf.un_entry=Entry(sf.f,bg='azure')
        sf.un_entry.place(x=440,y=130,width=200,height=25)
        sf.l.append(sf.un_entry)

        #   PASSWORD label
        sf.passw=Label(sf.f,text='Password')
        sf.passw.place(x=300,y=175,width=110,height=25)
        sf.l.append(sf.passw)

        #   PASSWORD entry_field
        sf.p_entry=Entry(sf.f,show="*",bg='azure')
        sf.p_entry.place(x=440,y=175,width=200,height=25)
        sf.l.append(sf.p_entry)
        
        #   SUBMIT button
        sf.submit=Button(sf.f,text='LOGIN',command=lambda:sf.result("login"))
        sf.submit.place(x=300,y=230,width=100,height=28)
        sf.l.append(sf.submit)
                
        #   REGISTER button
        sf.r=Button(sf.f,text='REGISTER',command=sf.register)
        sf.r.place(x=440,y=230,width=130,height=28)
        sf.l.append(sf.r)

        sf.ITEMS=0
        sf.TOTAL=0 
        sf.dict={}   #######   dictionary to keep track of Pizzas selected     ######
        sf.dict['1']=['MAREGHERIA',{'R':0,'M':0,'L':0},False]
        sf.dict['2']=['DOUBLE CHEESE MARGHERITA',{'R':0,'M':0,'L':0},False]
        sf.dict['3']=['FARM HOUSE',{'R':0,'M':0,'L':0},False]
        sf.dict['4']=['PEPPY PANEER',{'R':0,'M':0,'L':0},False]
        sf.dict['5']=['MEXICAN GREEN WAVE',{'R':0,'M':0,'L':0},False]
        sf.dict['6']=['DELUXE VEGGIE',{'R':0,'M':0,'L':0},False]
        sf.dict['7']=['5 PEPPER',{'R':0,'M':0,'L':0},False]
        sf.dict['8']=['VEG EXTRAVAGANZA',{'R':0,'M':0,'L':0},False]
        sf.dict['9']=['CHEESE N CORN',{'R':0,'M':0,'L':0},False]
        sf.dict['10']=['PANEER MAKHANI',{'R':0,'M':0,'L':0},False]
        sf.dict['11']=['VEGGIE PARADISE',{'R':0,'M':0,'L':0},False]
        sf.dict['12']=['FRESH VEGGIE',{'R':0,'M':0,'L':0},False]

        sf.D={}
        sf.D['1']=[False,'Coca Cola',84]
        sf.D['2']=[False,'Pepsi',80]
        sf.D['3']=[False,'Sprite',81]
        sf.D['4']=[False,'Mountain Dew',86]
        sf.D['5']=[False,'Fanta',78]
        sf.D['6']=[False,'Thums Up',84]

        sf.M={}
        sf.M['1']=[False,'Salsa Verde Enchiladas',449]
        sf.M['2']=[False,'Hawaiian Poke Bowl',490]
        sf.M['3']=[False,'California Chicken Bar',399]
        sf.M['4']=[False,'Bruchetta Salmon',549]

        sf.P={'R':0,'M':0,'L':0}    #### dict to keep count of total pizzas of each type ####

        sf.R1=IntVar()              #### 'REGULAR' variables  ####
        sf.R2=IntVar()
        sf.R3=IntVar()
        sf.R4=IntVar()
        sf.R5=IntVar()
        sf.R6=IntVar()
        sf.R7=IntVar()
        sf.R8=IntVar()
        sf.R9=IntVar()
        sf.R10=IntVar()
        sf.R11=IntVar()
        sf.R12=IntVar()
        sf.__R__=['0',sf.R1,sf.R2,sf.R3,sf.R4,sf.R5,sf.R6,sf.R7,sf.R8,sf.R9,sf.R10,sf.R11,sf.R12]

        sf.M1=IntVar()              #### 'MEDIUM' variable ####
        sf.M2=IntVar()
        sf.M3=IntVar()
        sf.M4=IntVar()
        sf.M5=IntVar()
        sf.M6=IntVar()
        sf.M7=IntVar()
        sf.M8=IntVar()
        sf.M9=IntVar()
        sf.M10=IntVar()
        sf.M11=IntVar()
        sf.M12=IntVar()
        sf.__M__=['0',sf.M1,sf.M2,sf.M3,sf.M4,sf.M5,sf.M6,sf.M7,sf.M8,sf.M9,sf.M10,sf.M11,sf.M12]
        
        sf.L1=IntVar()              #### 'LARGE' variables ####
        sf.L2=IntVar()
        sf.L3=IntVar()
        sf.L4=IntVar()
        sf.L5=IntVar()
        sf.L6=IntVar()
        sf.L7=IntVar()
        sf.L8=IntVar()
        sf.L9=IntVar()
        sf.L10=IntVar()
        sf.L11=IntVar()
        sf.L12=IntVar()
        sf.__L__=['0',sf.L1,sf.L2,sf.L3,sf.L4,sf.L5,sf.L6,sf.L7,sf.L8,sf.L9,sf.L10,sf.L11,sf.L12]
        
        sf.scr.mainloop()

    ######################    register() fuction signs up a new user      ####################    
    
    def register(sf):
        try:
            sf.flush()
        except:
            try:
                sf.flush()
            except:
                pass
        sf.f.config(bg='medium spring green')

        #   CANVAS  for image
        sf.canvas=Canvas(sf.f,bg='PeachPuff',bd=-2)
        sf.canvas.place(x=0,y=0,width=1900,height=850)  # previous height=125 
        sf.img=ImageTk.PhotoImage(Image.open('background.jpg'))
        sf.canvas.create_image(681,405,image=sf.img)
        sf.l.append(sf.canvas)
            
        #   NAME label
        sf.Name=Label(sf.f,text='Name')
        sf.Name.place(x=400,y=100,width=110,height=25)
        sf.l.append(sf.Name)

        #   NAME entry
        sf.N_entry=Entry(sf.f)
        sf.N_entry.place(x=540,y=100,width=200,height=25)
        sf.l.append(sf.N_entry)

        #   USERNAME label
        sf.name=Label(sf.f,text='Userame')
        sf.name.place(x=400,y=140,width=110,height=25)
        sf.l.append(sf.name)

        #  USERNAME entry_field
        sf.n_entry=Entry(sf.f)
        sf.n_entry.place(x=540,y=140,width=200,height=25)
        sf.l.append(sf.n_entry)

        #   PASSWORD label
        sf.plabel=Label(sf.f,text='Password')
        sf.plabel.place(x=400,y=180,width=110,height=25)
        sf.l.append(sf.plabel)

        #   PASSWORD entry_field
        sf.p_entry=Entry(sf.f,show="*")
        sf.p_entry.place(x=540,y=180,width=200,height=25)
        sf.l.append(sf.p_entry)

        #   PASSWORD2 label
        sf.plabel2=Label(sf.f,text='Retype password')
        sf.plabel2.place(x=400,y=220,width=110,height=25)
        sf.l.append(sf.plabel2)

         #   PASSWORD entry_field
        sf.p_entry2=Entry(sf.f,show="*")
        sf.p_entry2.place(x=540,y=220,width=200,height=25)
        sf.l.append(sf.p_entry2)

        #   EMAIL field
        sf.e_mail=Label(sf.f,text="Email")
        sf.e_mail.place(x=400,y=260,width=110,height=25)
        sf.l.append(sf.e_mail)

        #   EMAIL entry_field
        sf.e_entry=Entry(sf.f)
        sf.e_entry.place(x=540,y=260,width=200,height=25)
        sf.l.append(sf.e_entry)

        #   REGISTER button
        sf.rbutton=Button(sf.f,text='REGISTER ME',command=lambda:sf.result("register"))
        sf.rbutton.place(x=460,y=300,width=110,height=31)
        sf.l.append(sf.rbutton)

        sf.scr.mainloop()

    ####################    flush() function destroys all the widgets of the frame      ####################
    def flush(sf):
        for i in sf.l:
            i.destroy()
        sf.l=[]

    def result(sf,val):
        if val=="login":
            if not len(sf.un_entry.get()) or not len(sf.p_entry.get()): # login details not given
                messagebox.showinfo("Invalid credentials","Please fill both the fields to continue.\nPlease try again.")
            else:  #check for correct username
                x=sf.cur.execute("select count(*) from staff where user=%r"%(sf.un_entry.get()))
                if list(x)[0][0]==0:  #entered username doesn't exist
                    messagebox.showinfo("Invalid credentials.","Username %r doesn't exist.\nPlease 'register' to continue."%(sf.un_entry.get())) #wrong username
                    sf.__init__()
                else:  #username exists, check for correct password now
                    sf.MAIL=list(sf.cur.execute("select email from staff where user=%r"%(sf.un_entry.get())))[0][0]
                    sf.NAME=list(sf.cur.execute("select name from staff where user=%r"%(sf.un_entry.get())))[0][0]
                    print(sf.NAME)
                    x=sf.cur.execute("select count(*) from staff where passw=%r"%(sf.p_entry.get())) #checking for correct password
                    if list(x)[0][0]:       # correct password, grant access to order.
                        sf.create_order('1')
                    else:                  # wrong password
                        messagebox.showinfo("Wrong password","Please enter a valid password\nForgot password ?")
                        sf.rbutton=Button(sf.scr,text='Recover my password',command=sf.recover_password)
                        sf.rbutton.place(x=720,y=210,width=130,height=30)
                        sf.l.append(sf.rbutton)
        elif val=="register":
            if not len(sf.n_entry.get()) or not len(sf.N_entry.get()) or not len(sf.p_entry.get()) or not len(sf.p_entry2.get()) or not len(sf.e_entry.get()): # no username given
                messagebox.showinfo("Missing details","Please fill all the fields to continue.")
            else:                           #check for validity of data
                if sf.p_entry.get()==sf.p_entry2.get(): #both passwords are same,check for availability of username.
                    x=sf.cur.execute("select count(*) from staff where user=%r"%(sf.n_entry.get()))
                    if list(x)[0][0]!=0:   # username already taken.
                        messagebox.showinfo("Oops !","Username %r already exists.\nPlease try another one."%(sf.n_entry.get())) 
                    else:                   # username available.
                        try:
                            sf.cur.execute("insert into staff values(%r,%r,%r,%r)"%(sf.N_entry.get(),sf.n_entry.get(),sf.p_entry2.get(),sf.e_entry.get()))
                            sf.c.commit()
                            messagebox.showinfo("Info","You've been successfully registered\nRedirecting to LOGIN window")
                            sf.flush()
                            sf.__init__() #registration done.... redirect to 'login' window
                        except:
                             pass
                else:                     #passwords aren't same...reconstruct the 'register' window
                    messagebox.showinfo("Mismatched passwords","Both passwords should be same\nPlease try again.")
                    
    def recover_password(sf):
        try:
            sf.rbutton.destroy()
        except:
            sf.rbutton.destroy()
        try:
            mail=list(sf.cur.execute("select email from staff where user=%r and name=%r"%(sf.un_entry.get(),sf.NAME)))[0][0]
            sf.mail=mail
            password=list(sf.cur.execute("select passw from staff where name=%r"%(sf.NAME)))[0][0]
            server=smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()
            server.login('arvind.singh_cs16@gla.ac.in','9627803108')
            msg='Hello '+sf.NAME+'\nYour password for Pizza Palace is '+''+password+''
            server.sendmail('arvind.singh_cs16@gla.ac.in',mail,msg)
            print('mail sent')
            server.close()
            messagebox.showinfo('Info','Dear '+sf.NAME+', your password has been sent to '+mail+'\nPlease try again using the correct password.')
        except:
            messagebox.showinfo('Erro',"Your password couldn't be sent.Please check your internet connection.")
        sf.flush()
        sf.__init__()
        
    def myfunction(sf,event):
        sf.canvas.configure(scrollregion=sf.canvas.bbox("all"),width=1338,height=670) ## 'width' & 'height' are actual scrollable frame size.
    
    def func(sf,val):
        if sf.dict[val][1]['R']==0 and sf.dict[val][1]['M']==0 and sf.dict[val][1]['L']==0:
            messagebox.showinfo('Message','Please select a size before adding pizza to the cart')
        else: #some size has been selected...
            if sf.__labels__[int(val)]['text']=='REMOVE': #remove from cart
                sf.dict[val][2]=False
                if sf.dict[val][1]['R']==1:
                    sf.dict[val][1]['R']=0
                    sf.P['R']-=1
                    sf.TOTAL-=205
                    sf.ITEMS-=1
                    sf.__R__[int(val)].set(0)
                if sf.dict[val][1]['M']==1:
                    sf.dict[val][1]['M']=0
                    sf.P['M']-=1
                    sf.TOTAL-=385
                    sf.ITEMS-=1
                    sf.__M__[int(val)].set(0)
                if sf.dict[val][1]['L']==1:
                    sf.dict[val][1]['L']=0
                    sf.P['L']-=1
                    sf.TOTAL-=595
                    sf.ITEMS-=1
                    sf.__L__[int(val)].set(0)
                sf.__labels__[int(val)].config(text='ADD TO CART',fg='white')
            else: #add to cart
                sf.dict[val][2]=True
                if sf.dict[val][1]['R']==1:
                    sf.P['R']+=1
                    sf.TOTAL+=205
                    sf.ITEMS+=1
                if sf.dict[val][1]['M']==1:
                    sf.P['M']+=1
                    sf.TOTAL+=385
                    sf.ITEMS+=1
                if sf.dict[val][1]['L']==1:
                    sf.P['L']+=1
                    sf.TOTAL+=595
                    sf.ITEMS+=1
                sf.__labels__[int(val)].config(text='REMOVE',fg='SpringGreen2')
            sf.tl2.config(text=str(sf.ITEMS))
            sf.tl.config(text='TOTAL='+str(sf.TOTAL)+' \u20B9') #total amount

    def drink_cart(sf,val,price):
        if sf.__labels2__[int(val)]['text']=='REMOVE': #remove from cart
            sf.D[val][0]=False
            sf.TOTAL-=sf.D[val][2]
            sf.ITEMS-=1
            sf.__labels2__[int(val)].config(text='ADD TO CART',bg='light sea green',fg='white')
        else:  ## ADD TO CART ##
            sf.D[val][0]=True
            sf.TOTAL+=sf.D[val][2]
            sf.ITEMS+=1
            sf.__labels2__[int(val)].config(text='REMOVE',bg='light sea green',fg='black')
        sf.tl2.config(text=str(sf.ITEMS))  ## ITEMS ##
        sf.tl.config(text='TOTAL='+str(sf.TOTAL)+' \u20B9') #total amount
        
        
    def meals_func(sf,val,price):
        if sf.__labels3__[int(val)]['text']=='REMOVE': #remove from cart
            sf.M[val][0]=False
            sf.TOTAL-=sf.M[val][2]
            sf.ITEMS-=1
            sf.__labels3__[int(val)].config(text='ADD TO CART',bg='firebrick2',fg='gold')
        else:  ## ADD TO CART
            sf.M[val][0]=True
            sf.TOTAL+=sf.M[val][2]
            sf.ITEMS+=1
            sf.__labels3__[int(val)].config(text='REMOVE',bg='firebrick2',fg='black')
        sf.tl2.config(text=str(sf.ITEMS))  ## ITEMS ##
        sf.tl.config(text='TOTAL='+str(sf.TOTAL)+' \u20B9') #total amount
        
    def cbR(sf,R,val):                       ####################        checkbutton functions
        if R.get(): ## only 'set' when label reads 'ADD TO CART'
            if sf.__labels__[int(val)]['text']=='ADD TO CART':
                sf.__R__[int(val)].set(1)
                sf.dict[val][1]['R']=1
            else:   ## label reads 'REMOVE', then another checkbox has been clicked.
                sf.__R__[int(val)].set(0)
        else:
            if sf.__labels__[int(val)]['text']=='ADD TO CART':
                sf.__R__[int(val)].set(0)
                sf.dict[val][1]['R']=0
            else:
                sf.__R__[int(val)].set(1)
    def cbM(sf,M,val):
        if M.get():
            if sf.__labels__[int(val)]['text']=='ADD TO CART':
                sf.__M__[int(val)].set(1)
                sf.dict[val][1]['M']=1
            else:
                sf.__M__[int(val)].set(0)
        else:
            if sf.__labels__[int(val)]['text']=='ADD TO CART':
                sf.__M__[int(val)].set(0)
                sf.dict[val][1]['M']=0
            else:
                sf.__M__[int(val)].set(1)
    def cbL(sf,L,val):
        if L.get():
            if sf.__labels__[int(val)]['text']=='ADD TO CART':
                sf.__L__[int(val)].set(1)
                sf.dict[val][1]['L']=1
            else:
                sf.__L__[int(val)].set(0)
        else:
            if sf.__labels__[int(val)]['text']=='ADD TO CART':
                sf.__L__[int(val)].set(0)
                sf.dict[val][1]['L']=0
            else:
                sf.__L__[int(val)].set(1)
    
    def entry(sf,wel, color,event):                          # <<<<<< HOVERING >>>>>>   
        sf.wel.configure(background=color,foreground='white')
    def exit_(sf,wel, color, event):
        sf.wel.configure(background=color,foreground='red')
    def entryP(sf,pizza_label, color,event):
        sf.pizza_label.configure(background=color,foreground='red')
    def exitP(sf,pizza_label, color, event):
        sf.pizza_label.configure(background=color,foreground='white')
    def entryD(sf,drinks_label, color,event):
        sf.drinks_label.configure(background=color,foreground='red')
    def exitD(sf,drinks_label, color, event):
        sf.drinks_label.configure(background=color,foreground='white')
    def entryM(sf,meals_label, color,event):
        sf.meals_label.configure(background=color,foreground='red')
    def exitM(sf,meals_label, color, event):
        sf.meals_label.configure(background=color,foreground='white')
    def entryC(sf,pay, color,event):
        sf.pay.configure(background=color,foreground='white')
    def exitC(sf,pay, color, event):
        sf.pay.configure(background=color,foreground='medium aquamarine')
    
    def create_order(sf,val):
        sf.flush()
        sf.head=Canvas(sf.scr,bd=-2,bg='white')             #####   head canvas ######
        sf.head.place(x=0,y=0,width=1360,height=59)

        sf.wel=Label(sf.head,text='Welcome '+sf.NAME,fg='red',bg='white',font=('Serif 14 bold'))  ## WELCOME LABEL ##
        sf.wel.place(x=6,y=4,width=175,height=50)
        sf.wel.bind('<Enter>',partial(sf.entry,sf.wel,'red'))
        sf.wel.bind('<Leave>',partial(sf.exit_,sf.wel,'white'))
        sf.head.create_rectangle(5,3,181,54,outline='red',fill='white')
         
        sf.pizza_logo=PhotoImage(file='pizza_logo.png')  ## pizza logo  ##
        sf.head.create_image(193+20,29,image=sf.pizza_logo)
        sf.pizza_label=Label(sf.head,text='Pizzas',bg='red',fg='snow',font=('Sans 14 bold'))
        sf.pizza_label.place(x=255+20,y=8,width=90,height=44)
        sf.pizza_label.bind('<Button-1>',lambda val='1':sf.create_order('1'))
        sf.pizza_label.bind('<Enter>',partial(sf.entryP,sf.pizza_label,'white'))
        sf.pizza_label.bind('<Leave>',partial(sf.exitP,sf.pizza_label,'red'))
        sf.head.create_oval(237+20,9,273+20,51,fill='red',outline='red',width=2)
        sf.head.create_oval(237+90+20,9,273+90+20,51,fill='red',outline='red',width=2)

        sf.drinks_logo=PhotoImage(file='drinks_logo.png')  ## drinks logo ##
        sf.head.create_image(460+20,29,image=sf.drinks_logo)
        sf.drinks_label=Label(sf.head,text='Drinks',bg='red',fg='snow',font=('Sans 14 bold'))
        sf.drinks_label.place(x=523+20,y=8,width=90,height=44)
        sf.drinks_label.bind('<Button-1>',lambda val='1':sf.drinks('1'))
        sf.drinks_label.bind('<Enter>',partial(sf.entryD,sf.drinks_label,'white'))
        sf.drinks_label.bind('<Leave>',partial(sf.exitD,sf.drinks_label,'red'))
        sf.head.create_oval(505+20,9,541+20,51,fill='red',outline='red',width=2)
        sf.head.create_oval(505+90+20,9,541+90+20,51,fill='red',outline='red',width=2)

        sf.meals_logo=ImageTk.PhotoImage(Image.open('meals_logo.jpg'))  ## meals logo ##
        sf.head.create_image(727+20,29,image=sf.meals_logo)
        sf.meals_label=Label(sf.scr,text='Meals',bg='red',fg='snow',font=('Sans 14 bold'))
        sf.meals_label.place(x=795+20,y=8,width=90,height=44)
        sf.meals_label.bind('<Button-1>',lambda val='1':sf.meals('1'))
        sf.meals_label.bind('<Enter>',partial(sf.entryM,sf.meals_label,'white'))
        sf.meals_label.bind('<Leave>',partial(sf.exitM,sf.meals_label,'red'))
        sf.head.create_oval(782-5+20,9,818-5+20,51,fill='red',outline='red',width=2)
        sf.head.create_oval(782+90-5+20,9,818+90-5+20,51,fill='red',outline='red',width=2)

        sf.pay=Label(sf.scr,text='Checkout',fg='medium aquamarine',bg='snow',font=('Sans 14 bold')) ### checkout logo ##
        sf.pay.place(x=985,y=8,height=42,width=100)
        sf.pay.bind('<Button-1>',lambda val='1':sf.payment_window('1'))
        sf.pay.bind('<Enter>',partial(sf.entryC,sf.pay,'medium aquamarine'))
        sf.pay.bind('<Leave>',partial(sf.exitC,sf.pay,'white'))
        sf.head.create_rectangle(984,7,1085,50,fill='white',outline='medium aquamarine')
        sf.cart=PhotoImage(file='cart2.png')                                                 ## cart logo ##
        sf.head.create_image(1140,33,image=sf.cart)

        sf.tl2=Label(sf.head,bg='yellow',fg='black',text=sf.ITEMS,font=('Sans 11'))   ### NO OF ITEMS ## 
        sf.tl2.place(x=1141,y=8,width=17,height=15)
        sf.head.create_oval(1137,5,1162,25,fill='yellow',outline='yellow')
         
        sf.tl=Label(sf.scr,bg='brown1',fg='white',text='TOTAL=%d \u20B9'%(sf.TOTAL))   ####  run 'TOTAL AMOUNT' on a thread  ####
        sf.tl.place(x=1240,y=8,width=95,height=31)
         
        ''' sf.f is our PARENT FRAME '''          #################
        sf.f=Frame(sf.scr,relief=FLAT,width=690,height=900,bd=-2)
        sf.f.place(x=0,y=60)
        ''' PARENT frame will <<NOT>> be destroyed '''
        sf.canvas=Canvas(sf.f,bd=-2)
        ''' canvas will also <<NOT>> be destroyed '''
        sf.frame=Frame(sf.canvas,bd=-2,bg='white')
        sf.myscrollbar=Scrollbar(sf.f,orient=VERTICAL,command=sf.canvas.yview)   ####    SCROLL BAR   ####
        sf.canvas.configure(yscrollcommand=sf.myscrollbar.set)
        sf.myscrollbar.pack(side=RIGHT,fill=Y)

        sf.canvas.pack(side=LEFT)   
        sf.canvas.create_window((0,0),window=sf.frame)
        sf.frame.bind("<Configure>",sf.myfunction)

        sf.__labels__=['0'] #### list to store label objects ####

                      #############   specifications of a 'CANVAS'    #############
        sf.cwidth=331                           #canvas width 
        sf.cheight=430                          #canvas height
        sf.cbg='snow'                           #canvas bg color
        sf.ncolor='Dodgerblue2'                 #name color
        sf.nfont=("Helvetica 15 normal")        #name font description
        sf.dcolor='dim gray'                    #desciption color
        sf.dfont=("Helvetica 10 normal")        #descr. font description
        sf.sizecolor='snow'
        sf.sizefont=("Helvetica 12 normal") 
        sf.rec_color='snow4'
        sf.cbg2='firebrick1'
                                              #    MARGHERITA  1
        sf.veg=Canvas(sf.frame,bg=sf.cbg,width=sf.cwidth,height=sf.cheight,highlightthickness=1)
        sf.veg.grid(row=0,column=0)
        sf.veg.create_rectangle(1,1,330,429,outline=sf.rec_color,width=1) ## rectangle
        sf.veg.create_rectangle(1,1,330,15,fill='gray45',width=1)
        sf.veg.create_text(158,29,font=sf.nfont,fill=sf.ncolor,text='MARGHERITA')
        sf.img=ImageTk.PhotoImage(Image.open('Margherita.jpg'))
        sf.veg.create_image(162,172,image=sf.img)
        sf.veg.create_text(160,322,justify=CENTER,anchor=CENTER,font=sf.dfont,fill=sf.dcolor,text='A hugely popular margherita, with a deliciously \ntangy single cheese topping')
        sf.l.append(sf.veg)
        
        sf.veg2=Canvas(sf.veg,bg=sf.cbg2,highlightthickness=1)
        sf.veg2.place(x=2,y=341,width=sf.cwidth-3,height=88)

        sf.veg2.create_text(155,18,font=sf.sizefont,fill=sf.sizecolor,text='R:205 \u20B9        M:385 \u20B9         L:595 \u20B9')
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.R1,command=lambda variable=sf.R1,val='1':sf.cbR(sf.R1,'1')).place(x=98,y=5)
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.M1,command=lambda variable=sf.M1,val='1':sf.cbM(sf.M1,'1')).place(x=186,y=5)
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.L1,command=lambda variable=sf.L1,val='1':sf.cbL(sf.L1,'1')).place(x=276,y=5)
        sf.label1=Label(sf.veg2,bg='gray45',fg='white',text='ADD TO CART',font=("Sans 12 bold"))
        sf.label1.bind("<Button-1>",lambda val='1':sf.func('1'))
        sf.label1.place(x=94,y=40,width=110,height=30)
        sf.__labels__.append(sf.label1)
        sf.veg2.create_oval(77,33,220,76,fill='gray45',outline='gray45',width=0)

        sf.R1.set(sf.dict['1'][1]['R'])
        sf.M1.set(sf.dict['1'][1]['M'])
        sf.L1.set(sf.dict['1'][1]['L'])

                                #   DOUBLE CHEESE MARGHERITA  2
        sf.veg=Canvas(sf.frame,bg=sf.cbg,width=sf.cwidth,height=sf.cheight,highlightthickness=1)
        sf.veg.grid(row=0,column=1)
        sf.veg.create_rectangle(1,1,330,429,outline=sf.rec_color,width=1) ## rectangle
        sf.veg.create_text(161,29,font=sf.nfont,fill=sf.ncolor,text='DOUBLE CHEESE MARGHERITA')
        sf.img2=ImageTk.PhotoImage(Image.open('Double_Cheese_Margherita.jpg'))
        sf.veg.create_image(162,172,image=sf.img2)
        sf.veg.create_text(160,322,justify=CENTER,anchor=CENTER,font=sf.dfont,fill=sf.dcolor,text='The ever-popular Margherita - loaded with\n extra cheese... oodies of it!')
        sf.l.append(sf.veg)

        sf.veg2=Canvas(sf.veg,bg=sf.cbg2,highlightthickness=1)
        sf.veg2.place(x=2,y=341,width=sf.cwidth-3,height=88)    

        sf.veg2.create_text(155,18,font=sf.sizefont,fill=sf.sizecolor,text='R:205 \u20B9        M:385 \u20B9         L:595 \u20B9')       
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.R2,command=lambda variable=sf.R2,val='2':sf.cbR(sf.R2,'2')).place(x=98,y=5)
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.M2,command=lambda variable=sf.M2,val='2':sf.cbM(sf.M2,'2')).place(x=186,y=5)
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.L2,command=lambda variable=sf.L2,val='2':sf.cbL(sf.L2,'2')).place(x=276,y=5)
        sf.label2=Label(sf.veg2,bg='gray45',fg='white',text='ADD TO CART',font=("Sans 12 bold"))
        sf.label2.bind("<Button-1>",lambda val='2':sf.func('2'))
        sf.label2.place(x=94,y=40,width=110,height=30)
        sf.__labels__.append(sf.label2)
        sf.veg2.create_oval(77,33,220,76,fill='gray45',outline='gray45',width=0)   ######    STABLE

        sf.R2.set(sf.dict['2'][1]['R'])
        sf.M2.set(sf.dict['2'][1]['M'])
        sf.L2.set(sf.dict['2'][1]['L'])
        
                                                 #   FARM HOUSE   3
        sf.veg=Canvas(sf.frame,bg=sf.cbg,width=sf.cwidth,height=sf.cheight,highlightthickness=1)
        sf.veg.grid(row=0,column=2)
        sf.veg.create_rectangle(1,1,330,429,outline=sf.rec_color,width=1) ## rectangle
        sf.veg.create_rectangle(1,1,330,15,fill='gray45',width=1)
        sf.veg.create_text(161,29,font=sf.nfont,fill=sf.ncolor,text='FARM HOUSE')
        sf.img3=ImageTk.PhotoImage(Image.open('Farmhouse.jpg'))
        sf.veg.create_image(162,172,image=sf.img3)
        sf.veg.create_text(170,322,font=sf.dfont,fill=sf.dcolor,text='A pizza that goes ballistic on veggies! Check out\n              this overload of crunchness.')
        sf.l.append(sf.veg)
        
        sf.veg2=Canvas(sf.veg,bg=sf.cbg2,highlightthickness=1)
        sf.veg2.place(x=2,y=341,width=sf.cwidth-3,height=88)

        sf.veg2.create_text(155,18,font=sf.sizefont,fill=sf.sizecolor,text='R:205 \u20B9        M:385 \u20B9         L:595 \u20B9')
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.R3,command=lambda variable=sf.R3,val='3':sf.cbR(sf.R3,'3')).place(x=98,y=5)
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.M3,command=lambda variable=sf.M3,val='3':sf.cbM(sf.M3,'3')).place(x=186,y=5)
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.L3,command=lambda variable=sf.L3,val='3':sf.cbL(sf.L3,'3')).place(x=276,y=5)
        sf.label3=Label(sf.veg2,bg='gray45',fg='white',text='ADD TO CART',font=("Sans 12 bold"))
        sf.label3.bind("<Button-1>",lambda val='3':sf.func('3'))
        sf.label3.place(x=94,y=40,width=110,height=30)
        sf.__labels__.append(sf.label3)
        sf.veg2.create_oval(77,33,220,76,fill='gray45',outline='gray45',width=0)   ######    STABLE

        sf.R3.set(sf.dict['3'][1]['R'])
        sf.M3.set(sf.dict['3'][1]['M'])
        sf.L3.set(sf.dict['3'][1]['L'])
        
                                     #      PEPPY_PANEER    4
        sf.veg=Canvas(sf.frame,bg=sf.cbg,width=sf.cwidth,height=sf.cheight,highlightthickness=1)
        sf.veg.grid(row=0,column=3)
        sf.veg.create_rectangle(1,1,330,429,outline=sf.rec_color,width=1) ## rectangle
        sf.veg.create_text(161,29,font=sf.nfont,fill=sf.ncolor,text='PEPPY PANEER')
        sf.img4=ImageTk.PhotoImage(Image.open('Peppy_Paneer.jpg'))
        sf.veg.create_image(162,172,image=sf.img4)
        sf.veg.create_text(160,322,justify=CENTER,anchor=CENTER,font=sf.dfont,fill=sf.dcolor,text='Chunky paneer with crisp capsicum \nand spicy red pepper - quite a mouthful!')
        sf.l.append(sf.veg)

        sf.veg2=Canvas(sf.veg,bg=sf.cbg2,highlightthickness=1)
        sf.veg2.place(x=2,y=341,width=sf.cwidth-3,height=88)

        sf.veg2.create_text(155,18,font=sf.sizefont,fill=sf.sizecolor,text='R:205 \u20B9        M:385 \u20B9         L:595 \u20B9')
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.R4,command=lambda variable=sf.R4,val='4':sf.cbR(sf.R4,'4')).place(x=98,y=5)
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.M4,command=lambda variable=sf.M4,val='4':sf.cbM(sf.M4,'4')).place(x=186,y=5)
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.L4,command=lambda variable=sf.L4,val='4':sf.cbL(sf.L4,'4')).place(x=276,y=5)
        sf.label4=Label(sf.veg2,bg='gray45',fg='white',text='ADD TO CART',font=("Sans 12 bold"))
        sf.label4.place(x=94,y=40,width=110,height=30)
        sf.label4.bind("<Button-1>",lambda val='4':sf.func('4'))
        sf.__labels__.append(sf.label4)
        sf.veg2.create_oval(77,33,220,76,fill='gray45',outline='gray45',width=0)

        sf.R4.set(sf.dict['4'][1]['R'])
        sf.M4.set(sf.dict['4'][1]['M'])
        sf.L4.set(sf.dict['4'][1]['L'])
      
                                     #    MEXICAN GREEN WAVE     5
        sf.veg.create_rectangle(1,1,330,429,outline=sf.rec_color,width=1)
        sf.veg=Canvas(sf.frame,bg=sf.cbg,width=sf.cwidth,height=sf.cheight,highlightthickness=1)
        sf.veg.grid(row=1,column=0)
        sf.veg.create_rectangle(1,1,330,429,outline=sf.rec_color,width=1) ## rectangle
        sf.veg.create_text(158,29,font=sf.nfont,fill=sf.ncolor,text='MEXICAN GREEN WAVE')
        sf.img5=ImageTk.PhotoImage(Image.open('Mexican_Green_Wave.jpg'))
        sf.veg.create_image(162,172,image=sf.img5)
        sf.veg.create_text(160,322,justify=CENTER,anchor=CENTER,font=sf.dfont,fill=sf.dcolor,text='A pizza loaded with crunchy onions, crisp capsicum,\n juicy tomatoes,jalapeno & exotic Mexican herbs.')
        sf.l.append(sf.veg)

        sf.veg2=Canvas(sf.veg,bg=sf.cbg2,highlightthickness=1)
        sf.veg2.place(x=2,y=341,width=sf.cwidth-3,height=88)

        sf.veg2.create_text(155,18,font=sf.sizefont,fill=sf.sizecolor,text='R:205 \u20B9        M:385 \u20B9         L:595 \u20B9')
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.R5,command=lambda variable=sf.R5,val='5':sf.cbR(sf.R5,'5')).place(x=98,y=5)
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.M5,command=lambda variable=sf.M5,val='5':sf.cbM(sf.M5,'5')).place(x=186,y=5)
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.L5,command=lambda variable=sf.L5,val='5':sf.cbL(sf.L5,'5')).place(x=276,y=5)
        sf.label5=Label(sf.veg2,bg='gray45',fg='white',text='ADD TO CART',font=("Sans 12 bold"))
        sf.label5.place(x=94,y=40,width=110,height=30)
        sf.label5.bind("<Button-1>",lambda val='5':sf.func('5'))
        sf.__labels__.append(sf.label5)
        sf.veg2.create_oval(77,33,220,76,fill='gray45',outline='gray45',width=0)

        sf.R5.set(sf.dict['5'][1]['R'])
        sf.M5.set(sf.dict['5'][1]['M'])
        sf.L5.set(sf.dict['5'][1]['L'])
        
                                    #    DELUXE VEGGIE   6
        sf.veg=Canvas(sf.frame,bg=sf.cbg,width=sf.cwidth,height=sf.cheight,highlightthickness=1)
        sf.veg.grid(row=1,column=1)
        sf.veg.create_rectangle(1,1,330,429,outline=sf.rec_color,width=1) ## rectangle
        sf.veg.create_rectangle(1,1,330,15,fill='gray45',width=1)
        sf.veg.create_text(158,29,font=sf.nfont,fill=sf.ncolor,text='DELUXE VEGGIE')
        sf.img6=ImageTk.PhotoImage(Image.open('Deluxe_Veggie.jpg'))
        sf.veg.create_image(162,172,image=sf.img6)
        sf.veg.create_text(160,322,justify=CENTER,anchor=CENTER,font=sf.dfont,fill=sf.dcolor,text='The onions, the capsicum, those delectable\n mushrooms - with paneer and golden corn to top it all.')
        sf.l.append(sf.veg)

        sf.veg2=Canvas(sf.veg,bg=sf.cbg2,highlightthickness=1)
        sf.veg2.place(x=2,y=341,width=sf.cwidth-3,height=88)

        sf.veg2.create_text(155,18,font=sf.sizefont,fill=sf.sizecolor,text='R:205 \u20B9        M:385 \u20B9         L:595 \u20B9')
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.R6,command=lambda variable=sf.R6,val='6':sf.cbR(sf.R6,'6')).place(x=98,y=5)
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.M6,command=lambda variable=sf.M6,val='6':sf.cbM(sf.M6,'6')).place(x=186,y=5)
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.L6,command=lambda variable=sf.L6,val='6':sf.cbL(sf.L6,'6')).place(x=276,y=5)
        sf.label6=Label(sf.veg2,bg='gray45',fg='white',text='ADD TO CART',font=("Sans 12 bold"))
        sf.label6.place(x=94,y=40,width=110,height=30)
        sf.label6.bind("<Button-1>",lambda val='6':sf.func('6'))
        sf.__labels__.append(sf.label6)
        sf.veg2.create_oval(77,33,220,76,fill='gray45',outline='gray45',width=0)

        sf.R6.set(sf.dict['6'][1]['R'])
        sf.M6.set(sf.dict['6'][1]['M'])
        sf.L6.set(sf.dict['6'][1]['L'])
        
                                    #    5 PEPPER   7
        sf.veg=Canvas(sf.frame,bg=sf.cbg,width=sf.cwidth,height=sf.cheight,highlightthickness=1)
        sf.veg.grid(row=1,column=2)
        sf.veg.create_rectangle(1,1,330,429,outline=sf.rec_color,width=1) ## rectangle
        sf.veg.create_text(158,29,font=sf.nfont,fill=sf.ncolor,text='5 PEPPER')
        sf.img7=ImageTk.PhotoImage(Image.open('5_Pepper.jpg'))
        sf.veg.create_image(162,172,image=sf.img7)
        sf.veg.create_text(160,322,justify=CENTER,anchor=CENTER,font=sf.dfont,fill=sf.dcolor,text='Topped wih red & yellow bell pepper, capsicum,\n red paprika, jalapeno & sprinked with exotic herb')
        sf.l.append(sf.veg)

        sf.veg2=Canvas(sf.veg,bg=sf.cbg2,highlightthickness=1)
        sf.veg2.place(x=2,y=341,width=sf.cwidth-3,height=88)
        
        sf.veg2.create_text(155,18,font=sf.sizefont,fill=sf.sizecolor,text='R:205 \u20B9        M:385 \u20B9         L:595 \u20B9')
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.R7,command=lambda variable=sf.R7,val='7':sf.cbR(sf.R7,'7')).place(x=98,y=5)
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.M7,command=lambda variable=sf.M7,val='7':sf.cbM(sf.M7,'7')).place(x=186,y=5)
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.L7,command=lambda variable=sf.L7,val='7':sf.cbL(sf.L7,'7')).place(x=276,y=5)
        sf.label7=Label(sf.veg2,bg='gray45',fg='white',text='ADD TO CART',font=("Sans 12 bold"))
        sf.label7.place(x=94,y=40,width=110,height=30)
        sf.label7.bind("<Button-1>",lambda val='7':sf.func('7'))
        sf.__labels__.append(sf.label7)
        sf.veg2.create_oval(77,33,220,76,fill='gray45',outline='gray45',width=0)

        sf.R7.set(sf.dict['7'][1]['R'])
        sf.M7.set(sf.dict['7'][1]['M'])
        sf.L7.set(sf.dict['7'][1]['L'])
      
                                    #    VEG EXTRAVAGANZA    8
        sf.veg=Canvas(sf.frame,bg=sf.cbg,width=sf.cwidth,height=sf.cheight,highlightthickness=1)
        sf.veg.grid(row=1,column=3)
        sf.veg.create_rectangle(1,1,330,429,outline=sf.rec_color,width=1) ## rectangle
        sf.veg.create_rectangle(1,1,330,15,fill='gray45',width=1)
        sf.veg.create_text(158,29,font=sf.nfont,fill=sf.ncolor,text='VEG EXTRAVAGANZA')
        sf.img8=ImageTk.PhotoImage(Image.open('Veg_Extravaganza.jpg'))
        sf.veg.create_image(162,172,image=sf.img8)
        sf.veg.create_text(160,322,justify=CENTER,anchor=CENTER,font=sf.dfont,fill=sf.dcolor,text='A pizza that decidedly staggers under an overload of\n golden corn, exotic black olives,crunchy onions.')
        sf.l.append(sf.veg)

        sf.veg2=Canvas(sf.veg,bg=sf.cbg2,highlightthickness=1)
        sf.veg2.place(x=2,y=341,width=sf.cwidth-3,height=88)

        sf.veg2.create_text(155,18,font=sf.sizefont,fill=sf.sizecolor,text='R:205 \u20B9        M:385 \u20B9         L:595 \u20B9')
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.R8,command=lambda variable=sf.R8,val='8':sf.cbR(sf.R8,val='8')).place(x=98,y=5)
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.M8,command=lambda variable=sf.M8,val='8':sf.cbM(sf.M8,val='8')).place(x=186,y=5)
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.L8,command=lambda variable=sf.L8,val='8':sf.cbL(sf.L8,val='8')).place(x=276,y=5)
        sf.label8=Label(sf.veg2,bg='gray45',fg='white',text='ADD TO CART',font=("Sans 12 bold"))
        sf.label8.place(x=94,y=40,width=110,height=30)
        sf.label8.bind("<Button-1>",lambda val='8':sf.func('8'))
        sf.__labels__.append(sf.label8)
        sf.veg2.create_oval(77,33,220,76,fill='gray45',outline='gray45',width=0)

        sf.R8.set(sf.dict['8'][1]['R'])
        sf.M8.set(sf.dict['8'][1]['M'])
        sf.L8.set(sf.dict['8'][1]['L'])
        
                                    #    CHEESE N CORN  9                           
        sf.veg=Canvas(sf.frame,bg=sf.cbg,width=sf.cwidth,height=sf.cheight,highlightthickness=1)
        sf.veg.grid(row=2,column=0)
        sf.veg.create_rectangle(1,1,330,429,outline=sf.rec_color,width=1) ## rectangle
        sf.veg.create_rectangle(1,1,330,15,fill='gray45',width=1)
        sf.veg.create_text(158,29,font=sf.nfont,fill=sf.ncolor,text='CHEESE N CORN')
        sf.img9=ImageTk.PhotoImage(Image.open('Cheese_&_Corn.jpg'))
        sf.veg.create_image(162,172,image=sf.img9)
        sf.veg.create_text(160,322,justify=CENTER,anchor=CENTER,font=sf.dfont,fill=sf.dcolor,text='Cheese I Golden Corn')
        sf.l.append(sf.veg)

        sf.veg2=Canvas(sf.veg,bg=sf.cbg2,highlightthickness=1)
        sf.veg2.place(x=2,y=341,width=sf.cwidth-3,height=88)
        
        sf.veg2.create_text(155,18,font=sf.sizefont,fill=sf.sizecolor,text='R:205 \u20B9        M:385 \u20B9         L:595 \u20B9')
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.R9,command=lambda variable=sf.R9,val='9':sf.cbR(sf.R9,'9')).place(x=98,y=5)
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.M9,command=lambda variable=sf.M9,val='9':sf.cbM(sf.M9,'9')).place(x=186,y=5)
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.L9,command=lambda variable=sf.L9,val='9':sf.cbL(sf.L9,'9')).place(x=276,y=5)
        sf.label9=Label(sf.veg2,bg='gray45',fg='white',text='ADD TO CART',font=("Sans 12 bold"))
        sf.label9.place(x=94,y=40,width=110,height=30)
        sf.label9.bind("<Button-1>",lambda val='9':sf.func('9'))
        sf.__labels__.append(sf.label9)
        sf.veg2.create_oval(77,33,220,76,fill='gray45',outline='gray45',width=0)

        sf.R9.set(sf.dict['9'][1]['R'])
        sf.M9.set(sf.dict['9'][1]['M'])
        sf.L9.set(sf.dict['9'][1]['L'])
     
                                   #    PANEER MAKHANI   10
        sf.veg=Canvas(sf.frame,bg=sf.cbg,width=sf.cwidth,height=sf.cheight,highlightthickness=1)
        sf.veg.grid(row=2,column=1)
        sf.veg.create_rectangle(1,1,330,429,outline=sf.rec_color,width=1) ## rectangle
        sf.veg.create_text(158,29,font=sf.nfont,fill=sf.ncolor,text='PANEER MAKHANI')
        sf.img10=ImageTk.PhotoImage(Image.open('Paneer_Makhni.jpg'))
        sf.veg.create_image(162,172,image=sf.img10)
        sf.veg.create_text(160,322,justify=CENTER,anchor=CENTER,font=sf.dfont,fill=sf.dcolor,text='Paneer and Capsicum on Makhani Sauce')
        sf.l.append(sf.veg)
        
        sf.veg2=Canvas(sf.veg,bg=sf.cbg2,highlightthickness=1)
        sf.veg2.place(x=2,y=341,width=sf.cwidth-3,height=88)
        
        sf.veg2.create_text(155,18,font=sf.sizefont,fill=sf.sizecolor,text='R:205 \u20B9        M:385 \u20B9         L:595 \u20B9')
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.R10,command=lambda variable=sf.R10,val='10':sf.cbR(sf.R10,'10')).place(x=98,y=5)
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.M10,command=lambda variable=sf.M10,val='10':sf.cbM(sf.M10,'10')).place(x=186,y=5)
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.L10,command=lambda variable=sf.L10,val='10':sf.cbL(sf.L10,'10')).place(x=276,y=5)
        sf.label10=Label(sf.veg2,bg='gray45',fg='white',text='ADD TO CART',font=("Sans 12 bold"))
        sf.label10.place(x=94,y=40,width=110,height=30)
        sf.label10.bind("<Button-1>",lambda val='10':sf.func('10'))
        sf.__labels__.append(sf.label10)
        sf.veg2.create_oval(77,33,220,76,fill='gray45',outline='gray45',width=0)

        sf.R10.set(sf.dict['10'][1]['R'])
        sf.M10.set(sf.dict['10'][1]['M'])
        sf.L10.set(sf.dict['10'][1]['L'])
        
                                   #    VEGGIE PARADISE     11
        sf.veg=Canvas(sf.frame,bg=sf.cbg,width=sf.cwidth,height=sf.cheight,highlightthickness=1)
        sf.veg.grid(row=2,column=2)
        sf.veg.create_rectangle(1,1,330,429,outline=sf.rec_color,width=1) ## rectangle
        sf.veg.create_rectangle(1,1,330,15,fill='gray45',width=1)
        sf.veg.create_text(158,29,font=sf.nfont,fill=sf.ncolor,text='VEGGIE PARADISE')
        sf.img11=ImageTk.PhotoImage(Image.open('Veggie_Paradise.jpg'))
        sf.veg.create_image(162,172,image=sf.img11)
        sf.veg.create_text(160,322,justify=CENTER,anchor=CENTER,font=sf.dfont,fill=sf.dcolor,text='Goldern Corn, Black Olives, Capsicum & Red Paprika')
        sf.l.append(sf.veg)

        sf.veg2=Canvas(sf.veg,bg=sf.cbg2,highlightthickness=1)
        sf.veg2.place(x=2,y=341,width=sf.cwidth-3,height=88)
        
        sf.veg2.create_text(155,18,font=sf.sizefont,fill=sf.sizecolor,text='R:205 \u20B9        M:385 \u20B9         L:595 \u20B9')
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.R11,command=lambda variable=sf.R11,val='11':sf.cbR(sf.R11,'11')).place(x=98,y=5)
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.M11,command=lambda variable=sf.M11,val='11':sf.cbM(sf.M11,'11')).place(x=186,y=5)
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.L11,command=lambda variable=sf.L11,val='11':sf.cbL(sf.L11,'11')).place(x=276,y=5)
        sf.label11=Label(sf.veg2,bg='gray45',fg='white',text='ADD TO CART',font=("Sans 12 bold"))
        sf.label11.place(x=94,y=40,width=110,height=30)
        sf.label11.bind("<Button-1>",lambda val='11':sf.func('11'))
        sf.__labels__.append(sf.label11)
        sf.veg2.create_oval(77,33,220,76,fill='gray45',outline='gray45',width=0)

        sf.R11.set(sf.dict['11'][1]['R'])
        sf.M11.set(sf.dict['11'][1]['M'])
        sf.L11.set(sf.dict['11'][1]['L'])
        
                           #    FRESH VEGGIE   12
        sf.veg=Canvas(sf.frame,bg=sf.cbg,width=sf.cwidth,height=sf.cheight,highlightthickness=1)
        sf.veg.grid(row=2,column=3)
        sf.veg.create_rectangle(1,1,330,429,outline=sf.rec_color,width=1) ## rectangle
        sf.veg.create_text(158,29,font=sf.nfont,fill=sf.ncolor,text='FRESH VEGGIE')
        sf.img12=ImageTk.PhotoImage(Image.open('Fresh_Veggie.jpg'))
        sf.veg.create_image(162,172,image=sf.img12)
        sf.veg.create_text(160,322,justify=CENTER,anchor=CENTER,font=sf.dfont,fill=sf.dcolor,text='Onion I Capsicum')
        sf.l.append(sf.veg)

        sf.veg2=Canvas(sf.veg,bg=sf.cbg2,highlightthickness=1)
        sf.veg2.place(x=2,y=341,width=sf.cwidth-3,height=88)

        sf.veg2.create_text(155,18,font=sf.sizefont,fill=sf.sizecolor,text='R:205 \u20B9        M:385 \u20B9         L:595 \u20B9')
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.R12,command=lambda variable=sf.R12,val='12':sf.cbR(sf.R12,'12')).place(x=98,y=5)
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.M12,command=lambda variable=sf.M12,val='12':sf.cbM(sf.M12,'12')).place(x=186,y=5)
        Checkbutton(sf.veg2,bg=sf.cbg2,relief=FLAT,variable=sf.L12,command=lambda variable=sf.L12,val='12':sf.cbL(sf.L12,'12')).place(x=276,y=5)
        sf.label12=Label(sf.veg2,bg='gray45',fg='white',text='ADD TO CART',font=("Sans 12 bold"))
        sf.label12.place(x=94,y=40,width=110,height=30)
        sf.label12.bind("<Button-1>",lambda val='12':sf.func('12'))
        sf.__labels__.append(sf.label12)
        sf.veg2.create_oval(77,33,220,76,fill='gray45',outline='gray45',width=0)

        sf.R12.set(sf.dict['12'][1]['R'])
        sf.M12.set(sf.dict['12'][1]['M'])
        sf.L12.set(sf.dict['12'][1]['L'])

        for d in sf.dict:
            if sf.dict[d][2]==True:
                sf.__labels__[int(d)].config(text='REMOVE',fg='SpringGreen2')

        sf.scr.mainloop()
        
    def meals(sf,val):
        if sf.P['R']==0 and sf.P['M']==0 and sf.P['L']==0:
            messagebox.showinfo('Message','Please add a Pizza to the cart before selecting drinks.')
            sf.create_order('0')
        else:
            sf.flush()
    
            sf.frame.config(width=1336,height=1600)
            sf.canva=Canvas(sf.frame,bd=-2,bg='white',width=1336,height=1600,highlightthickness=1)
            sf.canva.place(x=0,y=0)
            
            sf.meal1=ImageTk.PhotoImage(Image.open('meal1.jpg'))   ## meal 1 ##
            sf.canva.create_image(940,200,image=sf.meal1)
            Label(sf.canva,text='Salsa Verde Enchiladas',font=('Sans 18 bold'),bg='white').place(x=170,y=84)
            Label(sf.canva,text='with Poblano Pepper,Black Beans & Monterey Jack Cheese',bg='white',font=('Helvetica 12 normal')).place(x=105,y=110)
            sf.canva.create_polygon(190,260,390,260,420,300,220,300,fill='firebrick2',width=2)
            sf.m1=Label(sf.canva,text='ADD TO CART',bg='firebrick2',fg='gold',font=('Sans 15 bold'))
            sf.m1.place(x=224,y=264,width=160,height=33)
            sf.m1.bind('<Button-1>',lambda val='1',price=449:sf.meals_func('1',price))
            Label(sf.canva,text='\u20B9',font=('Sans 15 bold'),bg='orange2',fg='white').place(x=606,y=240-40,width=26,height=24)
            Label(sf.canva,text='449',font=('Sans 18 bold'),bg='orange2').place(x=626,y=242-40,width=40,height=35)
            sf.canva.create_oval(597,230-40,675,286-40,fill='orange2',width=2,outline='orange2')

            sf.meal2=ImageTk.PhotoImage(Image.open('meal2.jpg'))  ## meal 2 ##
            sf.canva.create_image(940,570,image=sf.meal2)
            Label(sf.canva,text='Hawaiian Poke Bowl',font=('Sans 18 bold'),bg='white').place(x=180,y=450)
            Label(sf.canva,text='with Pineapple,Coconut Cashews & Sriracha Lime crunch',bg='white',font=('Helvetica 12 normal')).place(x=105,y=476)
            sf.canva.create_polygon(190,590+45,390,590+45,420,630+45,220,630+45,fill='firebrick2',width=2)
            sf.m2=Label(sf.canva,text='ADD TO CART',bg='firebrick2',fg='gold',font=('Sans 15 bold'))
            sf.m2.place(x=224,y=594+45,width=160,height=33)
            sf.m2.bind('<Button-1>',lambda val='2',price=490:sf.meals_func('2',price))
            Label(sf.canva,text='\u20B9',font=('Sans 15 bold'),bg='orange2',fg='white').place(x=606,y=240+350,width=26,height=24)
            Label(sf.canva,text='490',font=('Sans 18 bold'),bg='orange2').place(x=626,y=242+350,width=40,height=35)
            sf.canva.create_oval(597,230+350,675,286+350,fill='orange2',width=2,outline='orange2')
            
            sf.meal3=ImageTk.PhotoImage(Image.open('meal3.jpg'))  ## meal 3 ##
            sf.canva.create_image(940,970,image=sf.meal3)
            Label(sf.canva,text='California Chicken Bar',font=('Sans 18 bold'),bg='white').place(x=140,y=850)
            Label(sf.canva,text='with Smokey Spices,Jalapeno & Moneterey Jack Cheese',bg='white',font=('Helvetica 12 normal')).place(x=90,y=876)
            sf.canva.create_polygon(190,590+45+400,390,590+45+400,420,630+45+400,220,630+45+400,fill='firebrick2',width=2)
            sf.m3=Label(sf.canva,text='ADD TO CART',bg='firebrick2',fg='gold',font=('Sans 15 bold'))
            sf.m3.place(x=224,y=594+45+400,width=160,height=33)
            sf.m3.bind('<Button-1>',lambda val='3',price=399:sf.meals_func('3',price))
            Label(sf.canva,text='\u20B9',font=('Sans 15 bold'),bg='orange2',fg='white').place(x=606,y=240+350+400,width=26,height=24)
            Label(sf.canva,text='399',font=('Sans 18 bold'),bg='orange2').place(x=626,y=242+350+400,width=40,height=35)
            sf.canva.create_oval(597,230+350+400,675,286+350+400,fill='orange2',width=2,outline='orange2')

            sf.meal4=ImageTk.PhotoImage(Image.open('meal4.jpg'))  # bruchetta salmon
            sf.canva.create_image(940,1370,image=sf.meal4)
            Label(sf.canva,text='Bruchetta Salmon',font=('Sans 18 bold'),bg='white').place(x=165,y=850+400)
            sf.canva.create_polygon(190,590+45+800,390,590+45+800,420,630+45+800,220,630+45+800,fill='firebrick2',width=2)
            sf.m4=Label(sf.canva,text='ADD TO CART',bg='firebrick2',fg='gold',font=('Sans 15 bold'))
            sf.m4.place(x=224,y=594+45+800,width=160,height=33)
            sf.m4.bind('<Button-1>',lambda val='4',price=549:sf.meals_func('4',price))
            Label(sf.canva,text='\u20B9',font=('Sans 15 bold'),bg='orange2',fg='white').place(x=606,y=240+350+800,width=26,height=24)
            Label(sf.canva,text='549',font=('Sans 18 bold'),bg='orange2').place(x=626,y=242+350+800,width=40,height=35)
            sf.canva.create_oval(597,230+350+800,675,286+350+800,fill='orange2',width=2,outline='orange2')
            
            sf.__labels3__=['0',sf.m1,sf.m2,sf.m3,sf.m4]

            for m in sf.M:
                if sf.M[m][0]==True: ## previously selected meal
                    sf.__labels3__[int(m)].config(text='REMOVE',bg='firebrick2',fg='black')
                    
    def drinks(sf,val):
        if sf.TOTAL==-1:  ## was too lazy to reindent the else block............so a bogus condition here !!!
            messagebox.showinfo('Message','Please add a Pizza to the cart before selecting drinks.')
            sf.create_order('1')
        else:
            sf.flush()

            sf.frame.config(width=1336,height=710)
            sf.canva=Canvas(sf.frame,bd=-2,bg='white',width=1336,height=1200,highlightthickness=1)
            sf.canva.place(x=0,y=0)
            
            sf.coke=ImageTk.PhotoImage(Image.open('coca_cola.jpg')) ####    COKE 1  ####
            sf.canva.create_image(250,136,image=sf.coke)
            Label(sf.canva,text='COKE',font=('Sans 12 bold')).place(x=200,y=225,width=90,height=30)
            sf.d1=Label(sf.canva,text='ADD TO CART',font=('Sans 14 bold'),bg='light sea green',fg='snow')
            sf.d1.place(x=180,y=260,width=150,height=30)
            sf.d1.bind("<Button-1>",lambda val='1',price=84:sf.drink_cart('1',price))
            sf.canva.create_oval(165,260,195,289,fill='light sea green',outline='light sea green')
            Label(sf.canva,text='\u20B9 84/-',font=('Sans 17 bold'),bg='red3',fg='white').place(x=90,y=257,width=55,height=40)
            sf.canva.create_oval(83,242,152,312,fill='red3',outline='red3')

            sf.pepsi=PhotoImage(file='pepsi.png')                   ####    PEPSI 2  ####
            sf.canva.create_image(650,137,image=sf.pepsi)
            Label(sf.canva,text='PEPSI',font=('Sans 12 bold')).place(x=610,y=225,width=90,height=30)
            sf.d2=Label(sf.canva,text='ADD TO CART',font=('Sans 14 bold'),bg='light sea green',fg='snow')
            sf.d2.place(x=590,y=260,width=150,height=30)
            sf.d2.bind("<Button-1>",lambda val='2',price=80:sf.drink_cart('2',price))
            Label(sf.canva,text='\u20B9 80/-',font=('Sans 17 bold'),bg='red3',fg='white').place(x=90+413,y=257,width=55,height=40)
            sf.canva.create_oval(83+413,242,152+413,312,fill='red3',outline='red3')

            sf.sprite=PhotoImage(file='sprite.png')                 ####    SPRITE 3 ####
            sf.canva.create_image(1065,120,image=sf.sprite)
            Label(sf.canva,text='SPRITE',font=('Sans 12 bold')).place(x=1020,y=225,width=90,height=30)
            sf.d3=Label(sf.canva,text='ADD TO CART',font=('Sans 14 bold'),bg='light sea green',fg='snow')
            sf.d3.place(x=1000,y=260,width=150,height=30)
            sf.d3.bind("<Button-1>",lambda val='3',price=81:sf.drink_cart('3',price))
            sf.canva.create_oval(1135,260,1165,289,fill='light sea green',outline='light sea green')
            Label(sf.canva,text='\u20B9 81/-',font=('Sans 17 bold'),bg='red3',fg='white').place(x=90+413+413,y=257,width=55,height=40)
            sf.canva.create_oval(83+413+413,242,152+413+413,312,fill='red3',outline='red3')
        
            sf.mtn=ImageTk.PhotoImage(Image.open('mtn2.jpg'))       ####    DEW 4  ####
            sf.canva.create_image(250,425,image=sf.mtn)
            Label(sf.canva,text='DEW',font=('Sans 12 bold')).place(x=200,y=560,width=90,height=30)
            sf.d4=Label(sf.canva,text='ADD TO CART',font=('Sans 14 bold'),bg='light sea green',fg='snow')
            sf.d4.place(x=180,y=260+335,width=150,height=30)
            sf.d4.bind("<Button-1>",lambda val='4',price=86:sf.drink_cart('4',price))
            sf.canva.create_oval(165,260+335,195,289+335,fill='light sea green',outline='light sea green')
            Label(sf.canva,text='\u20B9 86/-',font=('Sans 17 bold'),bg='red3',fg='white').place(x=90,y=257+335,width=55,height=40)
            sf.canva.create_oval(83,242+335,152,312+335,fill='red3',outline='red3')

            sf.fanta=ImageTk.PhotoImage(Image.open('fanta.jpg'))    ####    FANTA 5 ####
            sf.canva.create_image(650,425,image=sf.fanta)
            Label(sf.canva,text='FANTA',font=('Sans 12 bold')).place(x=610,y=560,width=90,height=30)
            sf.d5=Label(sf.canva,text='ADD TO CART',font=('Sans 14 bold'),bg='light sea green',fg='snow')
            sf.d5.place(x=590,y=260+335,width=150,height=30)
            sf.d5.bind("<Button-1>",lambda val='5',price=78:sf.drink_cart('5',price))
            Label(sf.canva,text='\u20B9 78/-',font=('Sans 17 bold'),bg='red3',fg='white').place(x=90+413,y=257+335,width=55,height=40)
            sf.canva.create_oval(83+413,242+335,152+413,312+335,fill='red3',outline='red3')

            sf.thums=ImageTk.PhotoImage(Image.open('thums_up.jpg'))   ####    THUMS UP 6 ####
            sf.canva.create_image(1050,425,image=sf.thums)
            Label(sf.canva,text='THUMS UP',font=('Sans 12 bold')).place(x=1020,y=560,width=90,height=30)
            sf.d6=Label(sf.canva,text='ADD TO CART',font=('Sans 14 bold'),bg='light sea green',fg='snow')
            sf.d6.place(x=1000,y=260+335,width=150,height=30)
            sf.d6.bind("<Button-1>",lambda val='6',price=84:sf.drink_cart('6',price))
            sf.canva.create_oval(1135,260+335,1165,289+335,fill='light sea green',outline='light sea green')
            Label(sf.canva,text='\u20B9 84/-',font=('Sans 17 bold'),bg='red3',fg='white').place(x=90+413+413,y=257+335,width=55,height=40)
            sf.canva.create_oval(83+413+413,242+335,152+413+413,312+335,fill='red3',outline='red3')

            sf.__labels2__=['0',sf.d1,sf.d2,sf.d3,sf.d4,sf.d5,sf.d6]
            
            for d in sf.D:
                if sf.D[d][0]==True:
                    sf.__labels2__[int(d)].config(text='REMOVE',bg='light sea green',fg='black')
                    

    def payment_window(sf,val):  #####       Payment window       #####
        if(sf.P['R']==0 and sf.P['M']==0 and sf.P['L']==0):
            messagebox.showinfo("No pizzas selected.","Please make an order to continue")
        else:
            sf.flush()
            #sf.f.place(x=0,y=0)
            sf.frame.config(width=1336,height=1410,bg='white') ## prev height=1200
            sf.canva=Canvas(sf.frame,bd=-2,bg='white',width=1336,height=1410,highlightthickness=1)  ### 1000
            sf.canva.place(x=0,y=0)

            Label(sf.frame,text='PLEASE CHECK THE FOLLOWING DETAILS\n TO COMPLETE YOUR ORDER',font=('Helvetica 11 bold'),bg='white',fg='grey19').place(x=30,y=50)
            e=Entry(sf.frame,bg='gray99') ###   NAME   ##
            e.insert(0,sf.NAME)
            e.place(x=55,y=105,width=250,height=28)
            e=Entry(sf.frame,bg='gray99')  ##   EMAIL   ##
            e.insert(0,sf.MAIL)
            e.place(x=55,y=145,width=250,height=28)
            e=Entry(sf.frame,bg='gray99')  ##   PHONE NO   ##
            e.insert(0,'Phone No*')
            e.place(x=55,y=185,width=250,height=28)
            sf.canva.create_rectangle(14,38,365,245,width=2,outline='deep sky blue')  ## rectangle  ##

            Label(sf.frame,text='YOUR DELIVERY ADDRESS',font=('Helvetica 11 bold'),bg='white',fg='grey19').place(x=530,y=50)
            Label(sf.frame,text='House No',bg='white').place(x=460,y=105)
            Label(sf.frame,text='Street/Society ',bg='white').place(x=460,y=145)
            Label(sf.frame,text='City',bg='white').place(x=460,y=185)

            sf.he=Entry(sf.frame,bg='gray99') ###   HOUSE Entry field   ##
            sf.he.place(x=550,y=105,width=210,height=28)
            sf.se=Entry(sf.frame,bg='gray99')  ##   SOCIETY Entry field   ##
            sf.se.place(x=550,y=145,width=210,height=28)
            sf.ce=Entry(sf.frame,bg='gray99')  ##   CITY Entry field   ##
            sf.ce.place(x=550,y=185,width=210,height=28)
            sf.canva.create_rectangle(14+435,43,360+440+25,245,width=2,outline='deep sky blue')  ## rectangle  ##

            
            sf.loc=PhotoImage(file='loc.png')
            sf.loc_logo=Label(sf.canva,image=sf.loc,bg='white')
            sf.loc_logo.place(x=772,y=177,width=37,height=42)
            sf.loc_logo.bind('<Button-1>',lambda val='1':sf.detect_loc('1'))
            sf.dl=Label(sf.canva,text='Detect City')
            sf.dl.place(x=760,y=220)
            sf.dl.bind('<Button-1>',lambda val='1':sf.detect_loc('1'))
            
            Label(sf.frame,text='ORDER DETAILS',font=('Helvetica 11 bold'),bg='white',fg='grey19').place(x=1020,y=50)
            Label(sf.frame,text='Net Price',bg='white').place(x=936,y=110)    ###   TOTAL LABEL
            Label(sf.frame,text='\u20B9 '+str(sf.TOTAL),bg='white').place(x=1084,y=110)
            Label(sf.frame,text='GST',bg='white').place(x=936,y=150)   ### GST LABEL
            Label(sf.frame,text='\u20B9 '+str(math.ceil(0.18*sf.TOTAL)),bg='white').place(x=1084,y=150)
            Label(sf.frame,text='TOTAL',bg='turquoise1',font=('bold 10')).place(x=936,y=190)    ###   TOTAL LABEL
            Label(sf.frame,text=str(math.ceil(0.18*sf.TOTAL)+sf.TOTAL),bg='white',font=('bold 10')).place(x=1084,y=190)
            sf.canva.create_rectangle(894,38,1275,245,width=2,outline='deep sky blue')  ## rectangle  ##
            
            sf.canva.create_rectangle(50,288,900,358,fill='brown3',outline='white',width=2)
            Label(sf.canva,text='YOUR CART DETAILS',font=('Sans 21 bold'),fg='snow',bg='brown3').place(x=60,y=295,width=300,height=55)
            Label(sf.canva,text='Item',font=('Sans 17 bold'),fg='gray53',bg='white').place(x=180,y=370)
            Label(sf.canva,text='Price',font=('Sans 17 bold'),fg='gray53',bg='white').place(x=760,y=370)
            
            i=0         ################    first check for PIZZAS ################
            sf.pizza_logo2=PhotoImage(file='pizza_logo2.png')
            sf.drinks_logo2=PhotoImage(file='drinks_logo2.png')
            sf.meals_logo2=ImageTk.PhotoImage(Image.open('meals_logo2.jpg'))
            for p in sf.dict:
                if sf.dict[p][1]['R']==1 or sf.dict[p][1]['M']==1 or sf.dict[p][1]['L']==1:
                    size=''
                    price=0
                    if sf.dict[p][1]['R']==1:
                        size+=' R'
                        price+=205
                    if sf.dict[p][1]['M']==1:
                        size+=' M'
                        price+=385
                    if sf.dict[p][1]['L']==1:
                        size+=' L'
                        price+=595
                    sf.canva.create_oval(50,430+60*i,82,466+60*i,fill='brown3',outline='gold',width=4)
                    if i>=9:
                        Label(sf.canva,text=str(i+1),bg='brown3',fg='snow',font=('Sans 10 bold')).place(x=56,y=437+60*i)
                    else:
                         Label(sf.canva,text=str(i+1),bg='brown3',fg='snow',font=('Sans 10 bold')).place(x=60,y=437+60*i)
                    Label(sf.canva,text=sf.dict[p][0],font=('Sans 15 bold'),bg='white',fg='gray4').place(x=100,y=430+60*i) ##name
                    sf.canva.create_image(450,440+60*i,image=sf.pizza_logo2)  #### logo ####
                    Label(sf.canva,text=size,font=('Helvetica 11 bold italic')).place(x=550,y=432+60*i)  ## size ##
                    Label(sf.canva,text='\u20B9 '+str(price),font=('Times 15 bold'),bg='white').place(x=766,y=430+60*i)
                    i+=1
              
            for d in sf.D:  ############ drinks #################
                if sf.D[d][0]==True:
                    sf.canva.create_oval(50,430+60*i,82,466+60*i,fill='brown3',outline='gold',width=4)
                    if i>=9:
                        Label(sf.canva,text=str(i+1),bg='brown3',fg='snow',font=('Sans 10 bold')).place(x=56,y=437+60*i)
                    else:
                        Label(sf.canva,text=str(i+1),bg='brown3',fg='snow',font=('Sans 10 bold')).place(x=60,y=437+60*i)
                    Label(sf.canva,text=sf.D[d][1],font=('Sans 15 bold'),bg='white',fg='gray4').place(x=100,y=430+60*i) ## name
                    sf.canva.create_image(450,440+60*i,image=sf.drinks_logo2)  #### logo ####
                    Label(sf.canva,text='\u20B9 '+str(sf.D[d][2]),font=('Times 15 bold'),bg='white').place(x=766,y=430+60*i)
                    i+=1
            
            for m in sf.M:  #########  meals ##############
                if sf.M[m][0]==True:
                    sf.canva.create_oval(50,430+60*i,82,466+60*i,fill='brown3',outline='gold',width=4)
                    if i>=9:
                        Label(sf.canva,text=str(i+1),bg='brown3',fg='snow',font=('Sans 10 bold')).place(x=56,y=437+60*i)
                    else:
                        Label(sf.canva,text=str(i+1),bg='brown3',fg='snow',font=('Sans 10 bold')).place(x=60,y=437+60*i)
                    Label(sf.canva,text=sf.M[m][1],font=('Sans 15 bold'),bg='white',fg='gray4').place(x=100,y=430+60*i) #name
                    sf.canva.create_image(450,440+60*i,image=sf.meals_logo2)  #### logo ####
                    Label(sf.canva,text='\u20B9 '+str(sf.M[m][2]),font=('Times 15 bold'),bg='white').place(x=766,y=430+60*i)
                    i+=1

            Label(sf.canva,text='TOTAL',font=('Sans 17 bold'),bg='white',fg='gray2').place(x=100,y=430+60*i)
            Label(sf.canva,text='\u20B9 '+str(sf.TOTAL),font=('Sans 17 bold'),bg='white',fg='gray2').place(x=760,y=430+60*i)

            sf.po=Label(sf.canva,text='Place Order',bg='firebrick3',fg='gold',font=('Sans 15 bold'))
            sf.po.bind('<Button-1>',lambda val='1':sf.place_order('1'))
            sf.po.place(x=1100,y=400,width=130,height=40)
    def place_order(sf,val):
        if not len(sf.he.get()) or not len(sf.se.get()) or not len(sf.ce.get()):
            messagebox.showinfo('Missing Details','Please provide address details for successful delivery of your order.')
            sf.payment_window('1')
        else:
            messagebox.showinfo('Order placed','Dear '+sf.NAME+' ,your order has been successfully placed.\nIt will be delivered to '+
            sf.he.get()+','+sf.se.get()+','+sf.ce.get()+' within an hour.\nThank you !')
        
    def detect_loc(sf,val):
        try:
            sf.send_url='http://api.ipstack.com/check?access_key=53f81dc34a67ee115744d5c0b19d8300'
            try:
                sf.geo_req=requests.get(sf.send_url)
            except:
                messagebox.showinfo('Error',"Your location couldn't be detected.\nPlease make sure you have a reliable internet connection")
            sf.geo_json=json.loads(sf.geo_req.text)
            sf.city=sf.geo_json['city'] 
            sf.ce.delete(0,'end')       #delete user entered city (if any)
            sf.ce.insert(0,sf.city)     #insert the fetched city
        except:
            pass
x=Login() 
del(s)
