r'''
    
    Cumulant Calculation Manage System
    Author: Yige HUANG

    Latest Revision v4.3 (27.4.2024) - Yige Huang

    1. Some quantities are removed, so they won't be written into cfg file

    2. The resubmit mode is removed from manager system
    
    Revision v4.1 (5.4.2024) - Yige Huang

    1. Centrality files are now using Indian method, it's actually not significantly changing this program but need some updates on Core.cxx and this module
    
    Revision v4.0.3 (1.2.2024) - Yige Huang

    1. Suggested number of files per job: 30 -> 10

    2. Fix a minor bug in merge part

    3. Fix some bugs in calculate part

    4. Fix some bugs in collect part
    
    Revision: v4.0 (30.1.2024) - Yige Huang

    1. Support RefMult3X

    2. For |y| < 0.6, Vz is limited to be less than 30 (in manager-level)
    
    Revision: v3.4 (8.1.2023) - Yige Huang

    1. New feature: find the failed job and resubmit
    
    Revision: v3.3 (22.12.2023) - Yige Huang

    1. New feature: pT scan.
    
    Revision: v3.2 (15.12.2023) - Yige Huang

    1. Fix a minor bug: when prepare job folders, the log system is repeating too many times 'Done.'
    
    Revision: v3.1.2 (2.11.2023) - Yige Huang

    1. Fix a bug: the merge process of pDist can not work well, as the file name of pDist is incorrect.

    Revision: v3.1.1 (1.11.2023) - Yige Huang

    1. Improve the experience of using when tracking the status of submitted jobs.
    
    Revision: v3.1 (30.10.2023) - Yige Huang

    1. Updated the job name of merge and calc, which can make it easier to track the unfinished jobs.

    2. Now Vz split is embedded in the scan process.
    
    Revision: v3.0 (23.10.2023) - Yige Huang

    1. Now have 2 efficiency factors for proton and antiproton.

    2. The job index and job name will be shown in condor system.
    
    Revision: v2.7 (16.10.2023) - Yige Huang

    1. Now Vz range is now a sysmmetric value
    
    Revision: v2.6 (12.10.2023) - Yige Huang

    1. Bug fix: using submit mode with option [s] and [b] will get the bonus job lost.
    
    Revision: v2.5 (29.09.2023) - Yige Huang

    1. EffMaker is updated
    
    > By setting path of Efficiency file as "none", we can switch off the effciency factor (as 1.0). 
    > So the validation check part of manager has a little change.
    
    2. eTOF updates

    > Now the StFemtoTrack has eTOF mass2, should we use eTOF or not can be set in manager as well.
    > An additioanl eTOF argument is considered when copy getTerms.sh

    3. Rapidity scan

    > Now we can select the rapidity is symmetric about 0 or a specified range.
    > That is, we use cut like |y| < 0.5, or -0.3 < y < 0.5.

    4. Submit mode

    > Now you can generate files but don't submit, or directly submit with generated files.
    > Also, the default mode is generate files and submit.
    > Usage: python3 manager.py submit $OPT
    > Where OPT can be [a] (for All), [s] (for Sim) and [b] (for suBmit)

    Revision: v2.4 (16.08.2023) - Yige Huang

    > With getTerms core code version 2.3.
    > Cancel the PIDMODE arguments.

'''


import sys
import os
from conf import Args, CutArgs
from yLog import yLog

__version__ = '4.3'
__updatedTime__ = '27.04.2024'

mode = sys.argv[1]
assert(mode in ['sub', 'submit', 'mer', 'merge', 'run', 'calc', 'col', 'collect', 'clean', 'repo', 'report'])

if mode not in ['clean', 'repo', 'report']:
    # verifying rapidity scan validation
    if CutArgs.yScan:
        nScan = len(CutArgs.yTags)
        if not nScan == len(CutArgs.yMins) == len(CutArgs.yMaxs):
            raise Exception('[ERROR] The rapidity scan min and max should have a same length with y tags.')
    if CutArgs.ptScan:
        nScan = len(CutArgs.ptTags)
        if not nScan == len(CutArgs.ptMaxs):
            raise Exception('[ERROR] The pt scan max should have a same length with pt tags.')
    if CutArgs.yScan:
        print(f'Rapidity scan is [ON] with {len(CutArgs.yTags)} jobs.')
        print(f'During rapidity scan, pT range will be [{CutArgs.ptMin}, {CutArgs.ptMax}].')
        print(f'{CutArgs.yMins=}')
        print(f'{CutArgs.yMaxs=}')
        print(f'{CutArgs.yTags=}')
    else:
        print(f'Rapidity scan is [OFF].')
    if CutArgs.ptScan:
        print(f'pT scan is [ON] with {len(CutArgs.ptTags)} jobs.')
        print(f'During pT scan, y range will be [{CutArgs.yMin}, {CutArgs.yMax}].')
        print(f'{CutArgs.ptMin=}')
        print(f'{CutArgs.ptMaxs=}')
        print(f'{CutArgs.ptTags=}')


with open(Args.fileList) as f:
    flist = f.readlines()
nFiles = len(flist)
nFilesPerJob = Args.nFilesPerJob
nJobs = nFiles // nFilesPerJob
bonus = nFiles - nJobs * nFilesPerJob

