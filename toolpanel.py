import tkinter
import tkinter.ttk
import threading
class ToolPanel(tkinter.Frame) :
    def __init__(self,master,brightnessScaleCallback,contrastScaleCallback,cropCallback,rotateCallback,flipCallback,superImposeCallback) :
        tkinter.Frame.__init__(self,master,height=610,width=250)
        self.canvas=tkinter.Canvas(self,height=662,width=250,bg="#383838")
        self.canvas.pack(fill=tkinter.BOTH,expand=1) 
        self.canvas.create_text(135,35,text="IMagic",font=("Comic Sans MS",28,"bold"),fill="white")
        self.toolCanvas=tkinter.Canvas(self.canvas,height=592,width=250,bd=10,highlightbackground="black",highlightcolor="black",highlightthickness=3)
        self.canvas.create_window(0,70,window=self.toolCanvas,anchor="nw")
        self.scaleLabel=tkinter.Label(self.toolCanvas,fg="black",font=("Comic Sans MS",16,"bold"),text="0")
        self.contrastScale=tkinter.ttk.Scale(self.toolCanvas,from_=1,to=200,orient=tkinter.HORIZONTAL,length=200,command=self.updateScaleLabel)
        self.brightnessScale=tkinter.ttk.Scale(self.toolCanvas,from_=1,to=200,orient=tkinter.HORIZONTAL,length=200,command=self.updateScaleLabel)
        self.contrastScale.set(100)
        self.brightnessScale.set(100)
        self.brightnessScale.bind("<ButtonRelease-1>",brightnessScaleCallback) 
        self.brightnessScaleCallback=brightnessScaleCallback
        self.contrastScale.bind("<ButtonRelease-1>",contrastScaleCallback) 
        self.xEntry=tkinter.Entry(self.toolCanvas,width=10,font=("Verdana",10,))
        self.yEntry=tkinter.Entry(self.toolCanvas,width=10,font=("Verdana",10,))
        self.widthEntry=tkinter.Entry(self.toolCanvas,width=10,font=("Verdana",10,))
        self.heightEntry=tkinter.Entry(self.toolCanvas,width=10,font=("Verdana",10,))
        self.cropButton=tkinter.Button(self.toolCanvas,height=1,width=5,text="Crop",border=3,font=("Verdana",11,"bold"),command=self.cropButtonHandler)
        self.cancelButton=tkinter.Button(self.toolCanvas,height=1,width=7,text="Cancel",border=3,font=("Verdana",11,"bold"),command=self.cancelButtonHandler,relief="raised")            
        self.style1=tkinter.ttk.Style()
        self.rotateCombobox=tkinter.ttk.Combobox(self.toolCanvas,background="black",foreground="white",width=12,height=0,values=["90\u00B0 clockwise","90\u00B0 anticlockwise","180\u00B0"],justify="center",state="readonly")
        self.flipCombobox=tkinter.ttk.Combobox(self.toolCanvas,background="black",foreground="white",width=12,height=0,values=["Horizontal","Vertical"],justify="center",state="readonly")
        self.rotateButton=tkinter.Button(self.toolCanvas,text="Rotate",width=7,height=1,border=3,state="disabled",font=("Verdana",11,"bold"),command=lambda : threading.Thread(target=rotateCallback,args=(self.rotateCombobox.get(),)).start())
        self.flipButton=tkinter.Button(self.toolCanvas,width=5,height=1,text="Flip",border=3,font=("Verdana",11,"bold"),command=lambda : threading.Thread(target=flipCallback,args=(self.flipCombobox.get(),)).start(),state="disabled")	
        self.rotateCombobox.bind("<<ComboboxSelected>>",self.rotateComboboxHandler)        
        self.flipCombobox.bind("<<ComboboxSelected>>",self.flipComboboxHandler)        

        self.cropCallback=cropCallback
        self.superImposeCallback=superImposeCallback
        self.imageOpenEntry=tkinter.Entry(self.toolCanvas,width=15,font=("Verdana",12,),state="disabled",bd=3)
        self.selectFileButton=tkinter.Button(self.toolCanvas,height=1,width=6,text="Select",border=2,font=("Verdana",10,"bold"),command=self.selectFileButtonHandler)
        self.superImposeButton=tkinter.Button(self.toolCanvas,height=1,width=12,text="Super Impose",border=3,font=("Verdana",11,"bold"),command=self.superImposeButtonHandler,state="disabled")
    def cancelButtonHandler(self) :
        self.toolCanvas.delete('all')
    def selectFileButtonHandler(self,event=None) :
        self.imageOpenEntry.delete(0,'end')
        self.superImposeButton['state']='normal'
        self.fileName=tkinter.filedialog.askopenfilename(title="Open Image",initialdir='.',filetypes=(('Jpg files','*.jpg'),("All files","*.*")))   
        self.imageOpenEntry['state']="normal" 
        self.imageOpenEntry.insert(0,self.fileName)        
        self.imageOpenEntry['state']="disabled" 
    def superImposeButtonHandler(self,event=None) :
        x=int(self.xEntry.get())
        y=int(self.yEntry.get())
        t=threading.Thread(target=self.superImposeCallback,args=(self.fileName,(x,y)))
        t.start()
    def rotateComboboxHandler(self,event) :
        self.rotateButton['state']='normal'
    def flipComboboxHandler(self,event) :
        self.flipButton['state']='normal'

    def superImpose(self) :
        self.xEntry.delete(0,"end")
        self.yEntry.delete(0,"end")
        self.toolCanvas.delete('all')
        self.toolCanvas.create_text(120,40,text="Super Impose",font=("Comic Sans MS",24,"bold"),fill="#181818")
        self.toolCanvas.create_text(15,120,text="X Cordinate",font=("Verdana",12,"bold"),fill="black",anchor="nw")
        self.toolCanvas.create_window(140,116,window=self.xEntry,anchor="nw")         
        self.toolCanvas.create_text(15,150,text="Y Cordinate",font=("Verdana",12,"bold"),fill="black",anchor="nw")
        self.toolCanvas.create_window(140,146,window=self.yEntry,anchor="nw")         
        self.toolCanvas.create_window(78,228,window=self.imageOpenEntry,anchor="nw")
        self.toolCanvas.create_window(10,226,window=self.selectFileButton,anchor="nw")
        self.toolCanvas.create_window(10,300,window=self.superImposeButton,anchor="nw")
        self.toolCanvas.create_window(157,300,window=self.cancelButton,anchor="nw")
    def crop(self) :
        self.xEntry.delete(0,"end")
        self.yEntry.delete(0,"end")
        self.toolCanvas.delete('all')
        self.toolCanvas.create_text(130,30,text="Crop",font=("Comic Sans MS",24,"bold"),fill="#181818")
        self.toolCanvas.create_text(15,120,text="X Cordinate",font=("Verdana",12,"bold"),fill="black",anchor="nw")
        self.toolCanvas.create_window(140,116,window=self.xEntry,anchor="nw")         
        self.toolCanvas.create_text(15,150,text="Y Cordinate",font=("Verdana",12,"bold"),fill="black",anchor="nw")
        self.toolCanvas.create_window(140,146,window=self.yEntry,anchor="nw")         
        self.toolCanvas.create_text(15,200,text="Image width",font=("Verdana",12,"bold"),fill="black",anchor="nw")
        self.toolCanvas.create_text(15,230,text="Image height",font=("Verdana",12,"bold"),fill="black",anchor="nw")
        self.toolCanvas.create_window(140,196,window=self.widthEntry,anchor="nw")
        self.toolCanvas.create_window(140,226,window=self.heightEntry,anchor="nw")
        self.toolCanvas.create_window(40,300,window=self.cropButton,anchor="nw")
        self.toolCanvas.create_window(120,300,window=self.cancelButton,anchor="nw")
    def cropButtonHandler(self) :
        xCor=int(self.xEntry.get())
        yCor=int(self.yEntry.get())
        width=int(self.widthEntry.get())
        height=int(self.heightEntry.get()) 
        t=threading.Thread(target=self.cropCallback,args=((xCor,yCor),(width,height)))
        t.start()
    def grayScale(self) : 
        self.toolCanvas.delete('all')
    def brightness(self) :
        self.toolCanvas.delete('all')
        self.brightnessScale.set(100)
        self.toolCanvas.create_window(130,200,window=self.brightnessScale)         
        self.toolCanvas.create_text(130,100,text="Brightness",font=("Comic Sans MS",24,"bold"),fill="#181818")
        self.toolCanvas.create_window(130,240,window=self.scaleLabel)
        self.toolCanvas.create_window(130,300,window=self.cancelButton)
    def contrast(self) :
        self.toolCanvas.delete('all')
        self.contrastScale.set(100)
        self.toolCanvas.create_text(130,100,text="Contrast",font=("Comic Sans MS",24,"bold"),fill="#181818")
        self.toolCanvas.create_window(130,200,window=self.contrastScale)         
        self.toolCanvas.create_window(130,240,window=self.scaleLabel)
        self.toolCanvas.create_window(130,300,window=self.cancelButton)
    def rotate(self) :
        self.toolCanvas.delete('all')      
        self.toolCanvas.create_text(130,30,text="Rotate",font=("Comic Sans MS",24,"bold"),fill="#181818")
        self.toolCanvas.create_text(15,120,text="Rotate By ",font=("Verdana",14,"bold"),fill="black",anchor="nw")
        self.toolCanvas.create_window(130,120,window=self.rotateCombobox,anchor="nw")
        self.toolCanvas.create_window(40,200,window=self.rotateButton,anchor="nw")
        self.toolCanvas.create_window(130,200,window=self.cancelButton,anchor="nw")
    def updateScaleLabel(self,value) :
        value=int(float(value))
        self.scaleLabel.configure(text=f"{value} %")
    def flip(self) :
        self.toolCanvas.delete('all')      
        self.toolCanvas.create_text(130,30,text="Flip Image",font=("Comic Sans MS",24,"bold"),fill="#181818")
        self.toolCanvas.create_text(15,120,text="Flip : ",font=("Verdana",18,"bold"),fill="black",anchor="nw")
        self.toolCanvas.create_window(100,125,window=self.flipCombobox,anchor="nw")
        self.toolCanvas.create_window(40,190,window=self.flipButton,anchor="nw")
        self.toolCanvas.create_window(130,190,window=self.cancelButton,anchor="nw") 