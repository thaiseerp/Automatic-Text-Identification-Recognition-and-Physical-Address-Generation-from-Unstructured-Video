@mfunction("Regions")
def detectMSERFeatures(I=None, *varargin):
    #detectMSERFeatures Finds MSER features.
    #   regions = detectMSERFeatures(I) returns an MSERRegions object, regions,
    #   containing region pixel lists and other information about MSER features
    #   detected in a 2-D grayscale image I. detectMSERFeatures uses Maximally
    #   Stable Extremal Regions (MSER) algorithm to find regions.
    #
    #   regions = detectMSERFeatures(I,Name,Value) specifies additional
    #   name-value pair arguments described below:
    #
    #   'ThresholdDelta'   Scalar value, 0 < ThresholdDelta <= 100, expressed
    #                      as a percentage of the input data type range. This
    #                      value specifies the step size between intensity
    #                      threshold levels used in selecting extremal regions
    #                      while testing for their stability. Decrease this
    #                      value to return more regions. Typical values range
    #                      from 0.8 to 4.
    #
    #                      Default: 2
    #
    #   'RegionAreaRange'  Two-element vector, [minArea maxArea], which
    #                      specifies the size of the regions in pixels. This
    #                      value allows the selection of regions containing
    #                      pixels between minArea and maxArea, inclusive.
    #
    #                      Default: [30 14000]
    #
    #   'MaxAreaVariation' Positive scalar. Increase this value to return a
    #                      greater number of regions at the cost of their
    #                      stability. Stable regions are very similar in
    #                      size over varying intensity thresholds. Typical
    #                      values range from 0.1 to 1.0.
    #
    #                      Default: 0.25
    #
    #   'ROI'              A vector of the format [X Y WIDTH HEIGHT],
    #                      specifying a rectangular region in which corners
    #                      will be detected. [X Y] is the upper left corner of
    #                      the region.
    #
    #                      Default: [1 1 size(I,2) size(I,1)]
    #
    #   Class Support
    #   -------------
    #   The input image I can be uint8, int16, uint16, single or double,
    #   and it must be real and nonsparse.
    #
    #   Example
    #   -------
    #   % Find MSER regions
    #   I = imread('cameraman.tif');
    #   regions = detectMSERFeatures(I);
    #
    #   % Visualize MSER regions which are described by pixel lists stored
    #   % inside the returned 'regions' object
    #   figure; imshow(I); hold on;
    #   plot(regions, 'showPixelList', true, 'showEllipses', false);
    #
    #   % Display ellipses and centroids fit into the regions
    #   figure; imshow(I); hold on;
    #   plot(regions); % by default, plot displays ellipses and centroids
    #
    #   See also MSERRegions, extractFeatures, matchFeatures,
    #            detectBRISKFeatures, detectFASTFeatures, detectHarrisFeatures,
    #            detectMinEigenFeatures, detectSURFFeatures, SURFPoints

    #   Copyright 2011 The MathWorks, Inc.

    #   References:
    #      Jiri Matas, Ondrej Chum, Martin Urban, Tomas Pajdla. "Robust
    #      wide-baseline stereo from maximally stable extremal regions",
    #      Proc. of British Machine Vision Conference, pages 384-396, 2002.
    #
    #      David Nister and Henrik Stewenius, "Linear Time Maximally Stable
    #      Extremal Regions", European Conference on Computer Vision,
    #      pages 183-196, 2008.

    ##codegen
    ##ok<*EMCA>

    [Iu8, params] = parseInputs(I, varargin(mslice[:]))

    if isSimMode():
        # regionsCell is pixelLists in a cell array {a x 2; b x 2; c x 2; ...} and
        # can only be handled in simulation mode since cell arrays are not supported
        # in code genereration
        regionsCell = ocvExtractMSER(Iu8, params)

        if params.usingROI and not isempty(params.ROI):
            regionsCell = offsetPixelList(regionsCell, params.ROI)
        end

        Regions = MSERRegions(regionsCell)

    else:
        [pixelList, lengths] = vision.internal.buildable.detectMserBuildable.detectMser_uint8(Iu8, params)

        if params.usingROI and not isempty(params.ROI):        # offset location values
            pixelList = offsetPixelListCodegen(pixelList, params.ROI)
        end

        Regions = MSERRegions(pixelList, lengths)

    end

    #==========================================================================
    # Parse and check inputs
    #==========================================================================
