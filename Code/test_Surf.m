clc;clear;close all;
%=================================================================
%In this section;;
% 1. This program is prepared for tests
% 2. Number of features and time consumptions are calculated
%=================================================================

filename='..\Loc1_RGB.avi';
% filename='..\Loc1_DepthMap.avi';
% filename='..\Loc2_RGB.avi';
% filename='..\Loc2_DepthMap.avi';
% filename='..\Loc3_RGB.avi';
% filename='..\Loc3_DepthMap.avi';

mov=VideoReader(filename);

aralik=2;

b1=4;b2=4;%blok boyutlarý
fun = @(block_struct) median((block_struct.data),'all');
rEski=read(mov,9240);
rEski=rEski(:,1:1282,:);

rBloklanmisEski=rEski;
rBloklanmisEski=rgb2gray(rBloklanmisEski);


r=read(mov,9260);

r=r(:,1:1282,:);


rBloklanmisYeni=r;
rBloklanmisYeni=rgb2gray(rBloklanmisYeni);


tic
ptsEski  = detectSURFFeatures(rBloklanmisEski);
[featuresEski,validPtsEski] = extractFeatures(rBloklanmisEski,ptsEski);
toc

tic
ptsYeni = detectSURFFeatures(rBloklanmisYeni);
[featuresYeni,validPtsYeni] = extractFeatures(rBloklanmisYeni,ptsYeni);
toc

index_pairs = matchFeatures(featuresEski,featuresYeni);
matchedPtsEski  = validPtsEski(index_pairs(:,1));
matchedPtsYeni = validPtsYeni(index_pairs(:,2));

figure; 
showMatchedFeatures(rBloklanmisEski,rBloklanmisYeni,matchedPtsEski,matchedPtsYeni, 'montage');
title('Matched SURF points,including outliers');

[tform,inlierYeni,inlierEski] = estimateGeometricTransform(matchedPtsYeni,matchedPtsEski,'affine');
figure; 

showMatchedFeatures(rBloklanmisEski,rBloklanmisYeni,inlierEski,inlierYeni, 'montage');
title('Matched inlier points');

%% %===============================================================================

 
for k=1:size(inlierYeni,1)
       eslesmeAmp_Aci(k,1)=norm(inlierYeni(k,:)-inlierEski(k,:));
       eslesmeAmp_Aci(k,2)=atand((inlierYeni(k,2)-inlierEski(k,2))./(inlierYeni(k,1)-inlierEski(k,1)));
end

%%
 
 siyahBolge=8; %alt alta iki resim arasý siyah bölge
 matchedPtsYeni=matchedPtsYeni.Location;
 matchedPtsEski=matchedPtsEski.Location;
     figure;
     ra=[rBloklanmisYeni;zeros(siyahBolge,size(rBloklanmisYeni,2));  rBloklanmisEski];
     imshow(ra)
     hold on
     eklenecek_ra=size(rBloklanmisYeni,1)+siyahBolge;
     scatter(matchedPtsYeni(:,1),matchedPtsYeni(:,2),'r+')
     scatter(matchedPtsEski(:,1),matchedPtsEski(:,2)+eklenecek_ra,'b*')
     xa=[matchedPtsYeni(:,1) matchedPtsEski(:,1)];
     ya=[matchedPtsYeni(:,2) matchedPtsEski(:,2)+eklenecek_ra];    
     plot(xa',ya','y');    
     set(gcf,'Position',[100 -10 1200 800]);%figür penceresinin yeri ayarlandý.
