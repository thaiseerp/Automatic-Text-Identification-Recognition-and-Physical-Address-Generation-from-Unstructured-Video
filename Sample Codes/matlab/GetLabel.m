function [ Labels ] = GetLabel( Image, Regions, Size, convnet)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
    %regions = zeros(Regions.Count,59);
    Labels = zeros(Regions.Count,1);
    for i=1:Regions.Count
        x1 = min(Regions.PixelList{i, 1}(:,1));
        x2 = max(Regions.PixelList{i, 1}(:,1));
        y1 = min(Regions.PixelList{i, 1}(:,2));
        y2 = max(Regions.PixelList{i, 1}(:,2));
        clear img;

        if y1 >= 4
            y1 = y1-3;
        end

        if y2 <= (size(Image,1)-3)
            y2 = y2+3;
        end

        if x1 >= 4
            x1 = x1-3;
        end

        if x2 <= (size(Image,2)-3)
            x2 = x2+3;
        end

        img = Image(y1:y2,x1:x2);
        img = imresize(img,Size);
        
        Labels(i,1) = classify(convnet,img);
        %figure;imshow(img);
    end
end