# submit mode
if (mode in ['sub', 'submit']):
    l = yLog('.submit.log')
    if len(sys.argv) == 2:
        sMode = 'a' # by default
        l.log('Generate sub-folders and submit.')
    else:
        sMode = sys.argv[2]
        assert(sMode in ['a', 's', 'b'])
        if sMode == 'a':
            l.log('Generate sub-folders and submit.')
        if sMode == 's':
            l.log('Simulation mode, only generate sub-folders, you can submit the jobs with option [b].')
        if sMode == 'b':
            l.log('Submit jobs with pre-generated sub-folders.')
    l.log(f'===Submit System for GetTerms===')
    l.log('Summary of configuration are listed below:')
    l.log(f'{Args.nFilesPerJob=}')
    l.log(f'{Args.outDir=}')
    l.log(f'{Args.fileList=}')
    l.log(f'{Args.tpc_eff_path=}')
    l.log(f'{Args.tof_eff_path=}')
    l.log(f'{Args.pid_eff_path=}')
    l.log(f'{Args.nSigmaTag=}')
    l.log(f'{Args.eff_fac_pro=}')
    l.log(f'{Args.eff_fac_pbar=}')
    l.log(f'{nFiles} files in total, {nJobs} regular jobs with {nFilesPerJob} files to handle.')
    if bonus:
        l.log(f'Bonus job will manage {bonus} jobs.')


    l.log('Now preparing Job Directory and File Lists. May take few seconds.')
    outDir = Args.outDir
    if not os.path.exists(outDir):
        os.mkdir(outDir)

    if sMode in ['a', 's']:
        for i in range(nJobs):
            if not os.path.exists(f'{outDir}/job{i}'):
                os.mkdir(f'{outDir}/job{i}')
                with open(f'{outDir}/job{i}/file.list', 'w') as f:
                    for line in range(i * nFilesPerJob, (i+1) * nFilesPerJob):
                        f.write(flist[line])
        if bonus:
            if not os.path.exists(f'{outDir}/job{nJobs}'):
                os.mkdir(f'{outDir}/job{nJobs}')
                with open(f'{outDir}/job{nJobs}/file.list', 'w') as f:
                    for line in range(nJobs * nFilesPerJob, nFiles):
                        f.write(flist[line])
        l.log('Done.')

        l.log('Now copying necessary files. May take few seconds.')
        if bonus:
            nJobs += 1
    
        # getTerms (exec): just symlink
        # getTerms.sh: change the path and the name
        # getTerms.job: change the description (.sh name) and name
        # getTerms.cfg: generate one and symlink to jobs

        if CutArgs.vzBin not in [1, 3, 5]:
            raise Exception(f'[ERROR] The Vz bins should be 1, 3 or 5')

        vzMins = []
        vzMaxs = []

        if CutArgs.vzBin == 1:
            vzMins = [-CutArgs.vzRange]
            vzMaxs = [CutArgs.vzRange]
            l.log(f'Vz selection information: there will be only 1 Vz bin from {-CutArgs.vzRange} to {CutArgs.vzRange}')
        if CutArgs.vzBin == 3:
            vzMins = [-30, -10, 10]
            vzMaxs = [-10, 10, 30]
            l.log(f'Vz selection information: there will be only 3 Vz bins from -30 to 30')
        if CutArgs.vzBin == 5:
            vzMins = [-30, -10, 10, -50, 30]
            vzMaxs = [-10, 10, 30, -30, 50]
            l.log(f'Vz selection information: there will be only 5 Vz bins from -50 to 50')
        
        for vzIdx, vzRange in enumerate(zip(vzMins, vzMaxs)):

            vzMin, vzMax = vzRange

            # prepare y scan
            if CutArgs.yScan:
                for item, ymin, ymax, ymode in zip(CutArgs.yTags, CutArgs.yMins, CutArgs.yMaxs, CutArgs.yModes):
                    with open(f'{Args.title}.y{item}.vz{vzIdx}.getTerms.cfg', 'w') as f:
                        # for high rapidity scan, reduce the vz range
                        vzMinTmp = vzMin
                        vzMaxTmp = vzMax
                        if ymax > 0.55 and ymode == 1 and CutArgs.vzBin == 1 and vzMax > 30:
                            vzMinTmp = -30
                            vzMaxTmp = 30
                        f.write(f'VARLIST\n')
                        f.write(f'VZ\t{vzMinTmp}\t{vzMaxTmp}\n')
                        f.write(f'PT\t{CutArgs.ptMin}\t{CutArgs.ptMax}\nYP\t{ymin}\t{ymax}\nNHITSFIT\t{CutArgs.nHitsFit}\n')
                        f.write(f'NSIG\t{CutArgs.nSig}\nDCA\t{CutArgs.dca}\nMASS2\t{CutArgs.m2Min}\t{CutArgs.m2Max}\nRMODE\t{ymode}\n')
                        f.write(f'END')

            # prepare pt scan
            if CutArgs.ptScan:
                for item, ptmax in zip(CutArgs.ptTags, CutArgs.ptMaxs):
                    with open(f'{Args.title}.pt{item}.vz{vzIdx}.getTerms.cfg', 'w') as f:
                        f.write(f'VARLIST\n')
                        f.write(f'VZ\t{vzMin}\t{vzMax}\n')
                        f.write(f'PT\t{CutArgs.ptMin}\t{ptmax}\nYP\t{CutArgs.yMin}\t{CutArgs.yMax}\nNHITSFIT\t{CutArgs.nHitsFit}\n')
                        f.write(f'NSIG\t{CutArgs.nSig}\nDCA\t{CutArgs.dca}\nMASS2\t{CutArgs.m2Min}\t{CutArgs.m2Max}\nRMODE\t{CutArgs.yMode}\n')
                        f.write(f'END')

        for i in range(nJobs):
            tdir = f'{outDir}/job{i}'

            # getTerms exec
            if not os.path.exists(f'{tdir}/getTerms'):
                os.symlink(f'{os.getcwd()}/getTerms', f'{tdir}/getTerms')

            for vzIdx in range(CutArgs.vzBin):
                # getTerms job shell
                # for y scan
                if CutArgs.yScan:
                    for item in CutArgs.yTags:
                        os.system(f'cp getTerms.sh {tdir}/{Args.title}.{i}.y{item}.vz{vzIdx}.getTerms.sh')
                        os.system(f'sed -i "s|TPC_PATH|{Args.tpc_eff_path}|g" {tdir}/{Args.title}.{i}.y{item}.vz{vzIdx}.getTerms.sh')
                        os.system(f'sed -i "s|TOF_PATH|{Args.tof_eff_path}|g" {tdir}/{Args.title}.{i}.y{item}.vz{vzIdx}.getTerms.sh')
                        os.system(f'sed -i "s|PID_PATH|{Args.pid_eff_path}|g" {tdir}/{Args.title}.{i}.y{item}.vz{vzIdx}.getTerms.sh')
                        os.system(f'sed -i "s|NSIG_TAG|{Args.nSigmaTag}|g" {tdir}/{Args.title}.{i}.y{item}.vz{vzIdx}.getTerms.sh')
                        os.system(f'sed -i "s|EFF_FAC_PRO|{Args.eff_fac_pro}|g" {tdir}/{Args.title}.{i}.y{item}.vz{vzIdx}.getTerms.sh')
                        os.system(f'sed -i "s|EFF_FAC_PBAR|{Args.eff_fac_pbar}|g" {tdir}/{Args.title}.{i}.y{item}.vz{vzIdx}.getTerms.sh')
                        os.system(f'sed -i "s|TASK_TAG|{Args.title}.y{item}.vz{vzIdx}|g" {tdir}/{Args.title}.{i}.y{item}.vz{vzIdx}.getTerms.sh')
                # for pt scan
                if CutArgs.ptScan:
                    for item in CutArgs.ptTags:
                        os.system(f'cp getTerms.sh {tdir}/{Args.title}.{i}.pt{item}.vz{vzIdx}.getTerms.sh')
                        os.system(f'sed -i "s|TPC_PATH|{Args.tpc_eff_path}|g" {tdir}/{Args.title}.{i}.pt{item}.vz{vzIdx}.getTerms.sh')
                        os.system(f'sed -i "s|TOF_PATH|{Args.tof_eff_path}|g" {tdir}/{Args.title}.{i}.pt{item}.vz{vzIdx}.getTerms.sh')
                        os.system(f'sed -i "s|PID_PATH|{Args.pid_eff_path}|g" {tdir}/{Args.title}.{i}.pt{item}.vz{vzIdx}.getTerms.sh')
                        os.system(f'sed -i "s|NSIG_TAG|{Args.nSigmaTag}|g" {tdir}/{Args.title}.{i}.pt{item}.vz{vzIdx}.getTerms.sh')
                        os.system(f'sed -i "s|EFF_FAC_PRO|{Args.eff_fac_pro}|g" {tdir}/{Args.title}.{i}.pt{item}.vz{vzIdx}.getTerms.sh')
                        os.system(f'sed -i "s|EFF_FAC_PBAR|{Args.eff_fac_pbar}|g" {tdir}/{Args.title}.{i}.pt{item}.vz{vzIdx}.getTerms.sh')
                        os.system(f'sed -i "s|TASK_TAG|{Args.title}.pt{item}.vz{vzIdx}|g" {tdir}/{Args.title}.{i}.pt{item}.vz{vzIdx}.getTerms.sh')

                # getTerms job file
                # for y scan
                if CutArgs.yScan:
                    for item in CutArgs.yTags:
                        os.system(f'cp getTerms.job {tdir}/{Args.title}.{i}.y{item}.vz{vzIdx}.getTerms.job')
                        os.system(f'sed -i "s|GTMS|{Args.title}.{i}.y{item}.vz{vzIdx}.getTerms.sh|g" {tdir}/{Args.title}.{i}.y{item}.vz{vzIdx}.getTerms.job')
                        os.system(f'sed -i "s|Job|y{item}.Job|g" {tdir}/{Args.title}.{i}.y{item}.vz{vzIdx}.getTerms.job')
                # for pt scan
                if CutArgs.ptScan:
                    for item in CutArgs.ptTags:
                        os.system(f'cp getTerms.job {tdir}/{Args.title}.{i}.pt{item}.vz{vzIdx}.getTerms.job')
                        os.system(f'sed -i "s|GTMS|{Args.title}.{i}.pt{item}.vz{vzIdx}.getTerms.sh|g" {tdir}/{Args.title}.{i}.pt{item}.vz{vzIdx}.getTerms.job')
                        os.system(f'sed -i "s|Job|pt{item}.Job|g" {tdir}/{Args.title}.{i}.pt{item}.vz{vzIdx}.getTerms.job')

                # getTerms cfg file
                # for y scan
                if CutArgs.yScan:
                    for item in CutArgs.yTags:
                        if os.path.exists(f'{tdir}/{Args.title}.y{item}.vz{vzIdx}.getTerms.cfg'):
                            os.system(f'rm {tdir}/{Args.title}.y{item}.vz{vzIdx}.getTerms.cfg')
                        os.symlink(f'{os.getcwd()}/{Args.title}.y{item}.vz{vzIdx}.getTerms.cfg', f'{tdir}/{Args.title}.y{item}.vz{vzIdx}.getTerms.cfg')
                # for pt scan
                if CutArgs.ptScan:
                    for item in CutArgs.ptTags:
                        if os.path.exists(f'{tdir}/{Args.title}.pt{item}.vz{vzIdx}.getTerms.cfg'):
                            os.system(f'rm {tdir}/{Args.title}.pt{item}.vz{vzIdx}.getTerms.cfg')
                        os.symlink(f'{os.getcwd()}/{Args.title}.pt{item}.vz{vzIdx}.getTerms.cfg', f'{tdir}/{Args.title}.pt{item}.vz{vzIdx}.getTerms.cfg')

        l.log('Done.')


    if sMode in ['a', 'b']:
        if bonus and sMode == 'b':
            nJobs += 1
        l.log('Now submitting jobs.')
        # for y scan
        if CutArgs.yScan:
            for item in CutArgs.yTags:
                for i in range(nJobs):
                    tdir = f'{outDir}/job{i}'
                    l.log(f' - Current {item}::job{i} / {nJobs}')
                    for vzIdx in range(CutArgs.vzBin):
                        os.system(f'cd {tdir} && condor_submit {Args.title}.{i}.y{item}.vz{vzIdx}.getTerms.job')
        # for pt scan
        if CutArgs.ptScan:
            for item in CutArgs.ptTags:
                for i in range(nJobs):
                    tdir = f'{outDir}/job{i}'
                    l.log(f' - Current {item}::job{i} / {nJobs}')
                    for vzIdx in range(CutArgs.vzBin):
                        os.system(f'cd {tdir} && condor_submit {Args.title}.{i}.pt{item}.vz{vzIdx}.getTerms.job')
        l.log('All submitted!')

