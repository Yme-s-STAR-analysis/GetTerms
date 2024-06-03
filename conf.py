r'''
    Version: 5.0
    Date: 03.06.2024
'''

class Args:
    nFilesPerJob = 20
    targetDir = '/target/path'
    outDir = f'{targetDir}/job'
    mergeDir = f'{targetDir}/merge'
    runDir = f'{targetDir}/run'
    fileList = '/star/u/yghuang/Work/DataAnalysis/BES2/OverAll/3AceList/19.list'
    tpc_eff_path = '/star/u/yghuang/Work/DataAnalysis/BES2/OverAll/4EmbedList/4EffFiles/19/TpcEff.default.root'
    tof_eff_path = '/star/u/yghuang/Work/DataAnalysis/BES2/OverAll/4EmbedList/4EffFiles/19/TofEff.default.root'
    pid_eff_path = '/star/u/yghuang/Work/DataAnalysis/BES2/OverAll/4EmbedList/4EffFiles/19/PidEff.root'
    nSigmaTag = '2p0'
    eff_fac_pro = 1.0
    eff_fac_pbar = 1.0
    calc_exec = '/star/u/yghuang/.tools/CumulantCalculation/runCumulant'
    title = 'default'

class CutArgs:
    vzBin = 1
    vzRange = 50 # this works only when vzBin is 1
    nHitsFit = 20
    nSig = 2.0 
    dca = 1.0
    m2Min = 0.6
    m2Max = 1.2

    # pT scan options
    ptScan = False
    ptMin = 0.4
    ptMax = 2.0 # when do rapidity scan, this value will be default pt max
    ptMaxs = [
        0.8, 1.0, 1.2, 1.4, 1.6, 1.8
    ]
    ptTags = [
        "0p8", 
        "1p0", 
        "1p2", 
        "1p4", 
        "1p6", 
        "1p8"
    ]

    # y scan options
    yScan = True
    yMin = 0.0 # when do pt scan
    yMax = 0.5 # these values will be default
    yMode = 1  # y min/max and mode (-0.5~0.5)
    yMins = [
        0.0
        # 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    ]
    yMaxs = [
        0.5
        # 0.1, 0.2, 0.3, 0.4, 0.5, 0.6
    ]
    yModes = [ # 1 for absolute value of y and 2 for specified range
        1
        # 1, 1, 1, 1, 1, 1
    ]
    yTags = [
        # '0p1',
        # "0p2",
        # "0p3",
        # "0p4",
        "0p5",
        # "0p6"
    ]

