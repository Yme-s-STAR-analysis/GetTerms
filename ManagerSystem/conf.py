r'''
    Version: 7.0
    Date: 29.07.2024
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
    ref3 = False
    cent_edge = [511, 423, 289, 194, 125, 76, 43, 23, 11]
    cent_edgeX = [710, 590, 407, 275, 178, 109, 62, 33, 16]
    Npart = [342, 290, 226, 160, 110, 72, 44, 25, 13]
    NpartX = [342, 290, 226, 160, 110, 72, 44, 25, 13]
    w8 = [1.50625, -79.9735, 2.42896, 27.4434, -0.00119101, 8.70066e-07, 4461.3, 289]
    w8X = [1.62005, -145.283, 2.37174, 48.7206, -0.00102936, 5.35555e-07, 11989.1, 407]

class CutArgs:
    nHitsFit = 20
    nSig = 2.0 
    dca = 1.0
    m2Min = 0.6
    m2Max = 1.2

    # pT scan options
    ptScan = False
    ptMin = 0.4 # when do pT scan,
    ptMax = 2.0 # this value will be default
    pTRange = { # tag: [min, max]
        "0p8": [0.4, 0.8, -50, 50],
        "1p0": [0.4, 1.0, -50, 50],
        "1p2": [0.4, 1.2, -50, 50],
        "1p4": [0.4, 1.4, -50, 50],
        "1p6": [0.4, 1.6, -50, 50],
        "1p8": [0.4, 1.8, -50, 50],
    }

    # y scan options
    yScan = True
    yMin = 0.0 # when do pt scan
    yMax = 0.5 # these values will be default
    yMode = 1  # y min/max and mode (-0.5~0.5)
    yRange = { # tag: [min, max, mode, vz range]
        "0p1": [0.0, 0.1, 1, -50, 50],
        "0p2": [0.0, 0.2, 1, -50, 50],
        "0p3": [0.0, 0.3, 1, -50, 50],
        "0p4": [0.0, 0.4, 1, -50, 50],
        "0p5": [0.0, 0.5, 1, -50, 50],
        "0p6": [0.0, 0.6, 1, -25, 25],
    }

