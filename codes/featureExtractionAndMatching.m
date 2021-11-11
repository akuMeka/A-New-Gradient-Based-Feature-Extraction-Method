clc;clear;close all;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%In this section, 
%1-The features of each block are extracted.
%2-Features of image pairs are matched
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

filename='..\Loc1_RGB.avi';
% filename='..\Loc1_DepthMap.avi';
% filename='..\Loc2_RGB.avi';
% filename='..\Loc2_DepthMap.avi';
% filename='..\Loc3_RGB.avi';
% filename='..\Loc3_DepthMap.avi';


fun = @(block_struct) geomean(block_struct.data);
mov=VideoReader(filename);

artis=12;

cikarmaSayaci=1;

b1=4;b2=4;%block sizes


rEski=zeros(mov.Height,mov.Width);
rEski=uint8(rEski);

%çerçeveler okunmaya baþlýyor.
for sayi=1:artis:mov.NumberOfFrames
    r=read(mov,sayi);
   
    rBloklanmis1 = blockproc(r(:,:,1),[b1 b2],fun);
    
    oznitelikMatrisi1=Fun_BlokGoruntuOzntlkCikart2(rBloklanmis1);

    rBloklanmis2 = blockproc(r(:,:,2),[b1 b2],fun);
    oznitelikMatrisi2=Fun_BlokGoruntuOzntlkCikart2(rBloklanmis2);

    rBloklanmis3 = blockproc(r(:,:,3),[b1 b2],fun);
    oznitelikMatrisi3=Fun_BlokGoruntuOzntlkCikart2(rBloklanmis3);
   
    oznitelikMatrisi=[oznitelikMatrisi1 oznitelikMatrisi2 oznitelikMatrisi3];
    
    rBloklanmis=cat(3,uint8(rBloklanmis1),uint8(rBloklanmis2),uint8(rBloklanmis3));

    %oznitelikMatrisi=FeatureMatrix
    if cikarmaSayaci==1
      oznitelikMatrisiEski=oznitelikMatrisi; 
      rBloklanmisEski=rBloklanmis;
    else
        
    
     indexPairs=matchFeatures(oznitelikMatrisi,oznitelikMatrisiEski,'MatchThreshold',20,'MaxRatio',0.42,'Unique',true);
  
     matchedPoints1=oznitelikMatrisi((indexPairs(:,1)),17:18);
     matchedPoints2=oznitelikMatrisiEski((indexPairs(:,2)),17:18);
     
     for k=1:size(matchedPoints1,1)
       eslesmeAmp_Aci(k,1)=norm(matchedPoints1(k,:)-matchedPoints2(k,:));
       eslesmeAmp_Aci(k,2)=atand((matchedPoints1(k,1)-matchedPoints2(k,1)./((matchedPoints1(k,2)-matchedPoints2(k,2)))));
     end
     mostFrequentAmp_Aci=mode(eslesmeAmp_Aci,1)
     
     for k=1:size(matchedPoints1,1)
       eslesmeler(k,1)=matchedPoints2(k,1)-matchedPoints1(k,1);
       eslesmeler(k,2)=matchedPoints2(k,2)-matchedPoints1(k,2);
     end
     
     mostFrequent=mode(eslesmeler,1)

   
     figure;
     rr=[rBloklanmis,zeros(size(rBloklanmis,1),8,3),  rBloklanmisEski];
     imshow(rr)
     hold on
     eklenecek_rr=size(rBloklanmis,2)+8;
     scatter(matchedPoints1(:,2),matchedPoints1(:,1),'r+')
     scatter(matchedPoints2(:,2)+eklenecek_rr,matchedPoints2(:,1),'b*')
     x=[matchedPoints1(:,2) matchedPoints2(:,2)+eklenecek_rr];
     y=[matchedPoints1(:,1) matchedPoints2(:,1)];    
     plot(x',y');    
     set(gcf,'Position',[100 -10 1200 800]);%figure window
     
     
     figure;
     ra=[rBloklanmis;zeros(4,size(rBloklanmis,2),3);  rBloklanmisEski];
     imshow(ra)
     hold on
     eklenecek_ra=size(rBloklanmis,1)+8;
     scatter(matchedPoints1(:,2),matchedPoints1(:,1),'r+')
     scatter(matchedPoints2(:,2),matchedPoints2(:,1)+eklenecek_ra,'b*')
     xa=[matchedPoints1(:,2) matchedPoints2(:,2)];
     ya=[matchedPoints1(:,1) matchedPoints2(:,1)+eklenecek_ra];    
     plot(xa',ya');    
     set(gcf,'Position',[100 -10 1200 800]);
     
    
     hizaliResim=Fun_resimHizala(mostFrequent(1), mostFrequent(2), rBloklanmis);     
     fark=rBloklanmisEski-uint8(hizaliResim);
     fark=im2bw(fark);
     
     fark(end-abs(mostFrequent(1)):end,:)=0;
     fark(:,end-abs(mostFrequent(2)):end)=0
     fark=bwareaopen(fark,10);
     figure, imshow(fark) 
     
     figure
     imshow([rBloklanmisEski;hizaliResim;rBloklanmis])
     
     
    
     [solUstSatir,solUstSutun, en, boy ] = Fun_nesneKareIcineAl(fark,b1,b2,size(r,1), size(r,2))
     figure
     imshow(r);
     hold on
     rectangle('Position', [solUstSutun+b2, solUstSatir+b1, en+b2, boy+b1],'EdgeColor','r','LineWidth',2 );     
     hold off    
          
     oznitelikMatrisiEski=oznitelikMatrisi;   
    end
     cikarmaSayaci=cikarmaSayaci+1; 
     
     
end

