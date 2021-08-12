import tkinter
import tkinter.tix
import tkinter.ttk
import tkinter.filedialog
import numpy
import threading
from imagedisplayframe import *
import cv2
import PIL
import time
from buttonspanel  import *
from statusbar import *
from toolpanel import *
import os
import pathlib
import ctypes
class Undo :
    def __init__(self,btn) :
        self.undo=[None,None,None,None,None]
        self.btn=btn
        self.index=0 
        self.btn['state']="disabled"
    def append(self,data) :
        self.undo[self.index]=data
        self.index+=1
        if self.index>0 : self.btn['state']="normal"
        self.undo.append(None)
    def get(self) :
        self.index=self.index-1
        if self.index==0 : self.btn['state']="disabled"           
        data=self.undo[self.index]
        self.undo[self.index]=None
        return data
class Redo :
    def __init__(self,btn) :
        self.redo=[None,None,None,None,None]
        self.btn=btn
        self.btn['state']="disabled"
        self.index=0 
    def append(self,data) :
        self.redo[self.index]=data
        self.index+=1
        if self.index>0 : self.btn['state']="normal"
        self.redo.append(None)
    def get(self) :
        self.index=self.index-1
        if self.index==0 : self.btn['state']="disabled"           
        data=self.redo[self.index]
        self.redo[self.index]=None
        return data