# merge mode
if mode in ['mer', 'merge']:
    l = yLog('.merge.log')
    outDir = Args.outDir
    mergeDir = Args.mergeDir

    if not os.path.exists(outDir):
        raise Exception(f'{outDir=} which does not exist.')

    if not os.path.exists(mergeDir):
        os.mkdir(mergeDir)

    l.log('Here are the root files to be merged:')
    if CutArgs.yScan:
        l.log('For rapidity scan:')
        for idx, item in enumerate(CutArgs.yTags):
            l.log(f'Item {idx+1:03d}: y{item}')
    if CutArgs.ptScan:
        l.log('For pT scan:')
        for idx, item in enumerate(CutArgs.ptTags):
            l.log(f'Item {idx+1:03d}: pt{item}')

    # for y scan
    if CutArgs.yScan:
        for item in CutArgs.yTags:
            # mTerms
            if not os.path.exists(f'{mergeDir}/y{item}'):
                os.mkdir(f'{mergeDir}/y{item}')
            os.system(f'cp merge.py {mergeDir}/y{item}')
            os.system(f'cp yLog.py {mergeDir}/y{item}')
            for vzIdx in range(CutArgs.vzBin):
                os.system(f'cp merge.sh {mergeDir}/y{item}/{Args.title}.y{item}.vz{vzIdx}.merge.sh')
                os.system(f'cp merge.job {mergeDir}/y{item}/{Args.title}.vz{vzIdx}.merge.job')
                os.system(f'sed -i "s|TASKNAME|{Args.title}.y{item}.vz{vzIdx}|g" {mergeDir}/y{item}/{Args.title}.y{item}.vz{vzIdx}.merge.sh')
                os.system(f'sed -i "s|OUTDIR|{outDir}|g" {mergeDir}/y{item}/{Args.title}.y{item}.vz{vzIdx}.merge.sh')
                os.system(f'sed -i "s|MERDIR|{mergeDir}|g" {mergeDir}/y{item}/{Args.title}.y{item}.vz{vzIdx}.merge.sh')
                os.system(f'sed -i "s|SHELLNAME|{Args.title}.y{item}.vz{vzIdx}.merge.sh|g" {mergeDir}/y{item}/{Args.title}.vz{vzIdx}.merge.job')
                os.system(f'sed -i "s|TASKNAME|{Args.title}.y{item}.vz{vzIdx}|g" {mergeDir}/y{item}/{Args.title}.vz{vzIdx}.merge.job')
                os.system(f'cd {mergeDir}/y{item} && condor_submit {Args.title}.vz{vzIdx}.merge.job')
                l.log(f' - Current y{item} - Vz {vzIdx}')
            # mTerms RefMult3X
            if not os.path.exists(f'{mergeDir}/y{item}X'):
                os.mkdir(f'{mergeDir}/y{item}X')
            os.system(f'cp merge.py {mergeDir}/y{item}X')
            os.system(f'cp yLog.py {mergeDir}/y{item}X')
            for vzIdx in range(CutArgs.vzBin):
                os.system(f'cp merge.sh {mergeDir}/y{item}X/{Args.title}.y{item}.vz{vzIdx}.mergeX.sh')
                os.system(f'cp merge.job {mergeDir}/y{item}X/{Args.title}.vz{vzIdx}.merge.job')
                os.system(f'sed -i "s|TASKNAME|{Args.title}.y{item}.vz{vzIdx}X|g" {mergeDir}/y{item}X/{Args.title}.y{item}.vz{vzIdx}.mergeX.sh')
                os.system(f'sed -i "s|OUTDIR|{outDir}|g" {mergeDir}/y{item}X/{Args.title}.y{item}.vz{vzIdx}.mergeX.sh')
                os.system(f'sed -i "s|MERDIR|{mergeDir}|g" {mergeDir}/y{item}X/{Args.title}.y{item}.vz{vzIdx}.mergeX.sh')
                os.system(f'sed -i "s|SHELLNAME|{Args.title}.y{item}.vz{vzIdx}.mergeX.sh|g" {mergeDir}/y{item}X/{Args.title}.vz{vzIdx}.merge.job')
                os.system(f'sed -i "s|TASKNAME|{Args.title}.y{item}.vz{vzIdx}|g" {mergeDir}/y{item}X/{Args.title}.vz{vzIdx}.merge.job')
                os.system(f'cd {mergeDir}/y{item}X && condor_submit {Args.title}.vz{vzIdx}.merge.job')
                l.log(f' - Current y{item} - Vz {vzIdx} (X)')
            # proton number distribution
            pDist = f'y{item}.pDist'
            if not os.path.exists(f'{mergeDir}/{pDist}'):
                os.mkdir(f'{mergeDir}/{pDist}')
            os.system(f'cp merge.py {mergeDir}/{pDist}')
            os.system(f'cp yLog.py {mergeDir}/{pDist}')
            for vzIdx in range(CutArgs.vzBin):
                os.system(f'cp merge.sh {mergeDir}/{pDist}/{Args.title}.{pDist}.vz{vzIdx}.merge.sh')
                os.system(f'cp merge.job {mergeDir}/{pDist}/{Args.title}.vz{vzIdx}.merge.job')
                os.system(f'sed -i "s|TASKNAME|{Args.title}.y{item}.vz{vzIdx}.pDist|g" {mergeDir}/{pDist}/{Args.title}.{pDist}.vz{vzIdx}.merge.sh')
                os.system(f'sed -i "s|OUTDIR|{outDir}|g" {mergeDir}/{pDist}/{Args.title}.{pDist}.vz{vzIdx}.merge.sh')
                os.system(f'sed -i "s|MERDIR|{mergeDir}|g" {mergeDir}/{pDist}/{Args.title}.{pDist}.vz{vzIdx}.merge.sh')
                os.system(f'sed -i "s|SHELLNAME|{Args.title}.{pDist}.vz{vzIdx}.merge.sh|g" {mergeDir}/{pDist}/{Args.title}.vz{vzIdx}.merge.job')
                os.system(f'sed -i "s|TASKNAME|{Args.title}.y{item}.vz{vzIdx}.pDist|g" {mergeDir}/{pDist}/{Args.title}.vz{vzIdx}.merge.job')
                os.system(f'cd {mergeDir}/{pDist} && condor_submit {Args.title}.vz{vzIdx}.merge.job')
                l.log(f' - Current {pDist} - Vz {vzIdx}')
    # for pt scan
    if CutArgs.ptScan:
        for item in CutArgs.ptTags:
            # mTerms
            if not os.path.exists(f'{mergeDir}/pt{item}'):
                os.mkdir(f'{mergeDir}/pt{item}')
            os.system(f'cp merge.py {mergeDir}/pt{item}')
            os.system(f'cp yLog.py {mergeDir}/pt{item}')
            for vzIdx in range(CutArgs.vzBin):
                os.system(f'cp merge.sh {mergeDir}/pt{item}/{Args.title}.pt{item}.vz{vzIdx}.merge.sh')
                os.system(f'cp merge.job {mergeDir}/pt{item}/{Args.title}.vz{vzIdx}.merge.job')
                os.system(f'sed -i "s|TASKNAME|{Args.title}.pt{item}.vz{vzIdx}|g" {mergeDir}/pt{item}/{Args.title}.pt{item}.vz{vzIdx}.merge.sh')
                os.system(f'sed -i "s|OUTDIR|{outDir}|g" {mergeDir}/pt{item}/{Args.title}.pt{item}.vz{vzIdx}.merge.sh')
                os.system(f'sed -i "s|MERDIR|{mergeDir}|g" {mergeDir}/pt{item}/{Args.title}.pt{item}.vz{vzIdx}.merge.sh')
                os.system(f'sed -i "s|SHELLNAME|{Args.title}.pt{item}.vz{vzIdx}.merge.sh|g" {mergeDir}/pt{item}/{Args.title}.vz{vzIdx}.merge.job')
                os.system(f'sed -i "s|TASKNAME|{Args.title}.pt{item}.vz{vzIdx}|g" {mergeDir}/pt{item}/{Args.title}.vz{vzIdx}.merge.job')
                os.system(f'cd {mergeDir}/pt{item} && condor_submit {Args.title}.vz{vzIdx}.merge.job')
                l.log(f' - Current pt{item} - Vz {vzIdx}')
            # mTerms RefMult3X
            if not os.path.exists(f'{mergeDir}/pt{item}X'):
                os.mkdir(f'{mergeDir}/pt{item}X')
            os.system(f'cp merge.py {mergeDir}/pt{item}X')
            os.system(f'cp yLog.py {mergeDir}/pt{item}X')
            for vzIdx in range(CutArgs.vzBin):
                os.system(f'cp merge.sh {mergeDir}/pt{item}X/{Args.title}.pt{item}.vz{vzIdx}.mergeX.sh')
                os.system(f'cp merge.job {mergeDir}/pt{item}X/{Args.title}.vz{vzIdx}.merge.job')
                os.system(f'sed -i "s|TASKNAME|{Args.title}.pt{item}.vz{vzIdx}X|g" {mergeDir}/pt{item}X/{Args.title}.pt{item}.vz{vzIdx}.mergeX.sh')
                os.system(f'sed -i "s|OUTDIR|{outDir}|g" {mergeDir}/pt{item}X/{Args.title}.pt{item}.vz{vzIdx}.mergeX.sh')
                os.system(f'sed -i "s|MERDIR|{mergeDir}|g" {mergeDir}/pt{item}X/{Args.title}.pt{item}.vz{vzIdx}.mergeX.sh')
                os.system(f'sed -i "s|SHELLNAME|{Args.title}.pt{item}.vz{vzIdx}.mergeX.sh|g" {mergeDir}/pt{item}X/{Args.title}.vz{vzIdx}.merge.job')
                os.system(f'sed -i "s|TASKNAME|{Args.title}.pt{item}.vz{vzIdx}|g" {mergeDir}/pt{item}X/{Args.title}.vz{vzIdx}.merge.job')
                os.system(f'cd {mergeDir}/pt{item}X && condor_submit {Args.title}.vz{vzIdx}.merge.job')
                l.log(f' - Current pt{item} - Vz {vzIdx} (X)')
            # proton number distribution
            pDist = f'pt{item}.pDist'
            if not os.path.exists(f'{mergeDir}/{pDist}'):
                os.mkdir(f'{mergeDir}/{pDist}')
            os.system(f'cp merge.py {mergeDir}/{pDist}')
            os.system(f'cp yLog.py {mergeDir}/{pDist}')
            for vzIdx in range(CutArgs.vzBin):
                os.system(f'cp merge.sh {mergeDir}/{pDist}/{Args.title}.{pDist}.vz{vzIdx}.merge.sh')
                os.system(f'cp merge.job {mergeDir}/{pDist}/{Args.title}.vz{vzIdx}.merge.job')
                os.system(f'sed -i "s|TASKNAME|{Args.title}.pt{item}.vz{vzIdx}.pDist|g" {mergeDir}/{pDist}/{Args.title}.{pDist}.vz{vzIdx}.merge.sh')
                os.system(f'sed -i "s|OUTDIR|{outDir}|g" {mergeDir}/{pDist}/{Args.title}.{pDist}.vz{vzIdx}.merge.sh')
                os.system(f'sed -i "s|MERDIR|{mergeDir}|g" {mergeDir}/{pDist}/{Args.title}.{pDist}.vz{vzIdx}.merge.sh')
                os.system(f'sed -i "s|SHELLNAME|{Args.title}.{pDist}.vz{vzIdx}.merge.sh|g" {mergeDir}/{pDist}/{Args.title}.vz{vzIdx}.merge.job')
                os.system(f'sed -i "s|TASKNAME|{Args.title}.pt{item}.vz{vzIdx}.pDist|g" {mergeDir}/{pDist}/{Args.title}.vz{vzIdx}.merge.job')
                os.system(f'cd {mergeDir}/{pDist} && condor_submit {Args.title}.vz{vzIdx}.merge.job')
                l.log(f' - Current {pDist} - Vz {vzIdx}')

    l.log('All submitted!')

