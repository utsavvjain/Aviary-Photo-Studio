import tkinter
import tkinter.ttk
class StatusBar(tkinter.Frame) :
    def __init__(self,master,zoomCallback,undoCallback,redoCallback) :
        self.loadImages() 
        tkinter.Frame.__init__(self,master,width=1024,height=25)
        self.canvas=tkinter.Canvas(self,height=25,width=1024,bg="white",highlightthickness=1,highlightbackground="black")
        self.canvas.pack(fill=tkinter.BOTH,expand=1)
        self.style=tkinter.ttk.Style()
        self.style.theme_use('winnative')
        self.style.configure('MyStyle1.Horizontal.TScale',sliderthickness=1440,bordercolor='black',darkcolor="red")        
        self.zoomScale=tkinter.ttk.Scale(self.canvas,from_=1,to=200,orient=tkinter.HORIZONTAL,command=zoomCallback,state="disabled",style="MyStyle1.Horizontal.TScale")
        self.zoomLabel=tkinter.Label(self,text=f"Zoom : {self.zoomScale.get()}",font=("Veradana",8,"bold"))     
        self.undoButton=tkinter.Button(self,fg="white",border=4,width=18,height=18,image=self.img['undo'],bd=2,state="disabled",command=undoCallback)
        self.redoButton=tkinter.Button(self,fg="white",border=4,width=18,height=18,image=self.img['redo'],bd=2,state="disabled",command=redoCallback)
        self.canvas.create_window(1100,14,window=self.zoomScale) 
        self.canvas.create_window(1000,13,window=self.zoomLabel) 
        self.canvas.create_window(910,15,window=self.undoButton) 
        self.canvas.create_window(935,15,window=self.redoButton) 
        self.canvas.create_line(970,0,970,25,width=1,fill="#ADADAD")
        self.canvas.create_line(972,0,972,25,width=1,fill="white")
        self.canvas.create_line(880,0,880,25,width=1,fill="#ADADAD")
        self.canvas.create_line(882,0,882,25,width=1,fill="white")
        self.tip=tkinter.tix.Balloon(self)
        for sub in self.tip.subwidgets_all() : 
            sub.config(bg="white") 
        self.tip.bind_widget(self.redoButton,balloonmsg="Redo")
        self.tip.bind_widget(self.undoButton,balloonmsg="Undo")
        self.widgets=[self.zoomScale]   
    def setAll(self,state) :
        for wgt in self.widgets : wgt['state']=state
    def loadImages(self) :
        self.img={}
        self.img['undo']=tkinter.PhotoImage(file="images\\undo.png")         
        self.img['redo']=tkinter.PhotoImage(file="images\\redo.png")       	  	
    def updateFileDetails(self,name,size,resolution) :
        self.canvas.create_text(10,6,text=f"File : {name}",font=("Veradana",8,"bold"),anchor="nw")
        self.canvas.create_line(120,0,120,25,width=1,fill="#ADADAD")
        self.canvas.create_line(122,0,122,25,width=1,fill="white")
        self.canvas.create_text(155,6,text=f"File Size : {size} KB",font=("Veradana",8,"bold"),anchor="nw")
        self.canvas.create_line(300,0,300,25,width=1,fill="#ADADAD")
        self.canvas.create_line(302,0,302,25,width=1,fill="white")
        self.canvas.create_text(750,6,text=f"Resolution : {resolution}",font=("Veradana",8,"bold"),anchor="nw")     