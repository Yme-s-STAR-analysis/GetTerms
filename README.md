# GetTerms

`author: yghuang`

`version: 4.3`

## Quick Start

1. modify parameters in `conf.py` according to your requirements

2. swicth to ROOT6 and `make`

3. replace `utils/CentParams.h` with the correct one of the very data set

4. change `cent_edge.txt` and `cent_edgeX.txt`

5. run `python3 manager.py submit a` to submit jobs of get terms

    1. you can try `python3 manager.py submit s` to generate job folders and not submit jobs

    2. then use `python3 manager.py submit b` to submit jobs

6. after all the jobs are finished, try `python3 manager.py merge` to hadd them

7. switch back to ROOT5 and run `python3 manager.py calc` to calculate cumulants

8. `python3 manager.py col` to collect cumulant root file, note that, those files did not apply re-weight

9. `python3 manager.py clean [out/merge/calc]` to remove corresponding files

## Patch Note

Version: 4.3

27.04.2024 - Yige Huang

1. Quality controllder now removed unused quantities, like vr, nHitsDedx ...

2. And in StFemtoEvent and StFemtoTrack, unused quantities are also removed

3. resubmit mode is removed from manager system

4. add user's guide

Version: 4.2.2

09.04.2024 - Yige Huang

1. Quality controller will reject tracks with quantity equal to the limit:

    The EffMaker is using FindBin method to get PID effiicency, and for some particular tracks, the pt or y is exactly at the bin edge (like pt=2.0), which can pass QualityController's check, but fail to get a valid PID efficiency (=0).

    And efficiency equaling to 0 results in infinite cumulant value.

    Doing a cut in EffMaker would give an implicit hard cut and may be forgotten in the future and that's why I make this change in quality controller.

Version: 4.2.1

08.04.2024 - Yige Huang

1. Fix a bug: PID efficiency's interface in Core.cxx

Version: 4.2

08.04.2024 - Yige Huang

1. new efficiency maker class

2. new centrality tool

Version: 4.1

13.3.2024 - Yige Huang

1. Merge will skip files that does not exist to avoid failing

Version: 4.0

30.1.2024 - Yige Huang

Updates:

1. Support RefMult3X

Version: 3.5

12.1.2024 - Yige Huang

Updates:

1. 2 more rapidity bins for efficiency loader

Version: 3.4

8.1.2023 - Yige Huang

Updates:

1. New feature for manager system: find the failed jobs and resubmit them.

Version: 3.3

22.12.2023 - Yige Huang

Updates:

1. Now support pT scan as well.

Version: 3.2

15.12.2023 - Yige Huang

Updates:

1. DCAxy/z cut were applied during generating fDst, canceled in this part

2. Centrality tool are updated correspondingly

Version: 3.1

30.10.2023 - Yige Huang

Updates:

1. Updated the job name of merge and calc, which can make it easier to track the unfinished jobs.

2. Now Vz split is embedded in the scan process.
    

Version: 3.0

23.10.2023 - Yige Huang

Now, all modules under this package will share the patch.

Updates:

1. Effciciency factor can be different for protons and antiprotons. For systematic uncertainty, just use the same factor is okay. And other than that, we can do some checks (like apply additional efficiency factor for pro and pbar separately).

2. Manager system now can let the condor system show more detailed job name.
