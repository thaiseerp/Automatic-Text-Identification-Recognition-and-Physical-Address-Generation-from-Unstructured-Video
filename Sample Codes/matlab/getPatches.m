frames = getAllFiles('D:\Academics\Project\Files\frames\frames\', '*.jpg', 1);
for i = 1:size(frames,1)
    
    image = imread(frames{i});
    patchSize = [400,400];
    overlap = 100;

    continueprogram = true;
    r1 = 1;
    c1 = 1;
    count = 1;
    while continueprogram
        r2 = r1 + patchSize(1) - 1;
        onrows = true;

        while onrows
            c2 = c1 + patchSize(2) - 1;
            if r2 > size(image,1)
                r1 = size(image,1) - patchSize(1) + 1;
                r2 = size(image,1);
            end
            if c2 > size(image,2)
                c1 = size(image,2) - patchSize(2) + 1;
                c2 = size(image,2);
            end
            patch = image(r1:r2,c1:c2,:);
            mkdir(sprintf('D:\\Academics\\Project\\Files\\patches\\frame%i', i));
            imwrite(patch,  sprintf ( 'D:\\Academics\\Project\\Files\\patches\\frame%i\\%i.jpg', i, count));
            count = count + 1;
            c1 = c1 + patchSize(2) - overlap;
            if c2>=size(image,2)
                onrows = false;
            end
        end

        r1 = r1 + patchSize(1) - overlap;
        c1 = 1;
        if r2>=size(image,1) && c2 >= size(image,2)
            continueprogram = false;
        end
    end
end