# run mode
if mode in ['run', 'calc']:
    l = yLog('.calc.log')
    mergeDir = Args.mergeDir
    runDir = Args.runDir

    if not os.path.exists(mergeDir):
        raise Exception(f'{mergeDir=} which does not exist.')
    
    if not os.path.exists(runDir):
        os.mkdir(runDir)

    l.log('Here are the task names to be calculated:')
    if CutArgs.yScan:
        for idx, item in enumerate(CutArgs.yTags):
            l.log('For rapidity scan:')
            l.log(f'Item {idx+1:03d} - y{item}')

        for item in CutArgs.yTags:
            # RefMult3
            if not os.path.exists(f'{runDir}/y{item}'):
                os.mkdir(f'{runDir}/y{item}')
            if not os.path.exists(f'{runDir}/y{item}/runCumulant'):
                os.symlink(Args.calc_exec, f'{runDir}/y{item}/runCumulant')
            if not os.path.exists(f'{runDir}/y{item}/cent_edge.txt'):
                os.symlink(f'{os.getcwd()}/cent_edge.txt', f'{runDir}/y{item}/cent_edge.txt')
            if not os.path.exists(f'{runDir}/y{item}/Npart.txt'):
                os.symlink(f'{os.getcwd()}/Npart.txt', f'{runDir}/y{item}/Npart.txt')
            for vzIdx in range(CutArgs.vzBin):
                if os.path.exists(f'{runDir}/y{item}/{Args.title}.y{item}.vz{vzIdx}.root'):
                    os.remove(f'{runDir}/y{item}/{Args.title}.y{item}.vz{vzIdx}.root')
                os.symlink(f'{mergeDir}/{Args.title}.y{item}.vz{vzIdx}.root', f'{runDir}/y{item}/{Args.title}.y{item}.vz{vzIdx}.root')
                os.system(f'cp calc.sh {runDir}/y{item}/{Args.title}.y{item}.vz{vzIdx}.calc.sh')
                os.system(f'cp calc.job {runDir}/y{item}/{Args.title}.y{item}.vz{vzIdx}.calc.job')
                os.system(f'sed -i "s|TASKNAME|{Args.title}.y{item}.vz{vzIdx}|g" {runDir}/y{item}/{Args.title}.y{item}.vz{vzIdx}.calc.sh')
                os.system(f'sed -i "s|SHELLNAME|{Args.title}.y{item}.vz{vzIdx}.calc.sh|g" {runDir}/y{item}/{Args.title}.y{item}.vz{vzIdx}.calc.job')
                os.system(f'sed -i "s|TASKNAME|{Args.title}.y{item}.vz{vzIdx}|g" {runDir}/y{item}/{Args.title}.y{item}.vz{vzIdx}.calc.job')
                os.system(f'cd {runDir}/y{item} && condor_submit {Args.title}.y{item}.vz{vzIdx}.calc.job')
                l.log(f' - Current y{item} - Vz {vzIdx}')
            # RefMult3X
            if not os.path.exists(f'{runDir}/y{item}X'):
                os.mkdir(f'{runDir}/y{item}X')
            if not os.path.exists(f'{runDir}/y{item}X/runCumulant'):
                os.symlink(Args.calc_exec, f'{runDir}/y{item}X/runCumulant')
            if not os.path.exists(f'{runDir}/y{item}X/cent_edge.txt'):
                os.symlink(f'{os.getcwd()}/cent_edgeX.txt', f'{runDir}/y{item}X/cent_edge.txt')
            if not os.path.exists(f'{runDir}/y{item}X/Npart.txt'):
                os.symlink(f'{os.getcwd()}/Npart.txt', f'{runDir}/y{item}X/Npart.txt')
            for vzIdx in range(CutArgs.vzBin):
                if os.path.exists(f'{runDir}/y{item}X/{Args.title}.y{item}.vz{vzIdx}X.root'):
                    os.remove(f'{runDir}/y{item}X/{Args.title}.y{item}.vz{vzIdx}X.root')
                os.symlink(f'{mergeDir}/{Args.title}.y{item}.vz{vzIdx}X.root', f'{runDir}/y{item}X/{Args.title}.y{item}.vz{vzIdx}X.root')
                os.system(f'cp calc.sh {runDir}/y{item}X/{Args.title}.y{item}.vz{vzIdx}.calcX.sh')
                os.system(f'cp calc.job {runDir}/y{item}X/{Args.title}.y{item}.vz{vzIdx}.calc.job')
                os.system(f'sed -i "s|TASKNAME|{Args.title}.y{item}.vz{vzIdx}X|g" {runDir}/y{item}X/{Args.title}.y{item}.vz{vzIdx}.calcX.sh')
                os.system(f'sed -i "s|SHELLNAME|{Args.title}.y{item}.vz{vzIdx}.calcX.sh|g" {runDir}/y{item}X/{Args.title}.y{item}.vz{vzIdx}.calc.job')
                os.system(f'sed -i "s|TASKNAME|{Args.title}.y{item}.vz{vzIdx}X|g" {runDir}/y{item}X/{Args.title}.y{item}.vz{vzIdx}.calc.job')
                os.system(f'cd {runDir}/y{item}X && condor_submit {Args.title}.y{item}.vz{vzIdx}.calc.job')
                l.log(f' - Current y{item} - Vz {vzIdx} (X)')

    if CutArgs.ptScan:
        for idx, item in enumerate(CutArgs.ptTags):
            l.log('For pt scan:')
            l.log(f'Item {idx+1:03d} - pt{item}')
        for item in CutArgs.ptTags:
            # RefMult3
            if not os.path.exists(f'{runDir}/pt{item}'):
                os.mkdir(f'{runDir}/pt{item}')
            if not os.path.exists(f'{runDir}/pt{item}/runCumulant'):
                os.symlink(Args.calc_exec, f'{runDir}/pt{item}/runCumulant')
            if not os.path.exists(f'{runDir}/pt{item}/cent_edge.txt'):
                os.symlink(f'{os.getcwd()}/cent_edge.txt', f'{runDir}/pt{item}/cent_edge.txt')
            if not os.path.exists(f'{runDir}/pt{item}/Npart.txt'):
                os.symlink(f'{os.getcwd()}/Npart.txt', f'{runDir}/pt{item}/Npart.txt')

            for vzIdx in range(CutArgs.vzBin):
                if os.path.exists(f'{runDir}/pt{item}/{Args.title}.pt{item}.vz{vzIdx}.root'):
                    os.remove(f'{runDir}/pt{item}/{Args.title}.pt{item}.vz{vzIdx}.root')
                os.symlink(f'{mergeDir}/{Args.title}.pt{item}.vz{vzIdx}.root', f'{runDir}/pt{item}/{Args.title}.pt{item}.vz{vzIdx}.root')
                os.system(f'cp calc.sh {runDir}/pt{item}/{Args.title}.pt{item}.vz{vzIdx}.calc.sh')
                os.system(f'cp calc.job {runDir}/pt{item}/{Args.title}.pt{item}.vz{vzIdx}.calc.job')
                os.system(f'sed -i "s|TASKNAME|{Args.title}.pt{item}.vz{vzIdx}|g" {runDir}/pt{item}/{Args.title}.pt{item}.vz{vzIdx}.calc.sh')
                os.system(f'sed -i "s|SHELLNAME|{Args.title}.pt{item}.vz{vzIdx}.calc.sh|g" {runDir}/pt{item}/{Args.title}.pt{item}.vz{vzIdx}.calc.job')
                os.system(f'sed -i "s|TASKNAME|pt{item}.vz{vzIdx}|g" {runDir}/pt{item}/{Args.title}.pt{item}.vz{vzIdx}.calc.job')
                os.system(f'cd {runDir}/pt{item} && condor_submit {Args.title}.pt{item}.vz{vzIdx}.calc.job')
                l.log(f' - Current pt{item} - Vz {vzIdx}')

            # RefMult3X
            if not os.path.exists(f'{runDir}/pt{item}X'):
                os.mkdir(f'{runDir}/pt{item}X')
            if not os.path.exists(f'{runDir}/pt{item}X/runCumulant'):
                os.symlink(Args.calc_exec, f'{runDir}/pt{item}X/runCumulant')
            if not os.path.exists(f'{runDir}/pt{item}X/cent_edge.txt'):
                os.symlink(f'{os.getcwd()}/cent_edgeX.txt', f'{runDir}/pt{item}X/cent_edge.txt')
            if not os.path.exists(f'{runDir}/pt{item}X/Npart.txt'):
                os.symlink(f'{os.getcwd()}/Npart.txt', f'{runDir}/pt{item}X/Npart.txt')
            for vzIdx in range(CutArgs.vzBin):
                if os.path.exists(f'{runDir}/pt{item}X/{Args.title}.pt{item}.vz{vzIdx}X.root'):
                    os.remove(f'{runDir}/pt{item}X/{Args.title}.pt{item}.vz{vzIdx}X.root')
                os.symlink(f'{mergeDir}/{Args.title}.pt{item}.vz{vzIdx}X.root', f'{runDir}/pt{item}X/{Args.title}.pt{item}.vz{vzIdx}X.root')
                os.system(f'cp calc.sh {runDir}/pt{item}X/{Args.title}.pt{item}.vz{vzIdx}.calcX.sh')
                os.system(f'cp calc.job {runDir}/pt{item}X/{Args.title}.pt{item}.vz{vzIdx}.calc.job')
                os.system(f'sed -i "s|TASKNAME|{Args.title}.pt{item}.vz{vzIdx}X|g" {runDir}/pt{item}X/{Args.title}.pt{item}.vz{vzIdx}.calcX.sh')
                os.system(f'sed -i "s|SHELLNAME|{Args.title}.pt{item}.vz{vzIdx}.calcX.sh|g" {runDir}/pt{item}X/{Args.title}.pt{item}.vz{vzIdx}.calc.job')
                os.system(f'sed -i "s|TASKNAME|{Args.title}.pt{item}.vz{vzIdx}X|g" {runDir}/pt{item}X/{Args.title}.pt{item}.vz{vzIdx}.calc.job')
                os.system(f'cd {runDir}/pt{item}X && condor_submit {Args.title}.pt{item}.vz{vzIdx}.calc.job')
                l.log(f' - Current pt{item} - Vz {vzIdx} (X)')
        
    l.log('All submitted!')

