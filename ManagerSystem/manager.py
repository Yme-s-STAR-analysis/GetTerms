r'''
    
    Cumulant Calculation Manage System
    Author: Yige HUANG

    Latest Revision v7.0 (29.07.2024) - Yige Huang

    1. At present, cent_edge.txt, Npart.txt and w8.txt will be generated from parameters given in conf.py
    
    2. Inspired by other submitting system, manager system is upgraded and can save more time

        Limited by the condor system, now one has to submit s and then submit b

    3. Merge part is redesigned

        2 iterations are needed to save more time

    4. Multi-Vz bin is cancelled, only 1 Vz range will be used 

    v6.0 (26.03.2024) - Yige Huang

    1. RefMult3 is not a must, so the behavior of manager system changes accordingly

    2. resubmit returns, call it with submit mode and option 'r'

        usage: 1) python3 manager.py submit r 1,2,4 -> resubmit job id 1, 2 and 4

        usage: 2) python3 manager.py submit r -> read 'resubmit.id.txt' and resubmit job ids in it
    
    v5.0 (03.06.2024) - Yige Huang

    1. Only one log file will make use

    2. duoCBWC is removed

    3. Reweight parameters are necessary now
    
    Revision v4.3 (27.4.2024) - Yige Huang

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

__version__ = '7.0'
__updatedTime__ = '29.07.2024'

l = yLog('.ManagerSystem.log')

modeList = ['submit', 'merge', 'calculate', 'collect', 'clean', 'report']
abbrMap = {
    'sub': 'submit',
    'mer': 'merge',
    'run': 'calculate',
    'calc': 'calculate',
    'col': 'collect',
    'coll': 'collect',
    'cla': 'clean',
    'repo': 'report'
}
mode = sys.argv[1]
mode = abbrMap[mode] if mode in abbrMap else mode
assert(mode in modeList)

if mode not in ['clean', 'report']:
    if CutArgs.yScan:
        l.log(f'Rapidity scan is [ON] with {len(CutArgs.yRange)} tasks.')
        l.log(f'During rapidity scan, pT range will be [{CutArgs.ptMin}, {CutArgs.ptMax}].')
        for i, item in enumerate(CutArgs.yRange):
            l.log(f'\t[{i+1:02d}] {item} {CutArgs.yRange[item][0]} -> {CutArgs.yRange[item][1]} (mode {CutArgs.yRange[item][2]}) Vz: {CutArgs.yRange[item][3]} -> {CutArgs.yRange[item][4]}')
    else:
        l.log(f'Rapidity scan is [OFF].')
    if CutArgs.ptScan:
        l.log(f'pT scan is [ON] with {len(CutArgs.pTRange)} jobs.')
        l.log(f'During pT scan, y range will be [{CutArgs.yMin}, {CutArgs.yMax}].')
        for i, item in enumerate(CutArgs.pTRange):
            l.log(f'\t[{i+1:02d}] {item} {CutArgs.pTRange[item][0]} -> {CutArgs.pTRange[item][1]} Vz: {CutArgs.pTRange[item][2]} -> {CutArgs.pTRange[item][3]}')
    else:
        l.log(f'pT scan is [OFF].')
    if Args.ref3:
        l.log(f'RefMult3 is [ON].')
    else:
        l.log(f'RefMult3 is [OFF].')

with open(Args.fileList) as f:
    flist = f.readlines()
nFiles = len(flist)
nFilesPerJob = Args.nFilesPerJob
nJobs = nFiles // nFilesPerJob
bonus = nFiles - nJobs * nFilesPerJob
msDir = f'{Args.targetDir}/ManagerSystem'

# submit mode
if mode == 'submit':
    if len(sys.argv) != 3:
        raise Exception(f'Submit mode must accept 3 arguments but got {len(sys.argv)}')
    else:
        sMode = sys.argv[2]
        assert(sMode in ['s', 'b', 'r']) # this r: read resubmit.id.txt and resubmit
        if sMode == 's':
            l.log('Simulation mode, only generate sub-folders, you can submit the jobs with option [b].')
        if sMode == 'b':
            l.log('Submit jobs with pre-generated sub-folders.')
        if sMode == 'r':
            l.log('Resubmit jobs from "resubmit.id.txt"')
            if not os.path.exists('resubmit.id.txt'):
                raise Exception(f'[ERROR] Cannot open resubmit.id.txt!')
            
    outDir = Args.outDir
    if sMode == 'r':
        rids = open('resubmit.id.txt').readlines()
        rids = [item.strip() for item in rids]
        rids = [item for item in rids if item != '']
        l.log(f'{len(rids)} jobs will be resubmitted.')
        for idx, line in enumerate(rids):
            rScanTag, rJobIdx  = line.split(' ') # must splited by one space
            l.log(f'[{idx+1}] - {Args.title} {rScanTag} job{rJobIdx}')
            os.system(f'cd {outDir}/job{rJobIdx} && condor_submit {Args.title}.{rJobIdx}.{rScanTag}.getTerms.job')
        l.log('Done.')
    else:
        l.log('Now preparing Job Directory and File Lists. May take few seconds.')
        if not os.path.exists(outDir):
            os.mkdir(outDir)
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
        l.log(f'{Args.ref3=}')
        l.log(f'{nFiles} files in total, {nJobs} regular jobs with {nFilesPerJob} files to handle.')
        if bonus:
            l.log(f'Bonus job will manage {bonus} jobs.')

    if sMode == 's':
        # step 1: prepare file lists
        l.log('Now generating file lists for sub-jobs')
        if os.path.exists(f'{msDir}'):
            os.system(f'rm -rf {msDir}')
        os.mkdir(f'{msDir}')
        for i in range(nJobs):
            with open(f'{msDir}/{i}.list', 'w') as f:
                for line in range(i * nFilesPerJob, (i+1) * nFilesPerJob):
                    f.write(flist[line])
        if bonus:
            with open(f'{msDir}/{nJobs}.list', 'w') as f:
                for line in range(nJobs * nFilesPerJob, nFiles):
                    f.write(flist[line])

        # step 2: prepare submitting scripts
        l.log('Now preparing submitting scripts')
        if bonus:
            nJobs += 1
        # TASK_TAG will ba changed when submit the jobs
        # on current stage, general parameters are given
        getTermsShellFile = f'{msDir}/getTerms.sh'
        os.system(f'cp getTerms.sh getTermsShellFile')
        os.system(f'sed -i "s|TPC_PATH|{Args.tpc_eff_path}|g" {getTermsShellFile}')
        os.system(f'sed -i "s|TOF_PATH|{Args.tof_eff_path}|g" {getTermsShellFile}')
        os.system(f'sed -i "s|PID_PATH|{Args.pid_eff_path}|g" {getTermsShellFile}')
        os.system(f'sed -i "s|NSIG_TAG|{Args.nSigmaTag}|g" {getTermsShellFile}')
        os.system(f'sed -i "s|EFF_FAC_PRO|{Args.eff_fac_pro}|g" {getTermsShellFile}')
        os.system(f'sed -i "s|EFF_FAC_PBAR|{Args.eff_fac_pbar}|g" {getTermsShellFile}')

        # step 3: prepare cfg files
        l.log('Now preparing cfg files')
        if CutArgs.yScan:
            nScan_y = len(CutArgs.yRange)
            l.log(f'Rapidity scan is [ON], task list:')
            for i, item in enumerate(CutArgs.yRange):
                l.log(f'[{i:02d} / {nScan_y:02d}] - {item}: {CutArgs.yRange[item][0]} -> {CutArgs.yRange[item][1]}, (mode {CutArgs.yRange[item][2]}) Vz range: {CutArgs.yRange[item][3]} -> {CutArgs.yRange[item][4]} cm')
                with open(f'{msDir}/{Args.title}.y{item}.getTerms.cfg', 'w') as f:
                    f.write('VARLIST\n')
                    f.write(f'VZ\t{CutArgs.yRange[item][3]}\t{CutArgs.yRange[item][4]}\n')
                    f.write(f'PT\t{CutArgs.ptMin}\t{CutArgs.ptMax}\n')
                    f.write(f'YP\t{CutArgs.yRange[item][0]}\t{CutArgs.yRange[item][1]}\n')
                    f.write(f'NHITSFIT\t{CutArgs.nHitsFit}\n')
                    f.write(f'NSIG\t{CutArgs.nSig}\n')
                    f.write(f'DCA\t{CutArgs.dca}\n')
                    f.write(f'MASS2\t{CutArgs.m2Min}\t{CutArgs.m2Max}\n')
                    f.write(f'RMODE\t{CutArgs.yRange[item][2]}\n')
                    f.write(f'END')
        if CutArgs.ptScan:
            nScan_pt = len(CutArgs.pTRange)
            l.log(f'pT scan is [ON], task list:')
            for i, item in enumerate(CutArgs.pTRange):
                l.log(f'[{i:02d} / {nScan_pt:02d}] - {item}: {CutArgs.pTRange[item][0]} -> {CutArgs.pTRange[item][1]} Vz range: {CutArgs.pTRange[item][2]} -> {CutArgs.pTRange[item][3]} cm')
                with open(f'{msDir}/{Args.title}.pt{item}.getTerms.cfg', 'w') as f:
                    f.write('VARLIST\n')
                    f.write(f'VZ\t{CutArgs.pTRange[item][2]}\t{CutArgs.pTRange[item][3]}\n')
                    f.write(f'PT\t{CutArgs.pTRange[item][0]}\t{CutArgs.pTRange[item][1]}\n')
                    f.write(f'YP\t{CutArgs.yMin}\t{CutArgs.yMax}\n')
                    f.write(f'NHITSFIT\t{CutArgs.nHitsFit}\n')
                    f.write(f'NSIG\t{CutArgs.nSig}\n')
                    f.write(f'DCA\t{CutArgs.dca}\n')
                    f.write(f'MASS2\t{CutArgs.m2Min}\t{CutArgs.m2Max}\n')
                    f.write(f'RMODE\t{CutArgs.yMode}\n')
                    f.write(f'END')

        
        # step 4: prepare symlink
        l.log('Now preparing symlink to the executable')
        os.symlink(f'{os.getcwd()}/getTerms', f'{msDir}/getTerms')

        # step 5: prepare job files
        l.log('Now preparing job files')
        os.system(f'cp getTerms.job {msDir}/getTerms.job')

        # step 6: prepare text files
        l.log('Now preparing text files')
        with open(f'{msDir}/cent_edge.txt', 'w') as f:
            for idx, item in enumerate(Args.cent_edge):
                f.write(f'{item}')
                if idx != len(Args.cent_edge) -1:
                    f.write('\n')
        with open(f'{msDir}/cent_edgeX.txt', 'w') as f:
            for idx, item in enumerate(Args.cent_edgeX):
                f.write(f'{item}')
                if idx != len(Args.cent_edgeX) -1:
                    f.write('\n')
        with open(f'{msDir}/w8.txt', 'w') as f:
            for idx, item in enumerate(Args.w8):
                f.write(f'{item}')
                if idx != len(Args.w8) -1:
                    f.write('\n')
        with open(f'{msDir}/w8X.txt', 'w') as f:
            for idx, item in enumerate(Args.w8X):
                f.write(f'{item}')
                if idx != len(Args.w8X) -1:
                    f.write('\n')
        with open(f'{msDir}/Npart.txt', 'w') as f:
            for idx, item in enumerate(Args.Npart):
                f.write(f'{item}')
                if idx != len(Args.Npart) -1:
                    f.write('\n')
        with open(f'{msDir}/NpartX.txt', 'w') as f:
            for idx, item in enumerate(Args.NpartX):
                f.write(f'{item}')
                if idx != len(Args.NpartX) -1:
                    f.write('\n')

        l.log('Now deploying')
        os.system(f'cp conf.py {msDir}/conf.py')
        os.system(f'cp deploy.py {msDir}/deploy.py')
        os.system(f'cp deploy.job {msDir}/deploy.job')
        os.system(f'cd {msDir} && condor_submit deploy.job')
        l.log('Done.')

    if sMode == 'b':
        for i in range(nJobs):
            if CutArgs.yScan:
                for item in CutArgs.yRange:
                    os.system(f'cd {outDir}/job{i} && condor_submit {Args.title}.{i}.y{item}.getTerms.job')
            if CutArgs.ptScan:
                for item in CutArgs.pTRange:
                    os.system(f'cd {outDir}/job{i} && condor_submit {Args.title}.{i}.pt{item}.getTerms.job')
        l.log('Done.')

# merge mode
if mode == 'merge':
    outDir = Args.outDir
    mergeDir = Args.mergeDir

    mIter = 0
    if len(sys.argv) != 3:
        raise Exception(f'Merge mode must accept 2 arguments but got {len(sys.argv)}')
    else:
        mIter = int(sys.argv[2])
        assert(mIter >= 1)
        if mIter == 1:
            l.log('First iteration of merging, will merge raw outputs from previous stage')
        else:
            l.log(f'Additional iteration of merging ({mIter}), will merge merged files from previous iteration ({mIter-1})')

    if not os.path.exists(outDir):
        raise Exception(f'[ERROR] {outDir=} which does not exist.')

    if not os.path.exists(mergeDir):
        os.mkdir(mergeDir)

    if not os.path.exists(f'{mergeDir}/Iter{mIter}'):
        os.mkdir(f'{mergeDir}/Iter{mIter}')

    l.log('Here are the root files to be merged:')
    if CutArgs.yScan:
        l.log('For rapidity scan:')
        for idx, item in enumerate(CutArgs.yRange):
            l.log(f'Item {idx+1:02d}: y{item}')
    if CutArgs.ptScan:
        l.log('For pT scan:')
        for idx, item in enumerate(CutArgs.pTRange):
            l.log(f'Item {idx+1:02d}: pt{item}')
    
    if Args.ref3:
        l.log('RefMult3 and RefMult3X results will be merged respectively.')
    else:
        l.log('Only RefMult3X results will be merged.')
    
    if mIter == 1: # first iteration
        mFilesPerJob = 15
        mJobs = nJobs // mFilesPerJob
        mBonus = nJobs - mJobs * mFilesPerJob

        for iJob in range(mJobs):
            cJobDir = f'{mergeDir}/Iter{mIter}/job{iJob}'
            if os.path.exists(f'{cJobDir}'):
                os.system(f'rm -rf {cJobDir}')
            os.mkdir(f'{cJobDir}')
            os.system(f'cp merge.py {cJobDir}/merge.py')

            if CutArgs.yScan:
                for item in CutArgs.yRange:
                    # Refmult3 mTerms
                    if Args.ref3:
                        cJobFile = f'merge.y{item}.job'
                        # prepare list
                        with open(f'{cJobDir}/y{item}.{iJob}.list', 'w') as f:
                            for iFile in range(mFilesPerJob):
                                f.write(f'{outDir}/job{iFile+iJob*mFilesPerJob}/{Args.title}.y{item}.root\n')
                        # change configuration
                        os.system(f'cp merge.job {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|TASKNAME|{Args.title}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|SCANNAME|y{item}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|ITERID|{mIter}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|MERGEID|{iJob}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|FLIST|{cJobDir}/y{item}.{iJob}.list|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|TDIR|{cJobDir}|g" {cJobDir}/{cJobFile}')
                        # submit
                        l.log(f'Current task: y{item} Iteration-{mIter} Job-{iJob} RefMult3 mTerms')
                        os.system(f'cd {cJobDir} && condor_submit {cJobDir}/{cJobFile}')
                    # Refmult3X mTerms
                    if True:
                        cJobFile = f'merge.y{item}X.job'
                        # prepare list
                        with open(f'{cJobDir}/y{item}X.{iJob}.list', 'w') as f:
                            for iFile in range(mFilesPerJob):
                                f.write(f'{outDir}/job{iFile+iJob*mFilesPerJob}/{Args.title}.y{item}X.root\n')
                        # change configuration
                        os.system(f'cp merge.job {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|TASKNAME|{Args.title}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|SCANNAME|y{item}X|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|ITERID|{mIter}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|MERGEID|{iJob}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|FLIST|{cJobDir}/y{item}X.{iJob}.list|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|TDIR|{cJobDir}|g" {cJobDir}/{cJobFile}')
                        # submit
                        l.log(f'Current task: y{item} Iteration-{mIter} Job-{iJob} RefMult3X mTerms')
                        os.system(f'cd {cJobDir} && condor_submit {cJobDir}/{cJobFile}')
                    # pDist
                    if True:
                        cJobFile = f'merge.y{item}.pDist.job'
                        # prepare list
                        with open(f'{cJobDir}/y{item}.pDist.{iJob}.list', 'w') as f:
                            for iFile in range(mFilesPerJob):
                                f.write(f'{outDir}/job{iFile+iJob*mFilesPerJob}/{Args.title}.y{item}.pDist.root\n')
                        # change configuration
                        os.system(f'cp merge.job {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|TASKNAME|{Args.title}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|SCANNAME|y{item}.pDist|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|ITERID|{mIter}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|MERGEID|{iJob}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|FLIST|{cJobDir}/y{item}.pDist.{iJob}.list|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|TDIR|{cJobDir}|g" {cJobDir}/{cJobFile}')
                        # submit
                        l.log(f'Current task: y{item} Iteration-{mIter} Job-{iJob} pDist')
                        os.system(f'cd {cJobDir} && condor_submit {cJobDir}/{cJobFile}')
            if CutArgs.ptScan:
                for item in CutArgs.pTRange:
                    # Refmult3 mTerms
                    if Args.ref3:
                        cJobFile = f'merge.pt{item}.job'
                        # prepare list
                        with open(f'{cJobDir}/pt{item}.{iJob}.list', 'w') as f:
                            for iFile in range(mFilesPerJob):
                                f.write(f'{outDir}/job{iFile+iJob*mFilesPerJob}/{Args.title}.pt{item}.root\n')
                        # change configuration
                        os.system(f'cp merge.job {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|TASKNAME|{Args.title}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|SCANNAME|pt{item}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|ITERID|{mIter}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|MERGEID|{iJob}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|FLIST|{cJobDir}/pt{item}.{iJob}.list|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|TDIR|{cJobDir}|g" {cJobDir}/{cJobFile}')
                        # submit
                        l.log(f'Current task: pt{item} Iteration-{mIter} Job-{iJob} RefMult3 mTerms')
                        os.system(f'cd {cJobDir} && condor_submit {cJobDir}/{cJobFile}')
                    # Refmult3X mTerms
                    if True:
                        cJobFile = f'merge.pt{item}X.job'
                        # prepare list
                        with open(f'{cJobDir}/pt{item}X.{iJob}.list', 'w') as f:
                            for iFile in range(mFilesPerJob):
                                f.write(f'{outDir}/job{iFile+iJob*mFilesPerJob}/{Args.title}.pt{item}X.root\n')
                        # change configuration
                        os.system(f'cp merge.job {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|TASKNAME|{Args.title}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|SCANNAME|pt{item}X|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|ITERID|{mIter}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|MERGEID|{iJob}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|FLIST|{cJobDir}/pt{item}X.{iJob}.list|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|TDIR|{cJobDir}|g" {cJobDir}/{cJobFile}')
                        # submit
                        l.log(f'Current task: pt{item} Iteration-{mIter} Job-{iJob} RefMult3X mTerms')
                        os.system(f'cd {cJobDir} && condor_submit {cJobDir}/{cJobFile}')
                    # pDist
                    if True:
                        cJobFile = f'merge.pt{item}.pDist.job'
                        # prepare list
                        with open(f'{cJobDir}/pt{item}.pDist.{iJob}.list', 'w') as f:
                            for iFile in range(mFilesPerJob):
                                f.write(f'{outDir}/job{iFile+iJob*mFilesPerJob}/{Args.title}.pt{item}.pDist.root\n')
                        # change configuration
                        os.system(f'cp merge.job {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|TASKNAME|{Args.title}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|SCANNAME|pt{item}.pDist|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|ITERID|{mIter}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|MERGEID|{iJob}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|FLIST|{cJobDir}/pt{item}.pDist.{iJob}.list|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|TDIR|{cJobDir}|g" {cJobDir}/{cJobFile}')
                        # submit
                        l.log(f'Current task: pt{item} Iteration-{mIter} Job-{iJob} pDist')
                        os.system(f'cd {cJobDir} && condor_submit {cJobDir}/{cJobFile}')
        
        if mBonus > 0:
            cJobDir = f'{mergeDir}/Iter{mIter}/job{mJobs}'
            if os.path.exists(f'{cJobDir}'):
                os.system(f'rm -rf {cJobDir}')
            os.mkdir(f'{cJobDir}')
            os.system(f'cp merge.py {cJobDir}/merge.py')
            os.system(f'cp yLog.py {cJobDir}/yLog.py')
            if CutArgs.yScan:
                for item in CutArgs.yRange:
                    # Refmult3 mTerms
                    if Args.ref3:
                        cJobFile = f'merge.y{item}.job'
                        # prepare list
                        with open(f'{cJobDir}/y{item}.{mJobs}.list', 'w') as f:
                            for iFile in range(mBonus):
                                f.write(f'{outDir}/job{iFile+mJobs*mFilesPerJob}/{Args.title}.y{item}.root\n')
                        # change configuration
                        os.system(f'cp merge.job {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|TASKNAME|{Args.title}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|SCANNAME|y{item}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|ITERID|{mIter}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|MERGEID|{mJobs}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|FLIST|{cJobDir}/y{item}.{mJobs}.list|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|TDIR|{cJobDir}|g" {cJobDir}/{cJobFile}')
                        # submit
                        l.log(f'Current task: y{item} Iteration-{mIter} Job-{mJobs} RefMult3 mTerms')
                        os.system(f'cd {cJobDir} && condor_submit {cJobDir}/{cJobFile}')
                    # Refmult3X mTerms
                    if True:
                        cJobFile = f'merge.y{item}X.job'
                        # prepare list
                        with open(f'{cJobDir}/y{item}X.{mJobs}.list', 'w') as f:
                            for iFile in range(mBonus):
                                f.write(f'{outDir}/job{iFile+mJobs*mFilesPerJob}/{Args.title}.y{item}X.root\n')
                        # change configuration
                        os.system(f'cp merge.job {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|TASKNAME|{Args.title}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|SCANNAME|y{item}X|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|ITERID|{mIter}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|MERGEID|{mJobs}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|FLIST|{cJobDir}/y{item}X.{mJobs}.list|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|TDIR|{cJobDir}|g" {cJobDir}/{cJobFile}')
                        # submit
                        l.log(f'Current task: y{item} Iteration-{mIter} Job-{mJobs} RefMult3X mTerms')
                        os.system(f'cd {cJobDir} && condor_submit {cJobDir}/{cJobFile}')
                    # pDist
                    if True:
                        cJobFile = f'merge.y{item}.pDist.job'
                        # prepare list
                        with open(f'{cJobDir}/y{item}.pDist.{mJobs}.list', 'w') as f:
                            for iFile in range(mBonus):
                                f.write(f'{outDir}/job{iFile+mJobs*mFilesPerJob}/{Args.title}.y{item}.pDist.root\n')
                        # change configuration
                        os.system(f'cp merge.job {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|TASKNAME|{Args.title}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|SCANNAME|y{item}.pDist|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|ITERID|{mIter}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|MERGEID|{mJobs}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|FLIST|{cJobDir}/y{item}.pDist.{mJobs}.list|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|TDIR|{cJobDir}|g" {cJobDir}/{cJobFile}')
                        # submit
                        l.log(f'Current task: y{item} Iteration-{mIter} Job-{mJobs} pDist')
                        os.system(f'cd {cJobDir} && condor_submit {cJobDir}/{cJobFile}')   
            if CutArgs.ptScan:
                for item in CutArgs.pTRange:
                    # Refmult3 mTerms
                    if Args.ref3:
                        cJobFile = f'merge.pt{item}.job'
                        # prepare list
                        with open(f'{cJobDir}/pt{item}.{mJobs}.list', 'w') as f:
                            for iFile in range(mBonus):
                                f.write(f'{outDir}/job{iFile+mJobs*mFilesPerJob}/{Args.title}.pt{item}.root\n')
                        # change configuration
                        os.system(f'cp merge.job {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|TASKNAME|{Args.title}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|SCANNAME|pt{item}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|ITERID|{mIter}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|MERGEID|{mJobs}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|FLIST|{cJobDir}/pt{item}.{mJobs}.list|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|TDIR|{cJobDir}|g" {cJobDir}/{cJobFile}')
                        # submit
                        l.log(f'Current task: pt{item} Iteration-{mIter} Job-{mJobs} RefMult3 mTerms')
                        os.system(f'cd {cJobDir} && condor_submit {cJobDir}/{cJobFile}')
                    # Refmult3X mTerms
                    if True:
                        cJobFile = f'merge.pt{item}X.job'
                        # prepare list
                        with open(f'{cJobDir}/pt{item}X.{mJobs}.list', 'w') as f:
                            for iFile in range(mBonus):
                                f.write(f'{outDir}/job{iFile+mJobs*mFilesPerJob}/{Args.title}.pt{item}X.root\n')
                        # change configuration
                        os.system(f'cp merge.job {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|TASKNAME|{Args.title}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|SCANNAME|pt{item}X|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|ITERID|{mIter}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|MERGEID|{mJobs}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|FLIST|{cJobDir}/pt{item}X.{mJobs}.list|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|TDIR|{cJobDir}|g" {cJobDir}/{cJobFile}')
                        # submit
                        l.log(f'Current task: pt{item} Iteration-{mIter} Job-{mJobs} RefMult3X mTerms')
                        os.system(f'cd {cJobDir} && condor_submit {cJobDir}/{cJobFile}')
                    # pDist
                    if True:
                        cJobFile = f'merge.pt{item}.pDist.job'
                        # prepare list
                        with open(f'{cJobDir}/pt{item}.pDist.{mJobs}.list', 'w') as f:
                            for iFile in range(mBonus):
                                f.write(f'{outDir}/job{iFile+mJobs*mFilesPerJob}/{Args.title}.pt{item}.pDist.root\n')
                        # change configuration
                        os.system(f'cp merge.job {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|TASKNAME|{Args.title}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|SCANNAME|pt{item}.pDist|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|ITERID|{mIter}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|MERGEID|{mJobs}|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|FLIST|{cJobDir}/pt{item}.pDist.{mJobs}.list|g" {cJobDir}/{cJobFile}')
                        os.system(f'sed -i "s|TDIR|{cJobDir}|g" {cJobDir}/{cJobFile}')
                        # submit
                        l.log(f'Current task: pt{item} Iteration-{mIter} Job-{mJobs} pDist')
                        os.system(f'cd {cJobDir} && condor_submit {cJobDir}/{cJobFile}')
    elif mIter == 2: # in principle, we only need at most 2 times
        lastIterPath = f'{mergeDir}/Iter{mIter-1}'
        lastIterJobs = os.listdir(lastIterPath)
        lastIterJobs = [item for item in lastIterJobs if item.startswith('job')]
        mJobs = len(lastIterJobs)
        cJobDir = f'{mergeDir}/Iter{mIter}'
        os.system(f'cp merge.py {cJobDir}/merge.py')
        os.system(f'cp yLog.py {cJobDir}/yLog.py')

        if CutArgs.yScan:
            for item in CutArgs.yRange:
                # Refmult3 mTerms
                if Args.ref3:
                    cJobFile = f'merge.y{item}.job'
                    # prepare list
                    with open(f'{cJobDir}/y{item}.list', 'w') as f:
                        for iFile in range(mJobs):
                            f.write(f'{mergeDir}/Iter{mIter-1}/job{iFile}/{Args.title}.y{item}.root\n')
                    # change configuration
                    os.system(f'cp merge.job {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|TASKNAME|{Args.title}|g" {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|SCANNAME|y{item}|g" {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|ITERID|{mIter}|g" {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|MERGEID|tot|g" {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|FLIST|{cJobDir}/y{item}.list|g" {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|TDIR|{cJobDir}|g" {cJobDir}/{cJobFile}')
                    # submit
                    l.log(f'Current task: y{item} Iteration-{mIter} RefMult3 mTerms')
                    os.system(f'cd {cJobDir} && condor_submit {cJobDir}/{cJobFile}')
                # Refmult3X mTerms
                if True:
                    cJobFile = f'merge.y{item}X.job'
                    # prepare list
                    with open(f'{cJobDir}/y{item}X.list', 'w') as f:
                        for iFile in range(mJobs):
                            f.write(f'{mergeDir}/Iter{mIter-1}/job{iFile}/{Args.title}.y{item}X.root\n')
                    # change configuration
                    os.system(f'cp merge.job {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|TASKNAME|{Args.title}|g" {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|SCANNAME|y{item}X|g" {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|ITERID|{mIter}|g" {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|MERGEID|tot|g" {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|FLIST|{cJobDir}/y{item}X.list|g" {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|TDIR|{cJobDir}|g" {cJobDir}/{cJobFile}')
                    # submit
                    l.log(f'Current task: y{item} Iteration-{mIter} RefMult3X mTerms')
                    os.system(f'cd {cJobDir} && condor_submit {cJobDir}/{cJobFile}')
                # pDist
                if True:
                    cJobFile = f'merge.y{item}.pDist.job'
                    # prepare list
                    with open(f'{cJobDir}/y{item}.pDist.list', 'w') as f:
                        for iFile in range(mJobs):
                            f.write(f'{mergeDir}/Iter{mIter-1}/job{iFile}/{Args.title}.y{item}.pDist.root\n')
                    # change configuration
                    os.system(f'cp merge.job {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|TASKNAME|{Args.title}|g" {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|SCANNAME|y{item}.pDist|g" {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|ITERID|{mIter}|g" {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|MERGEID|tot|g" {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|FLIST|{cJobDir}/y{item}.pDist.list|g" {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|TDIR|{cJobDir}|g" {cJobDir}/{cJobFile}')
                    # submit
                    l.log(f'Current task: y{item} Iteration-{mIter} pDist')
                    os.system(f'cd {cJobDir} && condor_submit {cJobDir}/{cJobFile}')
        if CutArgs.ptScan:
            for item in CutArgs.pTRange:
                # Refmult3 mTerms
                if Args.ref3:
                    cJobFile = f'merge.pt{item}.job'
                    # prepare list
                    with open(f'{cJobDir}/pt{item}.list', 'w') as f:
                        for iFile in range(mJobs):
                            f.write(f'{mergeDir}/Iter{mIter-1}/job{iFile}/{Args.title}.pt{item}.root\n')
                    # change configuration
                    os.system(f'cp merge.job {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|TASKNAME|{Args.title}|g" {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|SCANNAME|pt{item}|g" {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|ITERID|{mIter}|g" {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|MERGEID|tot|g" {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|FLIST|{cJobDir}/pt{item}.list|g" {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|TDIR|{cJobDir}|g" {cJobDir}/{cJobFile}')
                    # submit
                    l.log(f'Current task: pt{item} Iteration-{mIter} RefMult3 mTerms')
                    os.system(f'cd {cJobDir} && condor_submit {cJobDir}/{cJobFile}')
                # Refmult3X mTerms
                if True:
                    cJobFile = f'merge.pt{item}X.job'
                    # prepare list
                    with open(f'{cJobDir}/pt{item}X.list', 'w') as f:
                        for iFile in range(mJobs):
                            f.write(f'{mergeDir}/Iter{mIter-1}/job{iFile}/{Args.title}.pt{item}X.root\n')
                    # change configuration
                    os.system(f'cp merge.job {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|TASKNAME|{Args.title}|g" {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|SCANNAME|pt{item}X|g" {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|ITERID|{mIter}|g" {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|MERGEID|tot|g" {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|FLIST|{cJobDir}/pt{item}X.list|g" {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|TDIR|{cJobDir}|g" {cJobDir}/{cJobFile}')
                    # submit
                    l.log(f'Current task: pt{item} Iteration-{mIter} RefMult3X mTerms')
                    os.system(f'cd {cJobDir} && condor_submit {cJobDir}/{cJobFile}')
                # pDist
                if True:
                    cJobFile = f'merge.pt{item}.pDist.job'
                    # prepare list
                    with open(f'{cJobDir}/pt{item}.pDist.list', 'w') as f:
                        for iFile in range(mJobs):
                            f.write(f'{mergeDir}/Iter{mIter-1}/job{iFile}/{Args.title}.pt{item}.pDist.root\n')
                    # change configuration
                    os.system(f'cp merge.job {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|TASKNAME|{Args.title}|g" {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|SCANNAME|pt{item}.pDist|g" {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|ITERID|{mIter}|g" {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|MERGEID|tot|g" {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|FLIST|{cJobDir}/pt{item}.pDist.list|g" {cJobDir}/{cJobFile}')
                    os.system(f'sed -i "s|TDIR|{cJobDir}|g" {cJobDir}/{cJobFile}')
                    # submit
                    l.log(f'Current task: pt{item} Iteration-{mIter} pDist')
                    os.system(f'cd {cJobDir} && condor_submit {cJobDir}/{cJobFile}')
    else:
        raise Exception('As per current design, merge supports at most 2 iteration!') 

# run mode
if mode == 'calculate':
    mergeDir = f'{Args.mergeDir}/Iter2' # we only wants 2 iterations
    runDir = Args.runDir

    if not os.path.exists(mergeDir):
        raise Exception(f'[ERROR] {mergeDir=} which does not exist.')
    
    if not os.path.exists(runDir):
        os.mkdir(runDir)

    if Args.ref3:
        l.log('RefMult3 and RefMult3X results will be calculated respectively.')
    else:
        l.log('Only RefMult3X results will be calculated.')

    l.log('Here are the task names to be calculated:')
    if CutArgs.yScan:
        for idx, item in enumerate(CutArgs.yRange):
            l.log('For rapidity scan:')
            l.log(f'Item {idx+1:03d} - y{item}')
            # RefMult3
            if Args.ref3:
                cJobDir = f'{runDir}/y{item}'
                if not os.path.exists(f'{cJobDir}'):
                    os.mkdir(f'{cJobDir}')
                if not os.path.exists(f'{cJobDir}/runCumulant'):
                    os.symlink(Args.calc_exec, f'{cJobDir}/runCumulant')
                if not os.path.exists(f'{cJobDir}/cent_edge.txt'):
                    os.symlink(f'{msDir}/cent_edge.txt', f'{cJobDir}/cent_edge.txt')
                if not os.path.exists(f'{cJobDir}/Npart.txt'):
                    os.symlink(f'{msDir}/Npart.txt', f'{cJobDir}/Npart.txt')
                if not os.path.exists(f'{cJobDir}/w8.txt'):
                    os.symlink(f'{msDir}/w8.txt', f'{cJobDir}/w8.txt')
                if os.path.exists(f'{cJobDir}/{Args.title}.y{item}.root'):
                    os.remove(f'{cJobDir}/{Args.title}.y{item}.root')
                os.symlink(f'{mergeDir}/{Args.title}.y{item}.root', f'{cJobDir}/{Args.title}.y{item}.root')
                os.system(f'cp calc.sh {cJobDir}/{Args.title}.y{item}.calc.sh')
                os.system(f'cp calc.job {cJobDir}/{Args.title}.y{item}.calc.job')
                os.system(f'sed -i "s|TASKNAME|{Args.title}.y{item}|g" {cJobDir}/{Args.title}.y{item}.calc.sh')
                os.system(f'sed -i "s|SHELLNAME|{Args.title}.y{item}.calc.sh|g" {cJobDir}/{Args.title}.y{item}.calc.job')
                os.system(f'sed -i "s|TASKNAME|{Args.title}.y{item}|g" {cJobDir}/{Args.title}.y{item}.calc.job')
                os.system(f'cd {cJobDir} && condor_submit {Args.title}.y{item}.calc.job')
                l.log(f' - Current y{item} with RefMult3')
            
            # RefMult3X
            if True:
                cJobDir = f'{runDir}/y{item}X'
                if not os.path.exists(f'{cJobDir}'):
                    os.mkdir(f'{cJobDir}')
                if not os.path.exists(f'{cJobDir}/runCumulant'):
                    os.symlink(Args.calc_exec, f'{cJobDir}/runCumulant')
                if not os.path.exists(f'{cJobDir}/cent_edge.txt'):
                    os.symlink(f'{msDir}/cent_edgeX.txt', f'{cJobDir}/cent_edge.txt')
                if not os.path.exists(f'{cJobDir}/Npart.txt'):
                    os.symlink(f'{msDir}/NpartX.txt', f'{cJobDir}/Npart.txt')
                if not os.path.exists(f'{cJobDir}/w8.txt'):
                    os.symlink(f'{msDir}/w8X.txt', f'{cJobDir}/w8.txt')
                if os.path.exists(f'{cJobDir}/{Args.title}.y{item}X.root'):
                    os.remove(f'{cJobDir}/{Args.title}.y{item}X.root')
                os.symlink(f'{mergeDir}/{Args.title}.y{item}X.root', f'{cJobDir}/{Args.title}.y{item}X.root')
                os.system(f'cp calc.sh {cJobDir}/{Args.title}.y{item}X.calc.sh')
                os.system(f'cp calc.job {cJobDir}/{Args.title}.y{item}X.calc.job')
                os.system(f'sed -i "s|TASKNAME|{Args.title}.y{item}X|g" {cJobDir}/{Args.title}.y{item}X.calc.sh')
                os.system(f'sed -i "s|SHELLNAME|{Args.title}.y{item}X.calc.sh|g" {cJobDir}/{Args.title}.y{item}X.calc.job')
                os.system(f'sed -i "s|TASKNAME|{Args.title}.y{item}X|g" {cJobDir}/{Args.title}.y{item}X.calc.job')
                os.system(f'cd {cJobDir} && condor_submit {Args.title}.y{item}X.calc.job')
                l.log(f' - Current y{item} with RefMult3X')

    if CutArgs.ptScan:
        for idx, item in enumerate(CutArgs.pTRange):
            l.log('For pT scan:')
            l.log(f'Item {idx+1:03d} - pt{item}')
            # RefMult3
            if Args.ref3:
                cJobDir = f'{runDir}/pt{item}'
                if not os.path.exists(f'{cJobDir}'):
                    os.mkdir(f'{cJobDir}')
                if not os.path.exists(f'{cJobDir}/runCumulant'):
                    os.symlink(Args.calc_exec, f'{cJobDir}/runCumulant')
                if not os.path.exists(f'{cJobDir}/cent_edge.txt'):
                    os.symlink(f'{msDir}/cent_edge.txt', f'{cJobDir}/cent_edge.txt')
                if not os.path.exists(f'{cJobDir}/Npart.txt'):
                    os.symlink(f'{msDir}/Npart.txt', f'{cJobDir}/Npart.txt')
                if not os.path.exists(f'{cJobDir}/w8.txt'):
                    os.symlink(f'{msDir}/w8.txt', f'{cJobDir}/w8.txt')
                if os.path.exists(f'{cJobDir}/{Args.title}.pt{item}.root'):
                    os.remove(f'{cJobDir}/{Args.title}.pt{item}.root')
                os.symlink(f'{mergeDir}/{Args.title}.pt{item}.root', f'{cJobDir}/{Args.title}.pt{item}.root')
                os.system(f'cp calc.sh {cJobDir}/{Args.title}.pt{item}.calc.sh')
                os.system(f'cp calc.job {cJobDir}/{Args.title}.pt{item}.calc.job')
                os.system(f'sed -i "s|TASKNAME|{Args.title}.pt{item}|g" {cJobDir}/{Args.title}.pt{item}.calc.sh')
                os.system(f'sed -i "s|SHELLNAME|{Args.title}.pt{item}.calc.sh|g" {cJobDir}/{Args.title}.pt{item}.calc.job')
                os.system(f'sed -i "s|TASKNAME|{Args.title}.pt{item}|g" {cJobDir}/{Args.title}.pt{item}.calc.job')
                os.system(f'cd {cJobDir} && condor_submit {Args.title}.pt{item}.calc.job')
                l.log(f' - Current pt{item} with RefMult3')
            
            # RefMult3X
            if True:
                cJobDir = f'{runDir}/pt{item}X'
                if not os.path.exists(f'{cJobDir}'):
                    os.mkdir(f'{cJobDir}')
                if not os.path.exists(f'{cJobDir}/runCumulant'):
                    os.symlink(Args.calc_exec, f'{cJobDir}/runCumulant')
                if not os.path.exists(f'{cJobDir}/cent_edge.txt'):
                    os.symlink(f'{msDir}/cent_edgeX.txt', f'{cJobDir}/cent_edge.txt')
                if not os.path.exists(f'{cJobDir}/Npart.txt'):
                    os.symlink(f'{msDir}/NpartX.txt', f'{cJobDir}/Npart.txt')
                if not os.path.exists(f'{cJobDir}/w8.txt'):
                    os.symlink(f'{msDir}/w8X.txt', f'{cJobDir}/w8.txt')
                if os.path.exists(f'{cJobDir}/{Args.title}.pt{item}X.root'):
                    os.remove(f'{cJobDir}/{Args.title}.pt{item}X.root')
                os.symlink(f'{mergeDir}/{Args.title}.pt{item}X.root', f'{cJobDir}/{Args.title}.pt{item}X.root')
                os.system(f'cp calc.sh {cJobDir}/{Args.title}.pt{item}X.calc.sh')
                os.system(f'cp calc.job {cJobDir}/{Args.title}.pt{item}X.calc.job')
                os.system(f'sed -i "s|TASKNAME|{Args.title}.pt{item}X|g" {cJobDir}/{Args.title}.pt{item}X.calc.sh')
                os.system(f'sed -i "s|SHELLNAME|{Args.title}.pt{item}X.calc.sh|g" {cJobDir}/{Args.title}.pt{item}X.calc.job')
                os.system(f'sed -i "s|TASKNAME|{Args.title}.pt{item}X|g" {cJobDir}/{Args.title}.pt{item}X.calc.job')
                os.system(f'cd {cJobDir} && condor_submit {Args.title}.pt{item}X.calc.job')
                l.log(f' - Current pt{item} with RefMult3X')
        
    l.log('All submitted!')

# collect mode
if mode == 'collect':
    mergeDir = f'{Args.mergeDir}/Iter2'
    runDir = Args.runDir

    if not os.path.exists(mergeDir):
        raise Exception(f'[ERROR] {mergeDir=} which does not exist.')

    if not os.path.exists(runDir):
        raise Exception(f'[ERROR] {runDir=} which does not exist.')
    
    l.log('Here are the task names to be collected:')
    if CutArgs.yScan:
        l.log(f'Rapidity scan is [ON]:')
        for idx, item in enumerate(CutArgs.yRange):
            l.log(f'Item {idx+1:03d} - y{item}')
    if CutArgs.ptScan:
        l.log(f'pT scan is [ON]:')
        for idx, item in enumerate(CutArgs.pTRange):
            l.log(f'Item {idx+1:03d} - pt{item}')

    col = f'{Args.title}.coll'

    if os.path.exists(col):
        l.log(f'Already have {col} now removing it.')
        os.system(f'rm -rf {col}')

    if Args.ref3:
        l.log('RefMult3 and RefMult3X results will be collected.')
    else:
        l.log('Only RefMult3X results will be collected.')
    
    os.mkdir(col)
    if CutArgs.yScan:
        for item in CutArgs.yRange:
            os.system(f'cp {mergeDir}/{Args.title}.y{item}.pDist.root {col}/')
            if Args.ref3:
                os.system(f'cp {runDir}/y{item}/cum.cbwc.{Args.title}.y{item}.root {col}/')
            os.system(f'cp {runDir}/y{item}X/cum.cbwc.{Args.title}.y{item}X.root {col}/')
    if CutArgs.ptScan:
        for item in CutArgs.pTRange:
            os.system(f'cp {mergeDir}/{Args.title}.pt{item}.pDist.root {col}/')
            if Args.ref3:
                os.system(f'cp {runDir}/pt{item}/cum.cbwc.{Args.title}.pt{item}.root {col}/')
            os.system(f'cp {runDir}/pt{item}X/cum.cbwc.{Args.title}.pt{item}X.root {col}/')
    
    if os.path.exists(f'{col}.tgz'):
        l.log(f'Already have {col}.tgz now removing it.')
        os.remove(f'{col}.tgz')
    os.system(f'tar -zcvf {col}.tgz {col}/')
    l.log(f'All done. See {col} and {col}.tgz')

# clean mode
if mode == 'clean':
    if len(sys.argv) != 3:
        l.log(f'Clean All: It is dangerous! This function is forbiden!')
    else:
        clcmd = sys.argv[2]
        if clcmd not in ['out', 'merge', 'run', 'calc']:
            raise Exception(f'[ERROR] Clean Mode support the following command: out merge run calc. Received: {clcmd}')
        if clcmd == 'out':
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
if mode == 'report':
    l.log('Manager System: Task Report')
    l.log(f'Current verion of manager: {__version__} ({__updatedTime__})')
    l.log(f'Task Name: {Args.title}')
    
    l.log(f'# General Information')
    l.log(f'\tnHitsFit cut: {CutArgs.nHitsFit}')
    l.log(f'\tnSigma cut: {CutArgs.nSig}')
    l.log(f'\tDCA cut: {CutArgs.dca}')
    l.log(f'\tmass square cut: {CutArgs.m2Min} -> {CutArgs.m2Max}')
    if CutArgs.yScan:
        l.log(f'\tRapidity scan is [ON] with {len(CutArgs.yRange)} tasks.')
        l.log(f'\tDuring rapidity scan, pT range will be [{CutArgs.ptMin}, {CutArgs.ptMax}].')
        for i, item in enumerate(CutArgs.yRange):
            l.log(f'\t {i+1:02d}) {item} {CutArgs.yRange[item][0]} -> {CutArgs.yRange[item][1]} (mode {CutArgs.yRange[item][2]}) Vz: {CutArgs.yRange[item][3]} -> {CutArgs.yRange[item][4]}')
    else:
        l.log(f'\tRapidity scan is [OFF].')
    if CutArgs.ptScan:
        l.log(f'\tpT scan is [ON] with {len(CutArgs.pTRange)} jobs.')
        l.log(f'\tDuring pT scan, y range will be [{CutArgs.yMin}, {CutArgs.yMax}].')
        for i, item in enumerate(CutArgs.pTRange):
            l.log(f'\t {i+1:02d}) {item} {CutArgs.pTRange[item][0]} -> {CutArgs.pTRange[item][1]} Vz: {CutArgs.pTRange[item][2]} -> {CutArgs.pTRange[item][3]}')
    if Args.ref3:
        l.log('\tRefMult3 is [ON]')
    else:
        l.log('\tRefMult3 is [OFF]')
    
    if os.path.exists(Args.outDir):
        l.log(f'# GetTerms: [E]')
        l.log(f'\tJobs are here: {Args.outDir}')
        l.log('\tThe directory exists, which means we are done or doing this step.')
    else:
        l.log(f'# GetTerms: [D]')
        l.log(f'\tJobs are here: {Args.outDir}')
        l.log('\tThe directory does not exist, which means it has not got started or is removed already.')
    l.log(f'\tFile list is: {Args.fileList} ({nFiles} files).')
    l.log(f'\t{nJobs} jobs are dispatched for processing {nFilesPerJob} files.')
    if bonus:
        l.log(f'Among them, there is one bonus job which will process {bonus} files.')
    l.log(f'\tTPC efficiency is from: {Args.tpc_eff_path}')
    l.log(f'\tTOF efficiency is from: {Args.tof_eff_path}')
    l.log(f'\tPID efficiency is from: {Args.pid_eff_path}')
    l.log(f'\tMaybe we are changing nSigma for systematic uncertainty calculations, the tag is: {Args.nSigmaTag}')

    if os.path.exists(Args.mergeDir): # has merge folder
        if os.path.exists(f'{Args.mergeDir}/Iter1'): # has iter 1
            if os.path.exists(f'{Args.mergeDir}/Iter2'): # has iter 2
                l.log(f'# Merge: [2]')
                l.log(f'\t2-iteration jobs are here: {Args.mergeDir}/Iter2')
                l.log('\tThe directory exists, which means we are done or doing this step.')
            else : # has not iter 2
                l.log(f'# Merge: [1]')
                l.log(f'\t1-iteration jobs are here: {Args.mergeDir}/Iter1')
                l.log('\tThe directory exists, which means we are done or doing this step.')
                l.log('\tNext step might be merge iteration 2')
        else: # has not iter 1
            l.log(f'# Merge: [D]')
            l.log(f'\tJobs are here: {Args.mergeDir}')
            l.log('\tThe directory exists, but iteration folders do not exist, which means we haven\'t started it or they have been removed')
    else: # removed
        l.log(f'# Merge: [E]')
        l.log(f'\tJobs are here: {Args.mergeDir}')
        l.log('\tThe directory does not exist, which means it has not got started or is removed already.')

    if os.path.exists(Args.runDir):
        l.log(f'# Calculation: [E]')
        l.log(f'\tJobs are here: {Args.runDir}')
        l.log('\tThe directory exists, which means we are done or doing this step.')
    else:
        l.log(f'# Calculation: [D]')
        l.log(f'\tJobs are here: {Args.runDir}')
        l.log('\tThe directory does not exist, which means it has not got started or is removed already.')
    l.log(f'\tThe executable file: {Args.calc_exec}')
    l.log(f'Generated files for manger system can be found at: {Args.targetDir}/ManagerSystem')
    
    l.log('This is the end of report.')
