function [ RegionsToRemove ] = RemoveNonText(Regions)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
    RegionsToRemove = zeros(Regions.Count,1);

    for i = 1:Regions.Count
        count = 0;
        for j = 1:Regions.Count
            dist = norm(Regions.Location(i,:)-Regions.Location(j,:));
            if(dist<80)
                count = count+1;
            end
            if(count>3)
                RegionsToRemove(i) = 0;
                break;
            else
                RegionsToRemove(i) = 1;
            end
            
        end
    end
end
