r'''
    Version: 7.7
    Date: 04.02.2025
'''

class Args:
    nFilesPerJob = 50
    targetDir = '/target/path'
    outDir = f'{targetDir}/job'
    mergeDir = f'{targetDir}/merge'
    runDir = f'{targetDir}/run'
    fileList = 'acetree.file.list'
    tpc_eff_path = 'TpcEff.default.root'
    tof_eff_path = 'TofEff.default.root'
    pid_eff_path = 'PidEff.root'
    nSigmaTag = '2p0'
    eff_fac_pro = 1.0
    eff_fac_pbar = 1.0
    calc_exec = '/star/u/yghuang/.tools/CumulantCalculation/runCumulant4'
    title = 'default'
    ref3 = False
    cent_edge = [500, 400, 350, 300, 250, 200, 150, 100, 50]
    cent_edgeX = [700, 600, 500, 400, 350, 300, 250, 150, 100]
    Npart = [342, 290, 226, 160, 110, 72, 44, 25, 13]
    NpartX = [342, 290, 226, 160, 110, 72, 44, 25, 13]
    w8 = [1.0, -80.0, 2.4, 48.7, -0.0012, 8e-7, 12000.0, 999]
    w8X = [1.0, -80.0, 2.4, 48.7, -0.0012, 8e-7, 12000.0, 999]

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

