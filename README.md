# Quick Start

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
