#bu kod deneme_3 ün kopyası niteliğindeddir
#bu koddaki silinen yorum satırları deneme_4.0.0 da mevcuttur.
#Bu yazılımda 3 farklı görünüt kaydı alıyotuz
#1.svo - sürüş kayıt
#2.avi - sol kameradan görüntü
#3.avi - derinlik görünütü (siyaz beyaz olan)
#txt ve path dosyaları klasörlendi
#mesafeler matrisi ayrıca mesafeler_ şeklinde 18x32 ye dönüştürüldü
#frameyi resim resim kaydetme eklendi

import sys
import numpy as np
import pyzed.sl as sl
import cv2
import math

path = "./"
path1 = "/media/nvidia/jetdisk/matris_2x576/"
path2 = "/media/nvidia/jetdisk/matris_18x32/"
path3 = "/media/nvidia/jetdisk/resim/"
path4 = "/media/nvidia/jetdisk/resim_depth/"
path6 = "/media/nvidia/jetdisk/video_norm/"
path7 = "/media/nvidia/jetdisk/video_depth/"
path8 = "/media/nvidia/jetdisk/kayit_svo/"
point_cloud_format = sl.POINT_CLOUD_FORMAT.POINT_CLOUD_FORMAT_XYZ_ASCII
depth_format = sl.DEPTH_FORMAT.DEPTH_FORMAT_PNG

#Main forksiyonumuz
def main() :

    # Zed kamera objesi oluştruruldu
    zed = sl.Camera()
    
    sayici=1
    # Video kayıt için kod çözücü seçildi ve kayıt dosyaları oluşturuldu. --with help of opencv-- 
    fourcc =cv2.VideoWriter_fourcc(*'MJPG')
    left = cv2.VideoWriter(path6+"Left_camera.avi", fourcc, 7, (1280, 720),True)
    depth = cv2.VideoWriter(path7+"Depth_camera.avi", fourcc, 7, (1280, 720),True)
    
    # Kamera Parametre Ayarları
    init = sl.InitParameters()
    init.camera_resolution = sl.RESOLUTION.RESOLUTION_HD720
    init.depth_mode = sl.DEPTH_MODE.DEPTH_MODE_PERFORMANCE	
    init.coordinate_units = sl.UNIT.UNIT_METER
    init.camera_fps =30
 
    # Kamerayı denetle ve aç
    err = zed.open(init)
    if err != sl.ERROR_CODE.SUCCESS :
        print(repr(err))
        zed.close()
        exit(1)

    # Set runtime parameters after opening the camera
    runtime = sl.RuntimeParameters()
    runtime.sensing_mode = sl.SENSING_MODE.SENSING_MODE_STANDARD

    # Kamera çözünürlükleri okunuyor
    image_size = zed.get_resolution()
    width = image_size.width
    height = image_size.height
    
    #Döngülerin başlangıç değerleri
    i=0
    k=0
    l=0
    s=1
    key=' '
    lp=0
    kp=0
    #Boş Matrisler --içine mesafe değerleri yazdırılacak--
    mesafeler = np.zeros((576,3))
    mesafeler_ = np.zeros((18,32))

    #Vid objesi tanımlanıyor ve bu kod zed kameranın kendi kodudur.
    vid = zed.enable_recording(path8+"surus_kayit_1"+ ".svo", sl.SVO_COMPRESSION_MODE.SVO_COMPRESSION_MODE_AVCHD)

    #Zed den görüntü matrisi alınıyor. --formatlı olarak--
    image_zed = sl.Mat(width, height, sl.MAT_TYPE.MAT_TYPE_8U_C4)
    depth_image_zed = sl.Mat(width, height, sl.MAT_TYPE.MAT_TYPE_8U_C4)
    point_cloud = sl.Mat()
 
    #Döngümüz başlıyor 
    while key != 113 :
         
        err = zed.grab(runtime) #Hata mesajı ile birlikte kameradan runtime yakalanıyor

        if (err == sl.ERROR_CODE.SUCCESS) : #hata yoksa

            zed.retrieve_image(image_zed, sl.VIEW.VIEW_LEFT) #Sol kameradan görüntü alındı
            zed.retrieve_image(depth_image_zed, sl.VIEW.VIEW_DEPTH) #Derinlik bilgisi alındı
            zed.retrieve_measure(point_cloud, sl.MEASURE.MEASURE_XYZRGBA,sl.MEM.MEM_CPU) 
            
            #Nan denetimi için döngüde kullanılan değerler
            p=0
            k=3
            
            #Zed kameranın görüntüleri numpy e dönüştürüldü.
            image_ocv = image_zed.get_data()
            depth_image_ocv = depth_image_zed.get_data()
            
            #Belitrilen piksellerdeki uzaklıklar hesaplanıyor
            for l in range(0,1280,40):
                
                for k in range(0,720,40):
                    
                    err, point_cloud_value = point_cloud.get_value(l, k)
                    mesafeler[p,2] = math.sqrt(point_cloud_value[0] * point_cloud_value[0] +
                                 point_cloud_value[1] * point_cloud_value[1] +
                                 point_cloud_value[2] * point_cloud_value[2]) 

                    if (math.isnan(mesafeler[p,2])==True): #Nan denetimi --şimdilik çalışmıyor--
                        mesafeler[p,2]=0

                    mesafeler_[kp,lp]=mesafeler[p,2]
                    mesafeler[p,0]=k
                    mesafeler[p,1]=l
                      
                    #Görüntü üzerine gridler çizdiriliyor
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.rectangle(depth_image_ocv , (l,k) , (l+2,k+2) , (0,255,0) ,1)
                    cv2.rectangle(image_ocv , (l,k) , (l+2,k+2) , (0,255,0) ,1)
                    cv2.putText(depth_image_ocv,str(round(mesafeler[p,2])), (l,k), font, 0.3, (255,255,0),1,cv2.LINE_AA)
                    p=p+1
                    kp=kp+1
                kp=0
                lp=lp+1
            lp=0
            np.savetxt(path1+'matris_2x576_'+str(sayici)+'.txt',mesafeler, delimiter=',',fmt='%.4s',newline='\n')
            np.savetxt(path2+'matris_18x32_'+str(sayici)+'.txt',mesafeler_, delimiter=',',fmt='%.4s',newline='\n')
            
            cv2.imwrite(path3+"resim"+str(sayici)+".jpg",image_ocv)
            cv2.imwrite(path4+'resim_depth'+str(sayici)+'.jpg',depth_image_ocv)
            cv2.imshow("Image", image_ocv)
            cv2.imshow("Depth", depth_image_ocv)

            #Derinlik ve sol görüntü kaydediliyor --with help of opencv--
            left.write(image_ocv)
            depth.write(depth_image_ocv)
            zed.record()#Zed gömülü görüntü kayıt kodu   
            #q harfi çıkış denetimi
            key = cv2.waitKey(10)
            sayici=sayici+1
    #Bağımlılıkları serbest bırak  
    cv2.destroyAllWindows()
    zed.close()
    left.release()
    depth.release()

    print("\nFINISH")

#Main ana forksiyonu başlatılıyor
if __name__ == "__main__":
	main()# Alt main forksiyonuna git -- en üstteki--