@mfunction("img, params")
def parseInputs(I=None, *varargin):

    validateattributes(I, mcellarray([mstring('logical'), mstring('uint8'), mstring('int16'), mstring('uint16'), mstring('single'), mstring('double')]), mcellarray([mstring('2d'), mstring('nonempty'), mstring('nonsparse'), mstring('real')]), mfilename, mstring('I'), 1)# Logical input is not supported

    Iu8 = im2uint8(I)

    imageSize = size(I)
    if isSimMode():
        params = parseInputs_sim(imageSize, varargin(mslice[:]))
    else:
        params = parseInputs_cg(imageSize, varargin(mslice[:]))
    end

    #--------------------------------------------------------------------------
    # Other OpenCV parameters which are not exposed in the main interface
    #--------------------------------------------------------------------------
    params.minDiversity = single(0.2)
    params.maxEvolution = int32(200)
    params.areaThreshold = 1
    params.minMargin = 0.003
    params.edgeBlurSize = int32(5)

    img = vision.internal.detector.cropImageIfRequested(Iu8, params.ROI, params.usingROI)

    #==========================================================================
@mfunction("params")
def parseInputs_sim(imageSize=None, *varargin):
    # Parse the PV pairs
    parser = inputParser

    defaults = getDefaultParameters(imageSize)

    parser.addParameter(mstring('ThresholdDelta'), defaults.ThresholdDelta)
    parser.addParameter(mstring('RegionAreaRange'), defaults.RegionAreaRange)
    parser.addParameter(mstring('MaxAreaVariation'), defaults.MaxAreaVariation)
    parser.addParameter(mstring('ROI'), defaults.ROI)

    # Parse input
    parser.parse(varargin(mslice[:]))

    checkThresholdDelta(parser.Results.ThresholdDelta)

    params.usingROI = not ismember(mstring('ROI'), parser.UsingDefaults)

    roi = parser.Results.ROI
    if params.usingROI:
        vision.internal.detector.checkROI(roi, imageSize)
    end

    isAreaRangeUserSpecified = not ismember(mstring('RegionAreaRange'), parser.UsingDefaults)

    if isAreaRangeUserSpecified:
        checkRegionAreaRange(parser.Results.RegionAreaRange, imageSize, params.usingROI, roi)
    end

    checkMaxAreaVariation(parser.Results.MaxAreaVariation)

    # Populate the parameters to pass into OpenCV's ocvExtractMSER()
    params.delta = parser.Results.ThresholdDelta * 255 / 100
    params.minArea = parser.Results.RegionAreaRange(1)
    params.maxArea = parser.Results.RegionAreaRange(2)
    params.maxVariation = parser.Results.MaxAreaVariation
    params.ROI = parser.Results.ROI

    #==========================================================================
@mfunction("params")
def parseInputs_cg(imageSize=None, *varargin):

    # Optional Name-Value pair: 3 pairs (see help section)
    defaults = getDefaultParameters(imageSize)
    defaultsNoVal = getDefaultParametersNoVal()
    properties = getEmlParserProperties()

    optarg = eml_parse_parameter_inputs(defaultsNoVal, properties, varargin(mslice[:]))
    parser_Results.ThresholdDelta = (eml_get_parameter_value(optarg.ThresholdDelta, defaults.ThresholdDelta, varargin(mslice[:])))
    parser_Results.RegionAreaRange = (eml_get_parameter_value(optarg.RegionAreaRange, defaults.RegionAreaRange, varargin(mslice[:])))
    parser_Results.MaxAreaVariation = (eml_get_parameter_value(optarg.MaxAreaVariation, defaults.MaxAreaVariation, varargin(mslice[:])))
    parser_ROI = eml_get_parameter_value(optarg.ROI, defaults.ROI, varargin(mslice[:]))

    checkThresholdDelta(parser_Results.ThresholdDelta)

    # check whether ROI parameter is specified
    usingROI = optarg.ROI != uint32(0)

    if usingROI:
        vision.internal.detector.checkROI(parser_ROI, imageSize)
    end

    # check whether area range parameter is specified
    isAreaRangeUserSpecified = optarg.RegionAreaRange != uint32(0)

    if isAreaRangeUserSpecified:
        checkRegionAreaRange(parser_Results.RegionAreaRange, imageSize, usingROI, parser_ROI)
    end

    checkMaxAreaVariation(parser_Results.MaxAreaVariation)

    params.delta = cCast(mstring('int32_T'), parser_Results.ThresholdDelta * 255 / 100)
    params.minArea = cCast(mstring('int32_T'), parser_Results.RegionAreaRange(1))
    params.maxArea = cCast(mstring('int32_T'), parser_Results.RegionAreaRange(2))
    params.maxVariation = cCast(mstring('real32_T'), parser_Results.MaxAreaVariation)
    params.ROI = parser_ROI
    params.usingROI = usingROI

    #==========================================================================
    # Offset pixel list locations based on ROI
    #==========================================================================
