import tkinter
import tkinter.ttk
class ButtonPanel(tkinter.Frame) :
    def __init__(self,master,brightnessCallback,grayScaleCallback,contrastCallback,cropCallback,rotateCallback,flipCallback,superImpCallback) :
        tkinter.Frame.__init__(self,master,width=100,height=618,bg="grey")
        self.loadImages() 
        self.grayScaleButton=tkinter.Button(self,bg="black",fg="white",border=2,width=24,height=24,image=self.img['gray'],command=grayScaleCallback,state="disabled")
        self.brightnessButton=tkinter.Button(self,bg="black",fg="white",border=2,width=24,height=24,image=self.img['brightness'],command=brightnessCallback,state="disabled")
        self.contrastButton=tkinter.Button(self,bg="black",fg="white",border=2,width=24,height=24,image=self.img['contrast'],command=contrastCallback,state="disabled")
        self.cropButton=tkinter.Button(self,bg="black",fg="white",border=2,width=24,height=24,image=self.img['crop'],command=cropCallback,state="disabled")
        self.rotateButton=tkinter.Button(self,bg="black",fg="white",border=2,width=24,height=24,image=self.img['rotate'],state="disabled",command=rotateCallback)
        self.flipButton=tkinter.Button(self,bg="black",fg="white",border=2,width=24,height=24,image=self.img['flip'],state="disabled",command=flipCallback)
        self.superImposeButton=tkinter.Button(self,bg="black",fg="white",border=2,width=24,height=24,image=self.img['superImp'],state="disabled",command=superImpCallback)
        self.tip=tkinter.tix.Balloon(master)
        for sub in self.tip.subwidgets_all() : 
            sub.config(bg="white") 
        self.tip.bind_widget(self.grayScaleButton,balloonmsg="Gray Scale")
        self.tip.bind_widget(self.brightnessButton,balloonmsg="Brightness")
        self.tip.bind_widget(self.contrastButton,balloonmsg="Contrast")
        self.tip.bind_widget(self.rotateButton,balloonmsg="Rotate")
        self.tip.bind_widget(self.flipButton,balloonmsg="Flip")      
        self.tip.bind_widget(self.superImposeButton,balloonmsg="Super-Impose")
        self.grayScaleButton.pack(side=tkinter.LEFT,padx=2,pady=2)  
        self.brightnessButton.pack(side=tkinter.LEFT,padx=2,pady=2)  
        self.contrastButton.pack(side=tkinter.LEFT,padx=2,pady=2)  
        self.cropButton.pack(side=tkinter.LEFT,padx=2,pady=2)  
        self.rotateButton.pack(side=tkinter.LEFT,padx=2,pady=2)  
        self.flipButton.pack(side=tkinter.LEFT,padx=2,pady=2)  
        self.superImposeButton.pack(side=tkinter.LEFT,padx=2,pady=2)  
        self.buttons=[self.grayScaleButton,self.contrastButton,self.brightnessButton,self.cropButton,self.rotateButton,self.superImposeButton,self.flipButton]
    def loadImages(self) :
        self.img={}
        self.img['gray']=tkinter.PhotoImage(file="images\\grayScale.png")         
        self.img['brightness']=tkinter.PhotoImage(file="images\\brightness.png")         
        self.img['contrast']=tkinter.PhotoImage(file="images\\contrast.png")         
        self.img['crop']=tkinter.PhotoImage(file="images\\crop.png")         
        self.img['rotate']=tkinter.PhotoImage(file="images\\rotate.png")         
        self.img['flip']=tkinter.PhotoImage(file="images\\flip.png")         
        self.img['superImp']=tkinter.PhotoImage(file="images\\superImp.png")         

    def setAll(self,state) :
        for btn in self.buttons : btn['state']=state         