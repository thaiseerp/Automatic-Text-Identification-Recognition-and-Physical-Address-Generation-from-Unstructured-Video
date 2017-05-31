function [ output ] = IsOverlapping( Loc1, Loc2, thres )
%UNTITLED3 Summary of this function goes here
%   Detailed explanation goes here
    
    val = abs(Loc1-Loc2);
    
    output = (val(1,1)<=thres && val(1,2)<=thres);
end