# collect mode
if mode in ['col', 'collect']:
    l = yLog('.collect.log')
    mergeDir = Args.mergeDir
    runDir = Args.runDir
    duo_cbwc = Args.duo_cbwc_exec

    if not os.path.exists(mergeDir):
        raise Exception(f'{mergeDir=} which does not exist.')

    if not os.path.exists(runDir):
        raise Exception(f'{runDir=} which does not exist.')
    
    if not os.path.exists(duo_cbwc):
        raise Exception(f'{duo_cbwc=} which does not exist.')
    
    l.log('Here are the task names to be collected:')
    if CutArgs.yScan:
        l.log(f'Rapidity scan is [ON]:')
        for idx, item in enumerate(CutArgs.yTags):
            l.log(f'Item {idx+1:03d} - y{item}')
    if CutArgs.ptScan:
        l.log(f'pT scan is [ON]:')
        for idx, item in enumerate(CutArgs.ptTags):
            l.log(f'Item {idx+1:03d} - pt{item}')

    col = f'{Args.title}.coll'

    if os.path.exists(col):
        l.log(f'Already have {col} now removing it.')
        os.system(f'rm -rf {col}')
    
    os.mkdir(col)
    if CutArgs.yScan:
        for item in CutArgs.yTags:
            for vzIdx in range(CutArgs.vzBin):
                os.system(f'cp {mergeDir}/{Args.title}.y{item}.vz{vzIdx}.pDist.root {col}/')
                os.system(f'cp {runDir}/y{item}/cum.cbwc.{Args.title}.y{item}.vz{vzIdx}.root {col}/')
                os.system(f'cp {runDir}/y{item}X/cum.cbwc.{Args.title}.y{item}.vz{vzIdx}X.root {col}/')
    if CutArgs.ptScan:
        for item in CutArgs.ptTags:
            for vzIdx in range(CutArgs.vzBin):
                os.system(f'cp {mergeDir}/{Args.title}.pt{item}.vz{vzIdx}.pDist.root {col}/')
                os.system(f'cp {runDir}/pt{item}/cum.cbwc.{Args.title}.pt{item}.vz{vzIdx}.root {col}/')
                os.system(f'cp {runDir}/pt{item}X/cum.cbwc.{Args.title}.pt{item}.vz{vzIdx}X.root {col}/')
    
    if os.path.exists(f'{col}.tgz'):
        l.log(f'Already have {col}.tgz now removing it.')
        os.remove(f'{col}.tgz')
    os.system(f'tar -zcvf {col}.tgz {col}/')
    l.log(f'All done. See {col} and {col}.tgz')

