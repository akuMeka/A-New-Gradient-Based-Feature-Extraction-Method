clc;clear;close all;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%In this section, images are divided into mxn size blocks. 
%The MD, AM, GM and LC of each blocks are calculated.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
filename='..\Loc1_RGB.avi';
% filename='..\Loc1_DepthMap.avi';
% filename='..\Loc2_RGB.avi';
% filename='..\Loc2_DepthMap.avi';
% filename='..\Loc3_RGB.avi';
% filename='..\Loc3_DepthMap.avi';


mov=VideoReader(filename);

b1=2;b2=2;%block sizes
artis=16;%frame interval
sayi=1;
i=1;

for sayi=sayi:artis:mov.NumberOfFrames
%MEDIAN
%blocking image in b1xb2 sizes and calculating median of each block
fun = @(block_struct) median((block_struct.data),'all');
r=read(mov,sayi);
r=r(:,1:1280,:);
rGri=rgb2gray(r); 
    %R channel
    rBloklanmis1 = blockproc(r(:,:,1),[b1 b2],fun);    
    %G channel
    rBloklanmis2 = blockproc(r(:,:,2),[b1 b2],fun);   
    %B channel
    rBloklanmis3 = blockproc(r(:,:,3),[b1 b2],fun); 
    
    %all channels are concatenating 
    rBloklanmisMed=cat(3,uint8(rBloklanmis1),uint8(rBloklanmis2),uint8(rBloklanmis3));
    rBloklanmisMedG=rgb2gray(rBloklanmisMed);     
 
 %ARITHMETIC MEAN
%blocking image in b1xb2 sizes and calculating arithmetic mean of each block
fun = @(block_struct) mean2((block_struct.data));
r=read(mov,sayi);
r=r(:,1:1280,:);

    %R channel
    rBloklanmis1 = blockproc(r(:,:,1),[b1 b2],fun);    
    %G channel
    rBloklanmis2 = blockproc(r(:,:,2),[b1 b2],fun);   
    %B channel
    rBloklanmis3 = blockproc(r(:,:,3),[b1 b2],fun);   
    %all channels are concatenating 
    rBloklanmisAM=cat(3,uint8(rBloklanmis1),uint8(rBloklanmis2),uint8(rBloklanmis3));
    rBloklanmisAMG=rgb2gray(rBloklanmisAM);

    
%GEOMETRIC MEAN
%blocking image in b1xb2 sizes and calculating geometric mean of each block
fun = @(block_struct) geomean(double(block_struct.data),'all');
r=read(mov,sayi);
r=r(:,1:1280,:);

    %R channel
    rBloklanmis1 = blockproc(r(:,:,1),[b1 b2],fun);    
    %G channel
    rBloklanmis2 = blockproc(r(:,:,2),[b1 b2],fun);   
    %B channel
    rBloklanmis3 = blockproc(r(:,:,3),[b1 b2],fun);   
    %all channels are concatenating
    rBloklanmisGM=cat(3,uint8(rBloklanmis1),uint8(rBloklanmis2),uint8(rBloklanmis3));
    rBloklanmisGMG=rgb2gray(rBloklanmisGM);
    
%LOCAL CONTRAST
%blocking image in b1xb2 sizes and calculating local contrast of each block
fun = @(block_struct) max(block_struct.data,[],'all')-min(block_struct.data,[],'all');
r=read(mov,sayi);
r=r(:,1:1280,:);

    %R channel
    rBloklanmis1 = blockproc(r(:,:,1),[b1 b2],fun);    
    %G channel 
    rBloklanmis2 = blockproc(r(:,:,2),[b1 b2],fun);   
    %B channel
    rBloklanmis3 = blockproc(r(:,:,3),[b1 b2],fun); 
    
    %all channels are concatenating
    rBloklanmisLC=cat(3,uint8(rBloklanmis1),uint8(rBloklanmis2),uint8(rBloklanmis3));
    rBloklanmisLCG=rgb2gray(rBloklanmisLC);
 
%% Original Image
r=read(mov,sayi);
r=r(:,1:1280,:);
%%
%Calculating histogram
rHist_V=normalizasyon2(histcounts(rGri,30));
rMedGHist_V=normalizasyon2(histcounts(rBloklanmisMedG,30));
rAmgHist_V=normalizasyon2(histcounts(rBloklanmisAMG,30));
rGmgHist_V=normalizasyon2(histcounts(rBloklanmisGMG,30));
rLcgHist_V=normalizasyon2(histcounts(rBloklanmisLCG,30));
rRszHist_V=normalizasyon2(histcounts(rBloklanmisRSZ,30));

FarkMed=rHist_V-rMedGHist_V;FarkMed=sum(abs(FarkMed));
FarkAMG=rHist_V-rAmgHist_V;FarkAMG=sum(abs(FarkAMG));
FarkGMG=rHist_V-rGmgHist_V;FarkGMG=sum(abs(FarkGMG));
FarkLCG=rHist_V-rLcgHist_V;FarkLCG=sum(abs(FarkLCG));
FarkRSZ=rHist_V-rRszHist_V;FarkRSZ=sum(abs(FarkRSZ));

FARK(i,:)=[FarkMed FarkAMG FarkGMG FarkLCG FarkRSZ];
i=i+1;
end
 

 
    