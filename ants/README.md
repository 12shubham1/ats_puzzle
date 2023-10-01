# Ants**
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

<table><tr><th colspan="3" valign="top">Test Name</th><th valign="top"></th><th colspan="2" valign="top">KS D-statistic (goodness of fit)</th><th colspan="2" valign="top">Expected time (seconds) to meet</th></tr>
<tr><td valign="top">Backtrack</td><td valign="top">Diagonal</td><td valign="top">Objective</td><td valign="top">Distribution</td><td valign="top">Best fit</td><td valign="top">Lognormal</td><td valign="top">Best fit</td><td valign="top">lognormal</td></tr>
<tr><td valign="top">True</td><td valign="top">False</td><td valign="top">Meet</td><td valign="top">Lognormal</td><td valign="top">0.023</td><td valign="top">0.019</td><td valign="top">849</td><td valign="top">842</td></tr>
<tr><td valign="top">False</td><td valign="top">False</td><td valign="top">Meet</td><td valign="top">Lognormal</td><td valign="top">0.025</td><td valign="top">0.023</td><td valign="top">850</td><td valign="top">845</td></tr>
<tr><td valign="top">True</td><td valign="top">True</td><td valign="top">Meet</td><td valign="top">Lognormal</td><td valign="top">0.029</td><td valign="top">0.030</td><td valign="top">960</td><td valign="top">963</td></tr>
<tr><td valign="top">False</td><td valign="top">True</td><td valign="top">Meet</td><td valign="top">Lognormal</td><td valign="top">0026</td><td valign="top">0.029</td><td valign="top">960</td><td valign="top">960</td></tr>
<tr><td valign="top">True</td><td valign="top">False</td><td valign="top">Cross</td><td colspan="5" rowspan="2" valign="top">*Not possible for ants to meet (explained below)</td></tr>
<tr><td valign="top">False</td><td valign="top">False</td><td valign="top">Cross</td></tr>
<tr><td valign="top">True</td><td valign="top">True</td><td valign="top">Cross</td><td valign="top">Gamma</td><td valign="top">0.018</td><td valign="top">0.047</td><td valign="top">4533</td><td valign="top">5016</td></tr>
<tr><td valign="top">False</td><td valign="top">True</td><td valign="top">Cross</td><td valign="top">Beta</td><td valign="top">0.010</td><td valign="top">0.050</td><td valign="top">3684</td><td valign="top">5012</td></tr>
</table>


From the above, there are 3 variables which were compared by forcing a lognormal distribution: 

`Backtrack (bool)`, `Diagonal (bool)` and `Objective (str)`. 

The appropriateness of this was studied visually and using the Kolmogorov-Smirnov (KS) test as a measure of ‘goodness of fit’ (see table above). The visual comparison is shown below where the log of the times taken is plotted as a histogram vs the underlying normal distribution backed out from the fitted lognormal distribution. This method is appropriate for all the ‘meet’ objective tests (first four) while starts to deviate in when the objective changes to ‘cross’.

![A graph of a normal distribution

Description automatically generated](Aspose.Words.3c8af976-6436-41a7-8ce5-d5084d63587b.001.png)

Overall, this method still seems sufficiently robust to analyse the trends. This can be seen in the second chart:

![A diagram of a normal distribution

Description automatically generated](Aspose.Words.3c8af976-6436-41a7-8ce5-d5084d63587b.002.png)The shortest/quickest time to meet (on average) is when ants are only allowed to move to adjacent squares, followed closely by stopping ants from backtracking. The next significant change in pattern comes from allowing diagonal moves where we can see a higher mean but also higher standard deviation in the plots. This suggests that despite the theoretical min (4 moves) being lower, the additional moves an ant can make from any given square increases both the time taken on average to meet and variation in these times (standard deviation increases from 0.75 to 0.85). Finally, when the success criteria is changed to ‘crossing’, we can see the biggest jump in time taken and standard deviation. This intuitively also makes sense as to cross paths, they must go onto opposite colour squares despite starting on the same colour squares. This additional complexity is seen in the results.

For the case where ants can only move adjacent and they must cross (backtrack or not), they cannot meet. The logic here is simple: to cross they must end up on different colour squares and this is not possible with adjacent moves only and starting on the same colour square. 


|Variable|Backtrack|Diagonal|Meet or Cross|
| :- | :- | :- | :- |
|Impact|Low|Medium|High|
