import cv2
import numpy as np
from appJar import *


cap = cv2.VideoCapture('/dev/video0')
font = cv2.FONT_HERSHEY_COMPLEX
program=gui("Title","300x300")
def ButtonHandler(select):
    
    if select == "Uygula":
        if program.getRadioButton("option") == "Mavi Dikdörtgen":
            program.infoBox("Message","Mavi Dikdörtgen Algılandı\n\n")

            while True:
                    _,frame=cap.read()
        
    
                    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
                    lower_blue=np.array([100, 55, 55])#blue detection
                    upper_blue=np.array([140, 255, 255])
                       
                    mask=cv2.inRange(hsv,lower_blue,upper_blue)
                    kernel=np.ones((2,2),np.uint8)
                    erosion=cv2.erode(mask,kernel,iterations = 1)#morfolojik filtreleme
    
                    #Contours detection
                    _, contours, _ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
                    for cnt in contours:
                        area=cv2.contourArea(cnt)
                        approx=cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)
                        x=approx.ravel()[0]
                        y=approx.ravel()[1]
        
        
                
                        if area > 400:
                            cv2.drawContours(frame,[approx],0,(0,0,0),5)
            
            
                            if len(approx) == 4:
                              cv2.putText(frame, "Dikdortgen", (x, y), font, 1, (0, 0, 0))
                                                
                        cv2.imshow("ekran",frame)
        
    
                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        break
  
            cv2.destroyAllWindows()
    
        if program.getRadioButton("option") == "Mavi Üçgen":
            program.infoBox("Message","Mavi Üçgen Seçildi\n\n")
            
            while True:
                    _,frame=cap.read()
        
    
                    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
                    lower_blue=np.array([95, 65, 65])#blue detection
                    upper_blue=np.array([145, 255, 255])
                       
                    mask=cv2.inRange(hsv,lower_blue,upper_blue)
                    kernel=np.ones((2,2),np.uint8)
                    erosion=cv2.erode(mask,kernel,iterations = 1)
    
                    #Contours detection
                    _, contours, _ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
                    for cnt in contours:
                        area=cv2.contourArea(cnt)
                        approx=cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)
                        x=approx.ravel()[0]
                        y=approx.ravel()[1]
        
                        if area > 400 :
                            cv2.drawContours(frame,[approx],0,(0,0,0),5)
                     

                            if len(approx)==3 :
                                cv2.putText(frame, "Ucgen", (x, y), font, 1, (0, 0, 0))
                    
                    cv2.imshow("Frame",frame)
        
    
                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        break
  
            cv2.destroyAllWindows()
			
			 
    init = sl.InitParameters()
    init.camera_resolution = sl.RESOLUTION.RESOLUTION_HD720
    init.depth_mode = sl.DEPTH_MODE.DEPTH_MODE_PERFORMANCE	
    init.coordinate_units = sl.UNIT.UNIT_METER
    init.camera_fps =30
            
        if program.getRadioButton("option") == "Mavi Beşgen":
            program.infoBox("Message","Mavi Beşgen Seçildi\n\n")
            
            while True:
                    _,frame=cap.read()
        
    
                    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
                    lower_blue=np.array([100, 55, 55])#blue detection
                    upper_blue=np.array([140, 255, 255])
                       
                    mask=cv2.inRange(hsv,lower_blue,upper_blue)
                    kernel=np.ones((2,2),np.uint8)
                    erosion=cv2.erode(mask,kernel,iterations = 1)
    
                    #Contours detection
                    _, contours, _ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
                    for cnt in contours:
                        area=cv2.contourArea(cnt)
                        approx=cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)
                        x=approx.ravel()[0]
                        y=approx.ravel()[1]
        
                        if area > 400 :
                            cv2.drawContours(frame,[approx],0,(0,0,0),5)
                     

                            if len(approx)==5 :
                                cv2.putText(frame, "Besgen", (x, y), font, 1, (0, 0, 0))
                    
                        cv2.imshow("Frame",frame)
        
    
                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        break
  
            cv2.destroyAllWindows()
        
        if program.getRadioButton("option") == "Yeşil Beşgen":
            program.infoBox("Message","Yeşil Beşgen Seçildi\n\n")
            
            while True:
                    _,frame=cap.read()
        
    
                    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
                    lower_blue=np.array([36, 55, 55])#blue detection
                    upper_blue=np.array([80, 255, 255])
                       
                    mask=cv2.inRange(hsv,lower_blue,upper_blue)
                    kernel=np.ones((2,2),np.uint8)
                    erosion=cv2.erode(mask,kernel,iterations = 1)
    
                    #Contours detection
                    _, contours, _ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
                    for cnt in contours:
                        area=cv2.contourArea(cnt)
                        approx=cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)
                        x=approx.ravel()[0]
                        y=approx.ravel()[1]
        
                        if area > 400 :
                            cv2.drawContours(frame,[approx],0,(0,0,0),5)
                     

                            if len(approx)==5 :
                                cv2.putText(frame, "Besgen", (x, y), font, 1, (0, 0, 0))
                    
                        cv2.imshow("Frame",frame)
        
    
                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        break
  
            cv2.destroyAllWindows()
            
        if program.getRadioButton("option") == "Yeşil Dikdörtgen":
            program.infoBox("Message","Yeşil Dikdörtgen Seçildi\n\n")
            
            while True:
                    _,frame=cap.read()
        
    
                    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
                    lower_blue=np.array([36, 55, 55])#blue detection
                    upper_blue=np.array([80, 255, 255])
                       
                    mask=cv2.inRange(hsv,lower_blue,upper_blue)
                    kernel=np.ones((2,2),np.uint8)
                    erosion=cv2.erode(mask,kernel,iterations = 1)
    
                    #Contours detection
                    _, contours, _ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
                    for cnt in contours:
                        area=cv2.contourArea(cnt)
                        approx=cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)
                        x=approx.ravel()[0]
                        y=approx.ravel()[1]
        
                        if area > 400 :
                            cv2.drawContours(frame,[approx],0,(0,0,0),5)
                     

                            if len(approx)==4 :
                                cv2.putText(frame, "Dikdortgen", (x, y), font, 1, (0, 0, 0))
                    
                        cv2.imshow("Frame",frame)
        
    
                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        break
  
            cv2.destroyAllWindows()            
        if program.getRadioButton("option") == "Yeşil Üçgen":
            program.infoBox("Message","Yeşil Üçgen Seçildi\n\n")
            
            while True:
                    _,frame=cap.read()
        
    
                    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
                    lower_blue=np.array([36, 55, 55])#blue detection
                    upper_blue=np.array([80, 255, 255])
                       
                    mask=cv2.inRange(hsv,lower_blue,upper_blue)
                    kernel=np.ones((2,2),np.uint8)
                    erosion=cv2.erode(mask,kernel,iterations = 1)
    
                    #Contours detection
                    _, contours, _ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
                    for cnt in contours:
                        area=cv2.contourArea(cnt)
                        approx=cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)
                        x=approx.ravel()[0]
                        y=approx.ravel()[1]
        
                        if area > 400 :
                            cv2.drawContours(frame,[approx],0,(0,0,0),5)
                     

                            if len(approx)==3 :
                                cv2.putText(frame, "Ucgen", (x, y), font, 1, (0, 0, 0))
                    
                        cv2.imshow("Frame",frame)
        
    
                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        break
  
            cv2.destroyAllWindows()
            
        if program.getRadioButton("option") == "Sarı Üçgen":
            program.infoBox("Message","Sarı Üçgen Seçildi\n\n")
            
            while True:
                    _,frame=cap.read()
        
    
                    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
                    lower_blue=np.array([24, 55, 55])#blue detection
                    upper_blue=np.array([35, 255, 255])
                       
                    mask=cv2.inRange(hsv,lower_blue,upper_blue)
                    kernel=np.ones((2,2),np.uint8)
                    erosion=cv2.erode(mask,kernel,iterations = 1)
    
                    #Contours detection
                    _, contours, _ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
                    for cnt in contours:
                        area=cv2.contourArea(cnt)
                        approx=cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)
                        x=approx.ravel()[0]
                        y=approx.ravel()[1]
        
                        if area > 400 :
                            cv2.drawContours(frame,[approx],0,(0,0,0),5)
                     

                            if len(approx)==3 :
                                cv2.putText(frame, "Ucgen", (x, y), font, 1, (0, 0, 0))
                    
                        cv2.imshow("Frame",frame)
        
    
                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        break
  
            cv2.destroyAllWindows()
            
        if program.getRadioButton("option") == "Sarı Dikdörtgen":
            program.infoBox("Message","Sarı Dikdörtgen Seçildi\n\n")
            
            while True:
                    _,frame=cap.read()
        
    
                    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
                    lower_blue=np.array([24, 55, 55])
                    upper_blue=np.array([35, 255, 255])
                       
                    mask=cv2.inRange(hsv,lower_blue,upper_blue)
                    kernel=np.ones((2,2),np.uint8)
                    erosion=cv2.erode(mask,kernel,iterations = 1)
    
                    #Contours detection
                    _, contours, _ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
                    for cnt in contours:
                        area=cv2.contourArea(cnt)
                        approx=cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)
                        x=approx.ravel()[0]
                        y=approx.ravel()[1]
        
                        if area > 400 :
                            cv2.drawContours(frame,[approx],0,(0,0,0),5)
                     

                            if len(approx)==4 :
                                cv2.putText(frame, "Dikdortgen", (x, y), font, 1, (0, 0, 0))
                    
                        cv2.imshow("Frame",frame)
        
    
                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        break
  
            cv2.destroyAllWindows()             
        nn=50    
        if program.getRadioButton("option") == "Sarı Beşgen":
            program.infoBox("Message","Sarı Beşgen Seçildi\n\n")
			
			  for l in range(0,1280,nn):
                
                for k in range(0,720,nn):
                    
                    err, point_cloud_value = point_cloud.get_value(l, k)
                    mesafeler[p,2] = math.sqrt(point_cloud_value[0] * point_cloud_value[0] +
                                 point_cloud_value[1] * point_cloud_value[1] +
                                 point_cloud_value[2] * point_cloud_value[2]) 

                    if (math.isnan(mesafeler[p,2])==True): 
                        mesafeler[p,2]=0

                    mesafeler_[kp,lp]=mesafeler[p,2]
                    mesafeler[p,0]=k
                    mesafeler[p,1]=l
                      
                    
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.rectangle(depth_image_ocv , (l,k) , (l+2,k+2) , (0,255,0) ,1)
                    cv2.rectangle(image_ocv , (l,k) , (l+2,k+2) , (0,255,0) ,1)
                    cv2.putText(depth_image_ocv,str(round(mesafeler[p,2])), (l,k), font, 0.3, (255,255,0),1,cv2.LINE_AA)
                    p=p+1
                    kp=kp+1
                kp=0
                lp=lp+1
            lp=0
            
            while True:
                    _,frame=cap.read()
        
    
                    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
                    lower_blue=np.array([24,100, 100])
                    upper_blue=np.array([35, 255, 255])
                       
                    mask=cv2.inRange(hsv,lower_blue,upper_blue)
                    kernel=np.ones((2,2),np.uint8)
                    erosion=cv2.erode(mask,kernel,iterations = 1)
    
                    #Contours detection
                    _, contours, _ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
                    for cnt in contours:
                        area=cv2.contourArea(cnt)
                        approx=cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)
                        x=approx.ravel()[0]
                        y=approx.ravel()[1]
        
                        if area > 400 :
                            cv2.drawContours(frame,[approx],0,(0,0,0),5)
                     

                            if len(approx)==5 :
                                cv2.putText(frame, "Besgen", (x, y), font, 1, (0, 0, 0))
                    
                        cv2.imshow("Frame",frame)
        
    
                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        break
  
            cv2.destroyAllWindows()           

#RadioButtons
program.addRadioButton("option","Mavi Üçgen")
program.addRadioButton("option","Mavi Dikdörtgen")
program.addRadioButton("option","Mavi Beşgen")
program.addRadioButton("option","Yeşil Üçgen")
program.addRadioButton("option","Yeşil Dikdörtgen")
program.addRadioButton("option","Yeşil Beşgen")
program.addRadioButton("option","Sarı Üçgen")
program.addRadioButton("option","Sarı Dikdörtgen")
program.addRadioButton("option","Sarı Beşgen")

#Button
program.addButtons(["Uygula"], ButtonHandler)
program.go()