class Window(tkinter.tix.Tk) :
    def __init__(self) :
        tkinter.tix.Tk.__init__(self)
        self.title("Image Editing Tool")
        width,height=ctypes.windll.user32.GetSystemMetrics(0),ctypes.windll.user32.GetSystemMetrics(1)
        self.desktopWidth=width
        self.desktopHeight=height 
        print(width,height)
        self.canvas=tkinter.Canvas(self,height=self.desktopHeight,width=self.desktopWidth,bg="#ADADAD")
        self.geometry(f"{self.desktopWidth}x{self.desktopHeight}+0+0")
        self.state("zoomed")
        self.resizable(0,0) 
        self.imageDisplayFrame=ImageDisplayFrame(self,645,1100)
        self.imageDisplayFrame.place(x=0,y=33)
        self.toolPanel=ToolPanel(self,brightnessScaleCallback=self.brightnessScaleClick,contrastScaleCallback=self.contrastScaleClick,cropCallback=self.cropImage,rotateCallback=self.rotateImage,flipCallback=self.flipImage,superImposeCallback=self.superImposeImage)
        self.toolPanel.place(x=1120,y=33) 
        self.buttonsPanel=ButtonPanel(self,grayScaleCallback=self.grayScale,contrastCallback=self.contrast,brightnessCallback=self.brightness,cropCallback=self.crop,rotateCallback=self.rotate,flipCallback=self.toolPanel.flip,superImpCallback=self.toolPanel.superImpose)
        self.buttonsPanel.pack(side=tkinter.TOP,fill=tkinter.X) 
        self.statusBar=StatusBar(self,zoomCallback=self.zoom,undoCallback=self.undoChange,redoCallback=self.redoChange) 
        self.statusBar.pack(side=tkinter.BOTTOM,fill=tkinter.X)
        self.menuBar=tkinter.Menu(self)
        self.config(menu=self.menuBar)
        #fileMenu
        self.fileMenu=tkinter.Menu(self.menuBar,tearoff=0)
        self.fileMenu.add_command(label="New")
        self.fileMenu.add_command(label="Open",command=self.openFile)
        self.fileMenu.add_command(label="Close")
        self.fileMenu.add_command(label="Save")
        self.fileMenu.add_command(label="Save as",state="disabled",command=self.saveAs)
        self.fileMenu.add_separator() 
        self.fileMenu.add_command(label="Exit",command=exit)
        #editMenu  
        self.editMenu=tkinter.Menu(self.menuBar,tearoff=0)
        self.editMenu.add_command(label="Cut")
        self.editMenu.add_command(label="Copy")
        self.editMenu.add_command(label="Paste")
        #veiwMenu
        self.viewMenu=tkinter.Menu(self.menuBar,tearoff=0)
        self.viewMenu.add_command(label="Zoom in",command=self.zoomIn)
        self.viewMenu.add_command(label="Zoom out",command=self.zoomOut)
        #viewMenu->magnificationMenu
        self.magnificationMenu=tkinter.Menu(self.viewMenu,tearoff=0)
        self.magnificationMenu.add_command(label="50")
        self.magnificationMenu.add_command(label="100")
        self.magnificationMenu.add_command(label="150")
        self.magnificationMenu.add_command(label="200")
        self.viewMenu.add_cascade(label="Magnification",menu=self.magnificationMenu)
        self.viewMenu.add_command(label="Full screen")
    
        #transformMenu
        self.transformMenu=tkinter.Menu(self.menuBar,tearoff=0)
        self.transformMenu.add_command(label="Crop")
        self.transformMenu.add_command(label="Rotate")
        self.transformMenu.add_command(label="Rotate 90\u00B0 left",command=lambda : self.rotateImage("90 degrees","left"))
        self.transformMenu.add_command(label="Rotate 90\u00B0 right",command=lambda : self.rotateImage("90 degrees","right"))
        self.transformMenu.add_command(label="Rotate 180\u00B0",command=lambda : self.rotateImage("180 degrees"))
        self.transformMenu.add_command(label="Flip horizontal",command=lambda : self.flipImage("h"))
        self.transformMenu.add_command(label="Flip vertical",command=lambda : self.flipImage("v"))

        #filterMenu
        self.filterMenu=tkinter.Menu(self.menuBar,tearoff=0)
        self.filterMenu.add_command(label="Mean")
        self.filterMenu.add_command(label="Median")
        self.filterMenu.add_command(label="Fourier transform")
        self.filterMenu.add_command(label="Gaussian smothing")
        self.filterMenu.add_command(label="Unsharp")
        self.filterMenu.add_command(label="Laplacian")


        self.menuBar.add_cascade(label="File",menu=self.fileMenu)
        self.menuBar.add_cascade(label="Edit",menu=self.editMenu)
        self.menuBar.add_cascade(label="View",menu=self.viewMenu)
        self.menuBar.add_cascade(label="Transform",menu=self.transformMenu)
        self.menuBar.add_cascade(label="Filter",menu=self.filterMenu)
        self.animation=None
        self.state=None
        self.tool=None
        self.isUpdating=False 
        self.imageData=None
        self.menuOptions={self.fileMenu:["Close","Save"],self.editMenu:["Cut","Copy","Paste"],self.viewMenu:["Zoom in","Zoom out","Full screen"],self.transformMenu:["Crop","Rotate","Rotate 90\u00B0 left","Rotate 90\u00B0 right","Rotate 180\u00B0","Flip horizontal","Flip vertical"],self.filterMenu:["Mean","Median","Fourier transform","Gaussian smothing","Unsharp","Laplacian"],self.magnificationMenu:["50","100","150","200"]} 
        for i in self.menuOptions.keys() : 
            for entry in self.menuOptions[i] :
                i.entryconfig(entry,state="disabled")
    def loadImages(self) :
        self.img={}
        self.img['gray']=tkinter.PhotoImage(file="images\\grayScale.png")         
        self.img['brightness']=tkinter.PhotoImage(file="images\\brightness.png")         
        self.img['contrast']=tkinter.PhotoImage(file="images\\contrast.png")         
        self.img['undo']=tkinter.PhotoImage(file="images\\undo.png")         
        self.img['redo']=tkinter.PhotoImage(file="images\\redo.png")         	
    def openFile(self) :
        self.fileName=tkinter.filedialog.askopenfilename(title="Open Image",initialdir='.',filetypes=(('Jpg files','*.jpg'),("All files","*.*")))   
        if(len(self.fileName)==0) : return
        self.imageData=cv2.imread(self.fileName)
        img=cv2.cvtColor(self.imageData,cv2.COLOR_BGR2RGB)
        self.image=PIL.Image.fromarray(img)
        self.imageWidth=self.image.width
        self.imageHeight=self.image.height
        self.imageDisplayFrame.displayImage(self.image)
        self.statusBar.setAll("normal") 
        self.buttonsPanel.setAll("normal")
        self.undo=Undo(self.statusBar.undoButton)
        self.redo=Redo(self.statusBar.redoButton)
        self.statusBar.zoomScale.set(100)
        self.fileMenu.entryconfig("Save as",state="normal")	         
        resolution=f"{self.imageData.shape[0]}x{self.imageData.shape[1]}"
        size=int((os.stat(self.fileName).st_size)/1024)
        self.statusBar.updateFileDetails(pathlib.Path(self.fileName).name,size,resolution) 
        for i in self.menuOptions.keys() : 
            for entry in self.menuOptions[i] :
                i.entryconfig(entry,state="normal")
    def zoomIn(self) :
        per=int(self.statusBar.zoomScale.get()+self.statusBar.zoomScale.get()*.25)	
        self.statusBar.zoomScale.set(per)
    def zoomOut(self) :
        per=self.statusBar.zoomScale.get()-self.statusBar.zoomScale.get()*.25	
        self.statusBar.zoomScale.set(per)
    def zoom(self,percent) :
        factor=self.statusBar.zoomScale.get()/100
        self.statusBar.zoomLabel.configure(text=f"Zoom : {int(self.statusBar.zoomScale.get())}%")
        width=int(self.imageWidth*factor)
        height=int(self.imageHeight*factor)
        if width<=0 : width=1
        if height<=0 : height=1
        self.imageDisplayFrame.displayImage(self.image.resize((width,height))) 
    def brightness(self) :
        self.toolPanel.brightness() 
    def contrast(self) :
        self.toolPanel.contrast() 
    def crop(self) :
        self.toolPanel.crop() 
    def rotate(self) :
        self.toolPanel.rotate()
    def superImposeImage(self,fileName,cordinates) :
        if self.isUpdating : return 
        self.buttonsPanel.setAll("disabled")
        self.statusBar.setAll("disabled")
        self.imageDisplayFrame.displayLoadingAnimation(2)
        self.isUpdating=True 
        self.undo.append((self.image,self.imageData.copy(),(self.imageData.shape[0],self.imageData.shape[1])))
        image2Data=cv2.imread(fileName)
        c1=cordinates[0]
        r1=cordinates[1]
        c2=image2Data.shape[1]-1+c1
        r2=image2Data.shape[0]-1+r1
        if r2>=self.imageData.shape[0] : r2=self.imageData.shape[0]-1
        if c2>=self.imageData.shape[1] : c2=self.imageData.shape[1]-1
        rr=0
        for r in range(r1,r2) :
            cc=0
            for c in range(c1,c2) :
                self.imageData[r][c]=image2Data[rr][cc]
                cc+=1
            rr+=1 
        self.imageDisplayFrame.cancelLoadingAnimation()       
        img=cv2.cvtColor(self.imageData,cv2.COLOR_BGR2RGB)
        self.image=PIL.Image.fromarray(img)	
        self.buttonsPanel.setAll("normal")
        self.statusBar.setAll("normal") 
        width,height=self.imageDisplayFrame.getDimensions()
        self.imageDisplayFrame.displayImage(self.image)
        self.toolPanel.contrastScale['state']="normal"
        self.isUpdating=False
    def flipImage(self,state) :
        if self.isUpdating : return 
        self.buttonsPanel.setAll("disabled")
        self.statusBar.setAll("disabled")
        self.imageDisplayFrame.displayLoadingAnimation(2)
        self.isUpdating=True 
        self.undo.append((self.image,self.imageData.copy(),(self.imageData.shape[0],self.imageData.shape[1])))
        rows=self.imageData.shape[0]
        columns=self.imageData.shape[1]
        newImage=numpy.zeros((rows,columns,3),numpy.uint8)
        if state=="Horizontal" :
            for i in range(rows) :
                c=0
                for j in range(columns-1,0,-1) :
                    newImage[i][j]=self.imageData[i][c]
                    c+=1
        if state=="Vertical" : 
            c=0	
            for i in range(rows-1,-1,-1) :
                for j in range(columns) :
                    newImage[i][j]=self.imageData[c][j]
                c+=1
        self.imageData=newImage
        self.imageDisplayFrame.cancelLoadingAnimation()       
        img=cv2.cvtColor(self.imageData,cv2.COLOR_BGR2RGB)
        self.image=PIL.Image.fromarray(img)	
        self.buttonsPanel.setAll("normal")
        self.statusBar.setAll("normal") 
        width,height=self.imageDisplayFrame.getDimensions()
        self.imageDisplayFrame.displayImage(self.image)
        self.toolPanel.contrastScale['state']="normal"
        self.isUpdating=False                  
    def rotateImage(self,state) :
        if self.isUpdating : return 
        self.buttonsPanel.setAll("disabled")
        self.statusBar.setAll("disabled")
        self.imageDisplayFrame.displayLoadingAnimation(2)
        self.isUpdating=True 
        self.undo.append((self.image,self.imageData.copy(),(self.imageData.shape[0],self.imageData.shape[1])))
        rows=self.imageData.shape[0]
        columns=self.imageData.shape[1]
        if state=="90\u00B0 anticlockwise" :
            newImage=numpy.zeros((columns,rows,3),numpy.uint8)
            for i in range(rows) :
                for j in range(columns) :
                    newImage[columns-j-1][i]=self.imageData[i][j]
        if state=="90\u00B0 clockwise" :  
            newImage=numpy.zeros((columns,rows,3),numpy.uint8)
            for i in range(rows) :
                for j in range(columns) :
                    newImage[j][rows-i-1]=self.imageData[i][j]
        if state=="180\u00B0" :
            newImage=numpy.zeros((rows,columns,3),numpy.uint8)
            a=0
            for i in range(rows-1,0,-1) :
                b=0
                for j in range(columns-1,0,-1) :
                    newImage[i][j]=self.imageData[a][b]
                    b+=1
                a+=1 
        self.imageData=newImage 
        self.imageDisplayFrame.cancelLoadingAnimation()       
        self.imageData=newImage
        img=cv2.cvtColor(self.imageData,cv2.COLOR_BGR2RGB)
        self.image=PIL.Image.fromarray(img)	
        self.buttonsPanel.setAll("normal")
        self.statusBar.setAll("normal") 
        width,height=self.imageDisplayFrame.getDimensions()
        self.imageDisplayFrame.displayImage(self.image)
        self.toolPanel.contrastScale['state']="normal"
        self.isUpdating=False 
    def cropImage(self,cropFrom,cropSize) :
        if self.isUpdating : return 
        self.buttonsPanel.setAll("disabled")
        self.statusBar.setAll("disabled")
        self.imageDisplayFrame.displayLoadingAnimation(2)
        self.isUpdating=True 
        self.undo.append((self.image,self.imageData.copy(),(self.imageData.shape[0],self.imageData.shape[1])))
        c1=cropFrom[0]
        r1=cropFrom[1]
        c2=cropSize[0]-1+c1
        r2=cropSize[1]-1+r1
        if r2>=self.imageData.shape[0] : r2=self.imageData.shape[0]-1
        if c2>=self.imageData.shape[1] : c2=self.imageData.shape[1]-1
        cropSize=(c2-c1+1,r2-r1+1)
        newImage=numpy.zeros((cropSize[1],cropSize[0],3),dtype=numpy.uint8)
        rr=0
        r=r1
        while r<=r2 :
            cc=0
            c=c1
            while c<=c2 :
                newImage[rr][cc]=self.imageData[r][c]
                cc+=1
                c+=1
            rr+=1
            r+=1
        self.imageDisplayFrame.cancelLoadingAnimation()       
        self.imageData=newImage
        img=cv2.cvtColor(self.imageData,cv2.COLOR_BGR2RGB)
        self.image=PIL.Image.fromarray(img)	
        self.buttonsPanel.setAll("normal")
        self.statusBar.setAll("normal") 
        width,height=self.imageDisplayFrame.getDimensions()
        self.imageDisplayFrame.displayImage(self.image)
        self.toolPanel.contrastScale['state']="normal"
        self.isUpdating=False 
    def grayScale(self) :
        self.undo.append((self.image,self.imageData.copy(),(self.imageData.shape[0],self.imageData.shape[1])))
        self.buttonsPanel.setAll("disabled")
        self.statusBar.setAll("disabled")
        self.toolPanel.grayScale() 
        thread=threading.Thread(target=self.makeGrayScale)
        self.imageDisplayFrame.displayLoadingAnimation(2)
        thread.start()        
    def makeGrayScale(self) :
        for r in range(self.imageData.shape[0]) :
            for c in range(self.imageData.shape[1]) :
                rgb=self.imageData[r][c]
                blue=int(rgb[0])*0.3
                green=int(rgb[1])*0.59
                red=int(rgb[2])*0.11
                total=red+green+blue
                self.imageData[r][c]=(total,total,total)
        self.imageDisplayFrame.cancelLoadingAnimation()
        img=cv2.cvtColor(self.imageData,cv2.COLOR_BGR2RGB)
        self.image=PIL.Image.fromarray(img)	
        self.buttonsPanel.setAll("normal")
        self.statusBar.setAll("normal") 
        width,height=self.imageDisplayFrame.getDimensions()
        self.imageDisplayFrame.displayImage(self.image.resize((width,height)))
    def brightnessScaleClick(self,event) :
        self.undo.append((self.image,self.imageData.copy(),(self.imageData.shape[0],self.imageData.shape[1])))
        if self.isUpdating : return 
        self.isUpdating=True 
        self.toolPanel.brightnessScale['state']="disabled"
        self.buttonsPanel.setAll("disabled")
        self.statusBar.setAll("disabled") 
        value=float(self.toolPanel.brightnessScale.get())
        value=int(value)
        if value<100 : factor=value-100
        else : factor=(value-100)
        brightness=int(factor)
        self.imageDisplayFrame.displayLoadingAnimation(1)
        thread=threading.Thread(target=self.changeBrightness,args=(brightness,))
        thread.start()
    def contrastScaleClick(self,event) :
        self.undo.append((self.image,self.imageData.copy(),(self.imageData.shape[0],self.imageData.shape[1]))) 
        if self.isUpdating : return 
        self.isUpdating=True 
        self.toolPanel.contrastScale['state']="disabled"
        self.buttonsPanel.setAll("disabled")
        self.statusBar.setAll("disabled") 
        value=float(self.toolPanel.contrastScale.get())
        value=int(value)
        factor=value-100
        contrast=int(factor)
        f=(259*(255+contrast))/(255*(259-contrast))
        self.imageDisplayFrame.displayLoadingAnimation(1)
        thread=threading.Thread(target=self.changeContrast,args=(f,))
        thread.start()
    def changeContrast(self,factor) :
        for r in range(self.imageData.shape[0]) :
            for c in range(self.imageData.shape[1]) :
                rgb=self.imageData[r][c]
                blue=int(rgb[0])
                green=int(rgb[1])
                red=int(rgb[2])
                self.imageData[r][c]=(self.truncate(factor*(blue-128)+128),self.truncate(factor*(green-128)+128),self.truncate(factor*(red-128)+128)) 
        self.imageDisplayFrame.cancelLoadingAnimation()
        img=cv2.cvtColor(self.imageData,cv2.COLOR_BGR2RGB)
        self.image=PIL.Image.fromarray(img)	
        self.buttonsPanel.setAll("normal")
        self.statusBar.setAll("normal") 
        width,height=self.imageDisplayFrame.getDimensions()
        self.imageDisplayFrame.displayImage(self.image.resize((width,height)))
        self.toolPanel.contrastScale['state']="normal"
        self.isUpdating=False 
        self.toolPanel.contrastScale.set(100) 
    def changeBrightness(self,brightness) :
        for r in range(self.imageData.shape[0]) :
            for c in range(self.imageData.shape[1]) :
                rgb=self.imageData[r][c]
                blue=int(rgb[0]) 
                green=int(rgb[1])
                red=int(rgb[2])
                self.imageData[r][c]=(self.truncate(blue+brightness),self.truncate(green+brightness),self.truncate(red+brightness)) 
        self.imageDisplayFrame.cancelLoadingAnimation()
        img=cv2.cvtColor(self.imageData,cv2.COLOR_BGR2RGB)
        self.image=PIL.Image.fromarray(img)	
        self.buttonsPanel.setAll("normal")
        self.statusBar.setAll("normal") 
        width,height=self.imageDisplayFrame.getDimensions()
        self.imageDisplayFrame.displayImage(self.image.resize((width,height)))
        self.toolPanel.brightnessScale['state']="normal"
        self.isUpdating=False 
        self.toolPanel.brightnessScale.set(100)
    def truncate(self,color) :
        if color<0 : return 0
        elif color>255 : return 255
        else : return color 
    def undoChange(self) :
        data=self.undo.get()
        self.redo.append((self.image,self.imageData,(self.imageData.shape[0],self.imageData.shape[1])))     
        self.image=data[0]
        self.imageData=data[1]
        height,width=data[2][0],data[2][1]
        self.imageDisplayFrame.displayImage(self.image.resize((width,height)))
        self.statusBar.zoomScale.set(100)
    def redoChange(self) :
        self.undo.append((self.image,self.imageData,(self.imageData.shape[0],self.imageData.shape[1])))
        data=self.redo.get()
        self.image=data[0]
        self.imageData=data[1] 
        height,width=data[2][0],data[2][1]
        self.imageDisplayFrame.displayImage(self.image.resize((width,height)))
        self.statusBar.zoomScale.set(100)
    def saveAs(self) :
        file=tkinter.filedialog.asksaveasfile(filetypes=(("Jpg files","*.jpg"),))
        if file==None : return
        cv2.imwrite(file.name,self.imageData)
main=Window()
main.mainloop()