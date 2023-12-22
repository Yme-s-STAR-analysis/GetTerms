r'''
    Version: 3.3
    Date: 22.12.2023
'''

class Args:
    nFilesPerJob = 30
    targetDir = '/star/u/yghuang/pwgdata/DataAnalysis/BES2/17p3/cumulant/231011_1'
    outDir = f'{targetDir}/job'
    mergeDir = f'{targetDir}/merge'
    runDir = f'{targetDir}/run'
    fileList = '/star/u/yghuang/Work/DataAnalysis/BES2/17p3/cumulant/AceTree/ace.file.list'
    tpc_eff_path = 'none'
    tof_eff_path = 'none'
    pid_eff_path = 'none'
    nSigmaTag = '2p0'
    eff_fac_pro = 1.0
    eff_fac_pbar = 1.0
    use_etof = 0 # 1 for use, 0 for ignore
    calc_exec = '/star/u/yghuang/Work/DataAnalysis/BES2/19p6/Cumulant/CumCalc/runCumulant'
    duo_cbwc_exec = '/star/u/yghuang/Work/DataAnalysis/BES2/19p6/Cumulant/CumCalc/duoCBWC'
    title = 'default'

class CutArgs:
    vzBin = 5
    vzRange = 50 # this works only when vzBin is 1
    vr = 2.0
    DCAz = 30.0
    DCAxy = 10.0
    nHitsFit = 20
    nHitsDedx = 5
    nHitsRatio = 0.52
    nSig = 2.0 
    dca = 1.0
    m2Min = 0.6
    m2Max = 1.2

    # pT scan options
    ptScan = True
    ptMin = 0.4
    ptMax = 2.0 # when do rapidity scan, this value will be default pt max
    ptMaxs = [
        # 2.0
        0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0
    ]
    ptTags = [
        # "2p0"
        "0p8", "1p0", "1p2", "1p4", "1p6", "1p8", "2p0"
    ]

    # y scan options
    yScan = True
    yMin = 0.0 # When do pt scan
    yMax = 0.5 # these values will be default
    yMode = 1  # y min/max and mode (-0.5~0.5)
    yMins = [
        0.0, 0.0, 0.0, 0.0, 0.0
    ]
    yMaxs = [
        0.1, 0.2, 0.3, 0.4, 0.5
    ]
    yModes = [ # 1 for absolute value of y and 2 for specified range
        1, 1, 1, 1, 1
    ]
    yTags = [
        '0p1', "0p2", "0p3", "0p4", "0p5"
    ]

