for k = 401:410
    filename = strcat('D:\Academics\Project\Files\training\new\',AllFiles(k).name);
    [img, map] = imread(filename);
    if ~isempty(map), img = ind2rgb(img, map); end
    imwrite(img, sprintf ( '%s%i.jpg', 'D:\\Academics\\Project\\Files\\training\\new\\jpg\\', k));
end
