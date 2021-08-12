import tkinter
import tkinter.ttk
from PIL import Image,ImageTk
import cv2
import tkinter.tix
import time
class ImageDisplayFrame(tkinter.Frame) :
    def __init__(self,master,height,width) :
        w=width
        h=height
        self.loadingJob=None
        tkinter.Frame.__init__(self,master,height=h,width=w)
        self.canvas=tkinter.Canvas(self,height=h,width=w,bg="#202020")
        vbar=tkinter.Scrollbar(self,orient=tkinter.VERTICAL,width=14)  
        vbar.pack(side=tkinter.RIGHT,fill=tkinter.Y)
        vbar.config(command=self.canvas.yview)
        hbar=tkinter.Scrollbar(self,orient=tkinter.HORIZONTAL,width=14)  
        hbar.pack(side=tkinter.BOTTOM,fill=tkinter.X)
        hbar.config(command=self.canvas.xview)
        self.canvas.config(xscrollcommand=hbar.set,yscrollcommand=vbar.set)
        self.canvas.pack(fill=tkinter.BOTH,expand=1)
        self.loadAnimationImages()
        self.animation=None
    def displayImage(self,img) : 
        self.canvas.delete('all')
        self.img=ImageTk.PhotoImage(img)                 
        height=self.img.height()
        width=self.img.width()
        self.canvas.create_image(10,10,image=self.img,anchor="nw")
        self.canvas.configure(scrollregion=(0,0,width,height))  
    def loadAnimationImages(self) :
        self.images=[]
        for i in range(1,28) :
            self.images.append(tkinter.PhotoImage(file="image.gif",format=f"gif -index {i}"))
    def getDimensions(self) :
        return self.img.width(),self.img.height()
    def displayLoadingAnimation(self,index) :
        if self.animation!=None : self.canvas.delete(self.animation)
        self.animation=self.canvas.create_image(530,309,image=self.images[index])              
        index+=1
        if index==27 : index=2
        self.update_idletasks()
        self.loadingJob=self.after(20,self.displayLoadingAnimation,index)
    def cancelLoadingAnimation(self) :
        self.after_cancel(self.loadingJob)       
        self.after_cancel(self.loadingJob)       

          