# clean mode
if mode == 'clean':
    l = yLog('.clean.log')
    if len(sys.argv) != 3:
        l.log(f'Clean All: It is dangerous! This function is forbiden!')
    else:
        clcmd = sys.argv[2]
        if clcmd not in ['cfg', 'out', 'merge', 'run', 'calc']:
            raise Exception(f'Clean Mode support the following command: cfg out merge run calc. Received: {clcmd}')
        elif clcmd == 'cfg':
            files = os.listdir()
            nrm = 0
            for item in files:
                if item[-13:] == '.getTerms.cfg':
                    l.log(f'Removing: {item}')
                    os.remove(item)
                    nrm += 1
            l.log(f'Removed {nrm} generated .cfg files.')
        elif clcmd == 'out':
            l.log(f'Need safe word, please input CONFIRM and continue:')
            k = input()
            if k == 'CONFIRM':
                outDir = Args.outDir
                l.log(f'Now we are trying to clean {outDir}.')
                os.system(f'rm -rf {outDir}')
                l.log(f'Removed.')
            else:
                l.log(f'Safe word was not accepted, canceled.')
        elif clcmd == 'merge':
            l.log(f'Need safe word, please input CONFIRM and continue:')
            k = input()
            if k == 'CONFIRM':
                mergeDir = Args.mergeDir
                l.log(f'Now we are trying to clean {mergeDir}.')
                os.system(f'rm -rf {mergeDir}')
                l.log(f'Removed.')
            else:
                l.log(f'Safe word was not accepted, canceled.')
        elif clcmd in ['run', 'calc']:
            l.log(f'Need safe word, please input CONFIRM and continue:')
            k = input()
            if k == 'CONFIRM':
                runDir = Args.runDir
                l.log(f'Now we are trying to clean {runDir}.')
                os.system(f'rm -rf {runDir}')
                l.log(f'Removed.')
            else:
                l.log(f'Safe word was not accepted, canceled.')
        else:
            l.log('Nothing happend. But I don\'t think you can see this in log file.')

