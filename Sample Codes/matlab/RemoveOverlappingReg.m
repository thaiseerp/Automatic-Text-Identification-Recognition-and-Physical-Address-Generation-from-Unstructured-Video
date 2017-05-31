function [ RegionsToRemove ] = RemoveOverlappingReg( Regions, thres)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
    RegionsToRemove = zeros(Regions.Count,1);

    for i = Regions.Count:-1:1
        regionLocation1 = Regions.Location(i,:);
        for j = i-1:-1:1
            regionLocation2 = Regions.Location(j,:);
            if(IsOverlapping(regionLocation1,regionLocation2,thres))
                if(size(Regions.PixelList{i,1},1)<size(Regions.PixelList{j,1},1))
                    RegionsToRemove(i) = 1;
                else
                    RegionsToRemove(j) = 1;
                end     
            end
        end
        
        % Remove regions based on aspect ratio
        
        x1 = min(Regions.PixelList{i, 1}(:,1));
        x2 = max(Regions.PixelList{i, 1}(:,1));
        y1 = min(Regions.PixelList{i, 1}(:,2));
        y2 = max(Regions.PixelList{i, 1}(:,2));
        
        h = y2-y1;
        w = x2-x1;
        
        AspRatio = double(w)/double(h);

        if(AspRatio>1.6 || AspRatio<0.15)
            RegionsToRemove(i) = 1;
        end
    end
end
