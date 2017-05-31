function [  ] = SaveRegions( Image, Regions, Size, Location, startIdx)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
    for i=1:Regions.Count
        x1 = min(Regions.PixelList{i, 1}(:,1));
        x2 = max(Regions.PixelList{i, 1}(:,1));
        y1 = min(Regions.PixelList{i, 1}(:,2));
        y2 = max(Regions.PixelList{i, 1}(:,2));
        clear img;

        if y1 >= 3
            y1 = y1-2;
        end

        if y2 <= (size(Image,1)-2)
            y2 = y2+2;
        end

        if x1 >= 3
            x1 = x1-2;
        end

        if x2 <= (size(Image,2)-2)
            x2 = x2+2;
        end

        img = Image(y1:y2,x1:x2);
        img = imresize(img,Size);
        imwrite(img,  sprintf ( '%s%i.jpg', Location, startIdx+i));
    end

end