# report mode
if mode in ['repo', 'report']:
    l = yLog('.report.log')
    l.log('Here is the Report:')
    l.log(f'Current verion of manager: {__version__} ({__updatedTime__})')

    # get the number of jobs
    with open(Args.fileList) as f:
        flist = f.readlines()
    nFiles = len(flist)
    nFilesPerJob = Args.nFilesPerJob
    nJobs = nFiles // nFilesPerJob
    bonus = nFiles - nJobs * nFilesPerJob
    if bonus:
        nJobs += 1
    
    # show reports
    l.log(f'<======{Args.title}======>')
    
    l.log(f'====== General Information ======')
    # l.log(f'[E] Vz cut: {CutArgs.vzMin} - {CutArgs.vzMax}')
    if CutArgs.vzBin == 1:
        l.log(f'[E] Vz bins [1/1]: -{CutArgs.vzRange} - +{CutArgs.vzRange}')
    if CutArgs.vzBin == 3:
        l.log(f'[E] Vz bins [1/3]: -30 - -10')
        l.log(f'[E] Vz bins [2/3]: -10 - +10')
        l.log(f'[E] Vz bins [3/3]: +10 - +30')
    if CutArgs.vzBin == 5:
        l.log(f'[E] Vz bins [1/5]: -30 - -10')
        l.log(f'[E] Vz bins [2/5]: -10 - +10')
        l.log(f'[E] Vz bins [3/5]: +10 - +30')
        l.log(f'[E] Vz bins [4/5]: -50 - -30')
        l.log(f'[E] Vz bins [5/5]: +30 - +50')
    l.log(f'[E] Vr cut: {CutArgs.vr}')
    l.log(f'[E] Mean DCAz cut: {CutArgs.DCAz}')
    l.log(f'[E] Mean signed DCAxy cut: {CutArgs.DCAxy}')
    l.log(f'[T] pT cut: {CutArgs.ptMin} - {CutArgs.ptMax}')
    l.log(f'[T] nHitsFit cut: {CutArgs.nHitsFit}')
    l.log(f'[T] nHitsDedx cut: {CutArgs.nHitsDedx}')
    l.log(f'[T] nHitsRatio cut: {CutArgs.nHitsRatio}')
    l.log(f'[T] nSigma cut: {CutArgs.nSig}')
    l.log(f'[T] DCA cut: {CutArgs.dca}')
    l.log(f'[T] Mass square cut: {CutArgs.m2Min} - {CutArgs.m2Max}')
    if CutArgs.yScan:
        l.log(f'Rapidity scan is [ON] with {len(CutArgs.yTags)} tasks.')
        for idx, item in enumerate(zip(CutArgs.yTags, CutArgs.yMins, CutArgs.yMaxs)):
            tag, ymin, ymax = item
            l.log(f'Item {idx+1:03d} / {len(CutArgs.yTags)} - {tag}: {ymin:.2f} - {ymax:.2f}')
    if CutArgs.ptScan:
        l.log(f'pT scan is [ON] with {len(CutArgs.ptTags)} tasks.')
        for idx, item in enumerate(zip(CutArgs.ptTags, CutArgs.ptMaxs)):
            tag, ptmax = item
            l.log(f'Item {idx+1:03d} / {len(CutArgs.ptTags)} - {tag}: {CutArgs.ptMin:.2f} - {ptmax:.2f}')
    
    if os.path.exists(Args.outDir):
        l.log(f'====== As for getTerms ===== [E]')
        l.log(f'Jobs are here: {Args.outDir}')
        l.log('The directory exists, which means we are done or doing this step.')
    else:
        l.log(f'====== As for getTerms ===== [D]')
        l.log(f'Jobs are here: {Args.outDir}')
        l.log('The directory does not exist, which means it has not got started or is removed already.')
    l.log(f'File list is: {Args.fileList} ({nFiles} files).')
    l.log(f'{nJobs} jobs are dispatched for processing {nFilesPerJob} files.')
    if bonus:
        l.log(f'Among them, there is a bonus job which will process {bonus} files.')
    else:
        l.log(f'No bonus job for this time.')
    l.log(f'The TPC efficiency path is: {Args.tpc_eff_path}')
    l.log(f'The TOF efficiency path is: {Args.tof_eff_path}')
    l.log(f'The PID efficiency path is: {Args.pid_eff_path}')
    l.log(f'Maybe we are changing nSigma for systematic uncertainty calculations, the tag is: {Args.nSigmaTag}')

    if os.path.exists(Args.mergeDir):
        l.log(f'====== As for merge ====== [E]')
        l.log(f'Jobs are here: {Args.mergeDir}')
        l.log('The directory exists, which means we are done or doing this step.')
    else:
        l.log(f'====== As for merge ====== [D]')
        l.log(f'Jobs are here: {Args.mergeDir}')
        l.log('The directory does not exist, which means it has not got started or is removed already.')
    
    if os.path.exists(Args.runDir):
        l.log(f'====== As for cumulant calculation ====== [E]')
        l.log(f'Jobs are here: {Args.runDir}')
        l.log('The directory exists, which means we are done or doing this step.')
    else:
        l.log(f'====== As for cumulant calculation ====== [D]')
        l.log(f'Jobs are here: {Args.runDir}')
        l.log('The directory does not exist, which means it has not got started or is removed already.')
    l.log(f'The executable file: {Args.calc_exec}')
    
    l.log('This is the end of report.')
