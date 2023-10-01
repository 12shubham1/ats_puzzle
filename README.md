# ATS Puzzles

Solving ATS ants and signal processing challenge.

## **Question 1: Ants**

{Insert ants here}

### **Approach**

The approach used was as follows:

1) Run N simulations for the different input cases.

2) Fit a distribution to the sample generated for each case.

3) Estimate the time taken as the mean of the distribution that best fits.

4) Based on initial analysis, force a lognormal distribution on each sample. This allowed for a comparison of the impact of each variable in the problem: Backtrack, Diagonal and success condition (meet or cross).

### **Results**

(Note: The results below can be replicated by using seed 1 `random.seed(1)` in `main.py` or similar results can be obtained by running the code directly without forcing a seed)

For each simulation, 10,000 runs were performed, and the results are summarised below:

| Test Name |
 | KS D-statistic (goodness of fit) | Expected time (seconds) to meet |
| --- | --- | --- | --- |
| Backtrack | Diagonal | Objective | Distribution | Best fit | Lognormal | Best fit | lognormal |
| True | False | Meet | Lognormal | 0.023 | 0.019 | 849 | 842 |
| False | False | Meet | Lognormal | 0.025 | 0.023 | 850 | 845 |
| True | True | Meet | Lognormal | 0.029 | 0.030 | 960 | 963 |
| False | True | Meet | Lognormal | 0026 | 0.029 | 960 | 960 |
| True | False | Cross | \*Not possible for ants to meet (explained below) |
| False | False | Cross |
| True | True | Cross | Gamma | 0.018 | 0.047 | 4533 | 5016 |
| False | True | Cross | Beta | 0.010 | 0.050 | 3684 | 5012 |

From the above, there are 3 variables which were compared by forcing a lognormal distribution:

`Backtrack (bool)`, `Diagonal (bool)` and `Objective (str)`.

The appropriateness of this was studied visually and using the Kolmogorov-Smirnov (KS) test as a measure of 'goodness of fit' (see table above). The visual comparison is shown below where the log of the times taken is plotted as a histogram vs the underlying normal distribution backed out from the fitted lognormal distribution. This method is appropriate for all the 'meet' objective tests (first four) while starts to deviate in when the objective changes to 'cross'.

![](RackMultipart20231001-1-edxozy_html_a344d103abae8ede.png)

Overall, this method still seems sufficiently robust to analyse the trends. This can be seen in the second chart:

T ![](RackMultipart20231001-1-edxozy_html_14e05caa6d7ff57a.png) he shortest/quickest time to meet (on average) is when ants are only allowed to move to adjacent squares, followed closely by stopping ants from backtracking. The next significant change in pattern comes from allowing diagonal moves where we can see a higher mean but also higher standard deviation in the plots. This suggests that despite the theoretical min (4 moves) being lower, the additional moves an ant can make from any given square increases both the time taken on average to meet and variation in these times (standard deviation increases from 0.75 to 0.85). Finally, when the success criteria is changed to 'crossing', we can see the biggest jump in time taken and standard deviation. This intuitively also makes sense as to cross paths, they must go onto opposite colour squares despite starting on the same colour squares. This additional complexity is seen in the results.

For the case where ants can only move adjacent and they must cross (backtrack or not), they cannot meet. The logic here is simple: to cross they must end up on different colour squares and this is not possible with adjacent moves only and starting on the same colour square.

| Variable | Backtrack | Diagonal | Meet or Cross |
| --- | --- | --- | --- |
| Impact | Low | Medium | High |
