## 'Jiao Tong' Preference of Jiao Tong Undergraduates

### Topic

At weekends, SJTU undergraduates face a dilemma—they want to get refreshed in the downtown area of Shanghai, but they either have to spend a lot of time on the railway or pay a relatively high amount for taxiing. We are interested in what factors affect SJTU undergraduates' choices of transportation.

### Questions

1. Given some situations, which vary in distance, weather, time constraint, etc., will the students' choice of transportation differentiate? What is the most important among these *situational variables*? 
   - we **do not** consider the characters of students in this question.
2. For any given situation, will the students' choices differentiate due to *demographic variables* like gender, origins, grades, major, pocket money, etc.?
3. Are there any interactions among all the independent variables mentioned above? Can we build a simple model to predict students' decisions under different circumstances?

### Variables

#### Situational Variables

| **Variable**               | **Type** | **Description**                             |
| -------------------------- | -------- | ------------------------------------------- |
| Distance to destination(D) | Category | 0/1/2 - short/medium/long-distance          |
| Weather conditions(W)      | Dummy    | 0 for sunny, 1 for rainy.                   |
| Time constraint(C)         | Dummy    | 0 for time-abundant, 1 for time-constrained |


#### Demographic Variables

| **Variable** | **Type** | **Description**                                              |
| ------------ | -------- | ------------------------------------------------------------ |
| Gender       | Dummy    | 0 for female, 1 for male.                                    |
| Origin       | Category | 0 for eastern, 1 for middle, 2 for western.                  |
| Grade*       | Category | 0 for freshman, 1 for sophomore, 2 for junior, 3 for senior. |
| Major        | Category | 0 for STEM, 1 for ACEM, 2 for liberal arts and social science, 3 for medical. |
| Pocket Money       | Int (¥)  | The student's income level in Chinese Yuan.                  |

*The subjects of our study are limited to undergraduates. 

#### Response Variable

| **Variable**             | **Type**         | **Description**                                              |
| ------------------------ | ---------------- | ------------------------------------------------------------ |
| Choice of transportation | Vector of floats | Each student assigns scores to transportation options*, and then the scores are converted into a probability distribution using the SoftMax function. To use categorical variables later, we can perform `argmax` to get the students' choices. |

*Options include: 0 for bus/subway, 1 for taxi, 2 for bikes/e-bikes, 3 for walking. 

### Data Collection

Questionnaires that collect

1. Basic information, i.e. the demographic variables mentioned above.
2. Decisions. We will design some situations with different combinations of situational variables and let students assign a score to each means of transportation by adjusting rating sliders.

The original data could be found in `raw_data3.csv`.

### Methods 

#### Data Pre-process

In `Clean.ipynb`, we

