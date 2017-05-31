parfor k = 1:410
    % Exclude bad images
%     exclude = [101, 105, 107, 108, 109, 111, 114, 115, 119, 125, 126, 127, 128, ...
%         129, 133, 134, 136, 138, 140, 148, 149, 150, 153, 169, 173, 174, 182, ...
%         183, 186, 189, 192, 205, 211, 216, 217, 218, 221, 224, 225, 226, 227, ...
%         232, 239, 240, 242, 256, 257, 259, 260, 261, 266, 267,271, 280, 284, ...
%         294, 303, 315, 316, 324, 328];
%     if any(exclude==k)
%         continue;
%     end

% Define all files using dir command
    filename = strcat('D:\Academics\Project\Files\training\new\',AllFiles(k).name);
    try
        image = imread(filename);
    catch
        continue;
    end
    
    try
        image = rgb2gray(image);
    catch
        continue;
    end
    
%     if ((size(image,1) >=1000) && (size(image,1) <2000))
%         image = imresize(image, 0.5);
%     elseif ((size(image,1) >=2000) && (size(image,1) <3000))
%         image = imresize(image, 0.35);
%     elseif ((size(image,1) >=3000))
%         image = imresize(image, 0.25);
%     end
    sprintf('Doing MSER on image %i', k)
    [regions, ~] = detectMSERFeatures(image, 'RegionAreaRange',[50 20000]);
    % figure; imshow(image); hold on;
    % plot(regions, 'showEllipses', true);

    RegionsToRemove = RemoveOverlappingReg(regions, 5);
    regions(RegionsToRemove==1) = [];

    % image = imread('D:\Academics\Project\Files\training\115.jpg');
    % image = rgb2gray(image);
    % figure; imshow(image); hold on;
    % plot(regions, 'showEllipses', true);

    Size = [24,24];
    D = dir(['D:\\Academics\\Project\\Files\\training\\train\\new\\', '\*.jpg']);
    startIdx = length(D(not([D.isdir])));
    SaveRegions(image,regions,Size, 'D:\\Academics\\Project\\Files\\training\\train\\new\\', startIdx);
    
end