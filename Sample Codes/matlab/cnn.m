 load('imds.mat');
 
 layers = [imageInputLayer([24 24 1])
	 convolution2dLayer(5,20)
	 reluLayer()
	 maxPooling2dLayer(2,'Stride',2)
	 fullyConnectedLayer(2)
	 softmaxLayer()
	 classificationLayer()];
 
 options = trainingOptions('sgdm','InitialLearnRate',0.00001);

convnet = trainNetwork(imds,layers,options);