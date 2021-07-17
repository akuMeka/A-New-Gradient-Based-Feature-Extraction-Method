function hizaliResim = Fun_resimHizala(satir,sutun,goruntu)
%With this function, two consecutive frames in a video will be aligned to 
%each other.
 rBloklanmis=goruntu;
 hizaliResim=zeros(size(rBloklanmis));%zeros matris oluþturuldu.
 if satir>=0 && sutun <=0
     
     for i=1:size(rBloklanmis,1)-abs(satir)
         for j=1:size(rBloklanmis,2)-abs(sutun)             
             hizaliResim(i+abs(satir),j,:)=rBloklanmis(i,j+abs(sutun),:);             
         end
     end
 elseif satir>=0 && sutun>=0
     
     for i=1:size(rBloklanmis,1)-abs(satir)
         for j=1:size(rBloklanmis,2)-abs(sutun)             
             hizaliResim(i+abs(satir),j+abs(sutun),:)=rBloklanmis(i,j,:);             
         end
     end
 elseif satir<=0 && sutun>=0
     
     for i=1:size(rBloklanmis,1)-abs(satir)
         for j=1:size(rBloklanmis,2)-abs(sutun)             
             hizaliResim(i,j+abs(sutun),:)=rBloklanmis(i+abs(satir),j,:);             
         end
     end
 elseif satir<=0 && sutun<=0
     
     for i=1:size(rBloklanmis,1)-abs(satir)
         for j=1:size(rBloklanmis,2)-abs(sutun)             
             hizaliResim(i,j,:)=rBloklanmis(i+abs(satir),j+abs(sutun),:);             
         end
     end
 end     
     
end

