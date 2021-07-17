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

b1=4;b2=4;
fun = @(block_struct) median((block_struct.data),'all');
rEski=read(mov,9240);%Tests are performed by constantly changing frame numbers.

rEski=rEski(:,1:1282,:);

rBloklanmis1 = blockproc(rEski(:,:,1),[b1 b2],fun);
rBloklanmis2 = blockproc(rEski(:,:,2),[b1 b2],fun);
rBloklanmis3 = blockproc(rEski(:,:,3),[b1 b2],fun);

tic
oznitelikMatrisi1=Fun_BlokGoruntuOzntlkCikart2(double(rBloklanmis1),aralik);
oznitelikMatrisi2=Fun_BlokGoruntuOzntlkCikart2(double(rBloklanmis2),aralik);
oznitelikMatrisi3=Fun_BlokGoruntuOzntlkCikart2(double(rBloklanmis3),aralik);
oznitelikMatrisiEski=[oznitelikMatrisi1 oznitelikMatrisi2 oznitelikMatrisi3];
toc
oznitelikMatrisiEski(:,53:54)=[];
oznitelikMatrisiEski(:,35:36)=[];
rBloklanmisEski=cat(3,uint8(rBloklanmis1),uint8(rBloklanmis2),uint8(rBloklanmis3));


r=read(mov,9260);%Tests are performed by constantly changing frame numbers.

r=r(:,1:1282,:);



rBloklanmis1 = blockproc(r(:,:,1),[b1 b2],fun);
rBloklanmis2 = blockproc(r(:,:,2),[b1 b2],fun);
rBloklanmis3 = blockproc(r(:,:,3),[b1 b2],fun);

tic
oznitelikMatrisi1=Fun_BlokGoruntuOzntlkCikart2(double(rBloklanmis1),aralik);
oznitelikMatrisi2=Fun_BlokGoruntuOzntlkCikart2(double(rBloklanmis2),aralik);
oznitelikMatrisi3=Fun_BlokGoruntuOzntlkCikart2(double(rBloklanmis3),aralik);
oznitelikMatrisiYeni=[oznitelikMatrisi1 oznitelikMatrisi2 oznitelikMatrisi3];
toc
oznitelikMatrisiYeni(:,53:54)=[];
oznitelikMatrisiYeni(:,35:36)=[];
rBloklanmisYeni=cat(3,uint8(rBloklanmis1),uint8(rBloklanmis2),uint8(rBloklanmis3));

%% %===============================================================================

tic
indexPairs=matchFeatures(oznitelikMatrisiYeni,oznitelikMatrisiEski,'MatchThreshold',10,'MaxRatio',0.92,'Unique',true);
toc

matchedPoints1=oznitelikMatrisiYeni((indexPairs(:,1)),17:18);
matchedPoints2=oznitelikMatrisiEski((indexPairs(:,2)),17:18);

matchedPoints1=flip(matchedPoints1,2);
matchedPoints2=flip(matchedPoints2,2);

showMatchedFeatures(rBloklanmisYeni, rBloklanmisEski, matchedPoints1, matchedPoints2, 'montage');
[tform, inlierYeni, inlierEski] = estimateGeometricTransform(matchedPoints1, matchedPoints2, 'affine');
figure;
showMatchedFeatures(rBloklanmisYeni, rBloklanmisEski, inlierYeni, inlierEski, 'montage');

%%
for k=1:size(inlierYeni,1)
       eslesmeAmp_Aci(k,1)=norm(inlierYeni(k,:)-inlierEski(k,:));
       eslesmeAmp_Aci(k,2)=atand((inlierYeni(k,2)-inlierEski(k,2))./(inlierYeni(k,1)-inlierEski(k,1)));
end

%%
 
 siyahBolge=8; 
     figure;
     ra=[rBloklanmisYeni;zeros(siyahBolge,size(rBloklanmisYeni,2),3);  rBloklanmisEski];
     imshow(ra)
     hold on
     eklenecek_ra=size(rBloklanmisYeni,1)+siyahBolge;
     scatter(inlierYeni(:,1),inlierYeni(:,2),'r+')
     scatter(inlierEski(:,1),inlierEski(:,2)+eklenecek_ra,'b*')
     xa=[inlierYeni(:,1) inlierEski(:,1)];
     ya=[inlierYeni(:,2) inlierEski(:,2)+eklenecek_ra];    
     plot(xa',ya','y');    
     set(gcf,'Position',[100 -10 1200 800]);%figür penceresinin yeri ayarlandý.