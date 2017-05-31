load('TrainPositiveImgFeat.mat');
load('TrainNegativeImgFeat.mat');
TrainingSet = zeros( ...
    (size(TrainPositiveImgFeat,1)+size(TrainNegativeImgFeat,1)) , 60);

%%

TrainingSet(1:size(TrainPositiveImgFeat,1),1:576) = TrainPositiveImgFeat;
TrainingSet(size(TrainPositiveImgFeat,1)+1:end,1:576) = TrainNegativeImgFeat;
TrainingSet(1:size(TrainPositiveImgFeat,1),577) = 1;
TrainingSet(size(TrainPositiveImgFeat,1)+1:end,577) = 0;

clear TrainPositiveImgFeat;
clear TrainNegativeImgFeat;
%save('TrainingSet','TrainingSet');
%%
tic;
AdaboostModelImgRand = fitcensemble(TrainingSet(:,1:576),TrainingSet(:,577));
toc;