1. Drop trivial columns.
2. Fill NaN with 0. If the student does not adjust the rating slider for a particular option, we assume that he/she has no preference for that option.
3. Rename the remaining columns according to **Description** in [Situational Variables](#situational-variables).
4. Transform each students' preference under each circumstance with softmax function. 
   - We will not add $e^0$ into denominators. The probability that was originally 0 remains 0 after softmax operation.
   - Since the scores are in range [0, 100], we actually calculate softmax with `score/=100`.

The cleaned data could be found in `cleaned_data.csv`.
The summary of data is coded in **Basic Description** of `Analysis.ipynb`.

#### Question 1

1. **Independence test with Pearson's $\chi^2$** - in **Pearson's $\chi^2$** of `Analysis.ipynb`
   - $H_0$: under any given situation, the proportions of the transportation options are equal. If we reject $H_0$, we can conclude there are interactions between situational variables. 
   - For each transportation option, fill in the number of people in each group who most prefer(i.e. `argmax`) that option under the group situation. The test statistic is
   $$
   \sum_{o=0}^{n_o - 1} \sum_{s}^{S} \frac{(f_{os} - e_{os})^2}{e_{os}} \sim \chi^2\Big((n_o - 1)(n_S - 1)\Big)
   \nonumber
   $$
   where $o$ denotes transportation options, $S$ is the set of all situations, $n_o = 4$, $n_S = 12$.

2. **Adjusted Marascuilo procedure with Bonferroni correction** - in **Marasuilo procedure** of `Analysis.ipynb`
   - Why adjusted? In our textbook, Marascuilo procedure is introduced to test whether concerned proportions (A or not A) belonging to three or more populations are significantly different. But here we have actually four proportions (0, 1, 2 or 3), so this procedure is a little different from the textbook version. Luckily, the procedure still works because when calculating the expected frequency, we are treating data as four proportion groups (0 or not 0, 1 or nor 1, etc.)
   - Why Bonferroni correction? We want to control the aggregate chance of committing type 1 error to 0.05.

In adjusted one, for each row (each option *o*) and column (situation *i*) we treat it as a proportion $p_{i}^o$. For the same *o*, the critical difference between the pair $(p_{i}^o,p_{j}^o) (i\neq j)$ is expressed as:
$${CV}_{ij}^o=\sqrt{\chi_{\alpha^\prime}^2}\sqrt{\frac{p_i^o(1-p_i^o)}{n_i}+\frac{p_j^o(1-p_j^o)}{n_j}}$$
If $|p_i^o-p_i^o|>{CV}_{ij}^o$, we conclude that under option *o* the difference between situation *i* and *j* is significant under the significant level $\alpha^\prime$.$\alpha^\prime$is calculated through the Bonferroni correction, dividing it by the number of comparisons:
$$\alpha^\prime=\frac{\alpha}{m},\alpha=0.05,m=C_{12}^2$$
The test was applied to *o*=(0,1,2,3) to looking into the significant discrepancy under different travel choices.

3. **T-test** - in **T-test** of `Analysis.ipynb`
   - We tried to figure out the relative importance rank of situational variables. We assumed that if one variable(A) is more important than another(B) for an option, then with controlled A, changes to B should not significantly influence the probability distribution of that option, which can be, to some extent, showed by **mean** softmax probabilities. For example, to test W is more important than C for certain option O, we formulated
$𝐻_0$: Given controlled D, C and O, different W leads to the same probability distribution of that option.($𝜇_{𝐷0𝐶O}$=$𝜇_{𝐷1𝐶O}$)
$𝐻_𝑎$: Given controlled D, C and O, different W leads to the different probability distribution of that option.($𝜇_{𝐷0𝐶O}$≠$𝜇_{𝐷1𝐶O}$)
If we reject $𝐻_0$, then we can deduce W is more important than C.

4. **3 Factor ANOVA** - in **ANOVA** of `Analysis.ipynb`
   - Specifically, each group is defined by a triple $S = (D, W, C)$, where $D \in \{0, 1, 2\}$,  $W \in \{0, 1\}$ , $C \in \{0, 1\}$. We then carry out ANOVA tests, each filling all the groups with the normalized probabilities of one transportation option. Then let Python calculate $SSD,\ SSW,\ SSC$, sum of squares due to interactions and $SSE$. Finally, we reach our conclusion via F-test. 
**However**, we failed because the distribution of the statistics doesn't follow the normal distribution.



#### Question 2
In **Multinomial Logistic Regression** of `Analysis.ipynb`.
In the preprocessing phase of our analysis, we applied one-hot encoding to the categorical variables - gender, major, grade, origin, and distance - to convert them into a numerical format suitable for regression analysis and applied z-score standardization to normalize the income variable. 

We then constructed multinomial logistic regression models with 14 variables including situational and demographic variables as inputs, and the 4-category variable - transportation options - as the output. The multinomial logistic regression model estimates the probability of the dependent variable belonging to one of the O categories, given the input variables X, and is expressed as:
$$P(O=j,j\neq 0|X)=\frac{exp(\beta_j^TX+\alpha_j)}{1+\sum_{k=1}^{n_o-1}{exp(\beta_k^TX+\alpha_k)}}$$
$$P(O=0|X)=\frac{1}{1+\sum_{k=1}^{n_0-1}{exp(\beta_k^TX+\alpha_k)}}\ (Benchmark)$$
Here we adopted option 0, bus/subway as the benchmark and constructed 3 models.

### Visulization

1. Basic description. We drew a pie chart for distribution of demographic variables.
2. For question 1, 
   - We drew a bar chart for number of the most favorable options of samples in different conditions.
   - We drew a heat map for discrepancy of probability distribution under different situations.
3. For question 2,
   - We drew forest plots to show the confidence interval of variables and the result of heterogeneity test.
   - We listed the confusion matrix to show the estimation accuracy of our regression model.
 