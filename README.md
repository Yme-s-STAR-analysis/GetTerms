# GetTerms

`author: yghuang`

`version: 7.7`

## Quick Start

1. modify parameters in `conf.py` according to your requirements

2. in `Source` folder, replace `utils/CentParams.h` with the correct one of the very data set

3. swicth to ROOT6 and `make`

    1. To activate utmost 4th order mode, add `FOURTH=1`

    2. To activate RefMult3, add `REFMULT3=1`

4. change `cent_edge.txt` and `cent_edgeX.txt`

5. run `python3 manager.py submit a` to submit jobs of get terms

    1. you can try `python3 manager.py submit s` to generate job folders and not submit jobs

    2. then use `python3 manager.py submit b` to submit jobs

6. after all the jobs are finished, try `python3 manager.py merge` to hadd them

7. switch back to ROOT5 and run `python3 manager.py calc` to calculate cumulants

8. `python3 manager.py col` to collect cumulant root file, note that, those files did not apply re-weight

9. `python3 manager.py clean [out/merge/calc]` to remove corresponding files

## Patch Note

Version: 7.7

04.02.2025 - Yige Huang

1. Adjust the default settings of configuration file.

2. Fix a bug: the bonus job issue.

Version: 7.6.1

27.11.2024 - Yige Huang

1. Fix a bug: when calculate number of jobs in submit (b) and merge (1) modes will miss the bonus job.

2. Text in report mode.

Version: 7.6

14.10.2024 - Yige Huang

1. The asymmetric cut affects efficiency, and now the impact (0.5) would be inside EffMaker instead of in the Core code.

Version: 7.5

06.10.2024 - Yige Huang

1. Add an additional option that alters the TOF efficiency formatting
    * Now use TH2->Interpolate(y, pt)
    * To activate this, `make INTERPOLATE=1`

Version: 7.4

16.09.2024 - Yige Huang

1. Add an additional option that only calculate up to 4th order
    * To activate this, `make FOURTH=1`

2. Similarly, at present, to activate RefMult3, please add `REFMULT3=1` when `make`

Version: 7.3

30.08.2024 - Yige Huang

1. The centrality selection is changed: from left-open and right-close to left-close and right-open

2. Removed patch notes from `Core.cxx`

Version: 7.2

27.08.2024 - Yige Huang

1. Add asymmetric cut option into the quality control

    * Corresponding cut selection can be modified in `Core.cxx`, see comment `// Make track Cut`

Version: 7.1

31.07.2024 - Yige Huang

1. Since manager system and source codes are now designed separately, the pcm files automatically generated by the compiler will no longer exist in the manager system's directory

    * This will cause problems reading external libraries

    * Manager system will link getTerms to the absolute path in source folder now to avoid this problem

Version: 7.0

29.07.2024 - Yige Huang

1. Separation of the source code and manager system

    * The get-terms part and manager system are put into 2 separate folders

    * In principle, source part only needs to be compiled once for every data set, and we only need the executable `getTerms`

    * To implete this, the traditional centrality correction tool is not a part of the source code, but replaced by a new one which reads centrality bin edge from text file

2. New design for manager system

    * Inspired by other submitting scripts (like PhQDM generating code using lustr in CBM's server, and my Glauber fit code for CBM's server), manager system can be much more easy to use (and save much more time)

    * For merge mode, a much more efficient approach is invented: files will be merged twice, and save much more time

    * There are also some minor changes in manager system, like centrality bin edge and other outside parameters are put into `conf.py`

Version: 6.0

26.06.2024 - Yige Huang

* Since we focus on RefMult3X results, calculating cumulants with RefMult3 is now an option.

1. By default, Loader of RefMult3 will not be used.

2. One can switch on it when compile: `make EXTRA_CPPFLAG=-D__REFMULT3__`

3. Manager system was changed accordingly.

Version: 5.0

03.06.2024 - Yige Huang

1. Important update: p+pbar is now taken into account, Loader class is updated

2. Remove old EffMaker

3. Optmize manager system

4. Reweight is now a part of calculation

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
