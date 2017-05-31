
image = imread('D:\Academics\Project\Files\frames\frames\6.jpg');
image = rgb2gray(image);
if ((size(image,1) >=1000) && (size(image,1) <2000))
    image = imresize(image, 0.5);
elseif ((size(image,1) >=2000) && (size(image,1) <3000))
    image = imresize(image, 0.35);
elseif ((size(image,1) >=3000))
    image = imresize(image, 0.25);
end
[regions, ~] = detectMSERFeatures(image, 'RegionAreaRange',[20 5000] );
figure; imshow(image); hold on;
plot(regions, 'showEllipses', true);
title('Detected MSER Regions');
%%
RegionsToRemove = RemoveOverlappingReg(regions, 4);
regions(RegionsToRemove==1) = [];


figure; imshow(image); hold on;
plot(regions, 'showEllipses', true);
title('After removing overlapping regions and regions based on aspect ratio');

regionscl = regions;
%%
Size = [24,24];
load('convnet');
Label = GetLabel(image,regions,Size,convnet);

regions(Label ~= 2) = [];

figure; imshow(image); hold on;
plot(regions, 'showEllipses', true);
title('Regions after classification');

%%
for n = 1:4
    RegionsToRemove2 = RemoveNonText(regions);
    regions(RegionsToRemove2==1) = [];
end
%
figure; imshow(image); hold on;
plot(regions, 'showEllipses', true);
title('FinalText Regions');

