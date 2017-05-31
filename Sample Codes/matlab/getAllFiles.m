function [ fileList ] = getAllFiles(dirName, fileExtension, appendFullPath)
%UNTITLED4 Summary of this function goes here
%   Detailed explanation goes here

    dirData = dir([dirName '/' fileExtension]); 
    dirWithSubFolders = dir(dirName);
    dirIndex = [dirWithSubFolders.isdir];
    fileList = {dirData.name}';
    
    if ~isempty(fileList)
        if appendFullPath
          fileList = cellfun(@(x) fullfile(dirName,x),...  
                           fileList,'UniformOutput',false);
        end
    end
    subDirs = {dirWithSubFolders(dirIndex).name};  
    validIndex = ~ismember(subDirs,{'.','..'}); 

    for iDir = find(validIndex)                  
        nextDir = fullfile(dirName,subDirs{iDir});    
        fileList = [fileList; getAllFiles(nextDir, ...
            fileExtension, appendFullPath)]; 
    end
end