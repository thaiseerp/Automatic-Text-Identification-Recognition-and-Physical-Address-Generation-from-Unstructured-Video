fileList = getAllFiles( ...
    'D:\Academics\Project\Files\training\train\ICDAR2003\char\', ...
    '*.jpg', 1);

for i = 1: size(fileList,1)
    filename = fileList{i};
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
    
    image = imresize(image,[24,24]);
    imwrite(image,  sprintf ( 'D:\\Academics\\Project\\Files\\training\\train\\ICDAR2003\\positive\\%i.jpg', i));
    if mod(i,1000) == 0
        disp(i)
    end
end