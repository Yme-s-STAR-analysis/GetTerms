import os
import sys
from yLog import yLog

taskName = sys.argv[1]
outDir = sys.argv[2]
mergeDir = sys.argv[3]

taskName = taskName + '.root'

l = yLog(f'.{taskName}.merge.log')

l.log(f'{taskName=}')
l.log(f'{outDir=}')
l.log(f'{mergeDir=}')

lists = os.listdir(outDir)
lists = [f'{outDir}/{item}/{taskName}' for item in lists]

n = len(lists)

baseFile = lists.pop(0)
l.log(f'Now hadd 1 / {n} : {baseFile}')
os.system(f'cp {baseFile} {mergeDir}/tmp.{taskName}')
for idx, item in enumerate(lists):
    l.log(f'Now hadd {idx + 2} / {n} : {item}')
    if not os.path.exists(item):
        l.log(f'{item} does not exist, skip!')
        continue
    os.system(f'hadd {mergeDir}/{taskName} {item} {mergeDir}/tmp.{taskName}')
    os.system(f'mv {mergeDir}/{taskName} {mergeDir}/tmp.{taskName}')
os.system(f'mv {mergeDir}/tmp.{taskName} {mergeDir}/{taskName}')

l.log('All done.')