@mfunction("pixListOut")
def offsetPixelList(pixListIn=None, roi=None):
    n = size(pixListIn, 1)
    pixListOut = cell(n, 1)
    for i in mslice[1:n]:
        pixListOut(i).lvalue = vision.internal.detector.addOffsetForROI(pixListIn(i), roi, true)
    end

    #==========================================================================
    # Offset pixel list locations based on ROI
    #==========================================================================
@mfunction("pixListOut")
def offsetPixelListCodegen(pixListIn=None, roi=None):

    pixListOut = vision.internal.detector.addOffsetForROI(pixListIn, roi, true)

    #==========================================================================
@mfunction("defaults")
def getDefaultParameters(imgSize=None):

    defaults = struct(mstring('ThresholdDelta'), 5 * 100 / 255, mstring('RegionAreaRange'), mcat([30, 14000]), mstring('MaxAreaVariation'), 0.25, mstring('ROI'), mcat([1, 1, imgSize(2), imgSize(1)]))

    #==========================================================================


    defaultsNoVal = struct(mstring('ThresholdDelta'), uint32(0), mstring('RegionAreaRange'), uint32(0), mstring('MaxAreaVariation'), uint32(0), mstring('ROI'), uint32(0))

    #==========================================================================


    properties = struct(mstring('CaseSensitivity'), false, mstring('StructExpand'), true, mstring('PartialMatching'), false)

    #==========================================================================
@mfunction("tf")
def checkThresholdDelta(thresholdDelta=None):
    validateattributes(thresholdDelta, mcellarray([mstring('numeric')]), mcellarray([mstring('scalar'), mstring('nonsparse'), mstring('real'), mstring('positive'), mstring('<='), 100]), mfilename)
    tf = true

    #==========================================================================
@mfunction("")
def checkRegionAreaRange(regionAreaRange=None, imageSize=None, usingROI=None, roi=None):

    if usingROI:
        # When an ROI is specified, the region area range validation should
        # be done with respect to the ROI size.
        sz = int32(mcat([roi(4), roi(3)]))
    else:
        sz = int32(imageSize)
    end

    imgArea = sz(1) * sz(2)
    validateattributes(regionAreaRange, mcellarray([mstring('numeric')]), mcellarray([mstring('integer'), mstring('nonsparse'), mstring('real'), mstring('positive'), mstring('size'), mcat([1, 2])]), mfilename)

    coder.internal.errorIf(regionAreaRange(2) < regionAreaRange(1), mstring('vision:detectMSERFeatures:invalidRegionSizeRange'))

    # When the imageSize is less than area range, throw a warning.
    if imgArea < int32(regionAreaRange(1)):
        coder.internal.warning(mstring('vision:detectMSERFeatures:imageAreaLessThanAreaRange'))
    end


    #==========================================================================
@mfunction("tf")
def checkMaxAreaVariation(maxAreaVariation=None):
    validateattributes(maxAreaVariation, mcellarray([mstring('numeric')]), mcellarray([mstring('nonsparse'), mstring('real'), mstring('scalar'), mstring('>='), 0]), mfilename)
    tf = true

    #==========================================================================


    flag = isempty(coder.target)

    #==========================================================================
@mfunction("outVal")
def cCast(outClass=None, inVal=None):
    outVal = coder.nullcopy(zeros(1, 1, outClass))
    outVal = coder.ceval(mcat([mstring('('), outClass, mstring(')')]), inVal)