## 'Jiao Tong' Preference of Jiao Tong Undergraduates

### Topic

At weekends, SJTU undergraduates face a dilemma—they want to get refreshed in the downtown area of Shanghai, but they either have to spend a lot of time on the railway or pay a relatively high amount for taxiing. We are interested in what factors affect SJTU undergraduates' choices of transportation.

### Questions

1. Given some situations, which vary in distance, weather, time constraint, etc., will the students' choice of transportation differentiate? What is the most important factor among these *situational variables*? Note that we do not consider the characters of students in this question.
2. For any given situation, will the students' choices differentiate due to *demographic variables* including gender, origins, grades, major, pocket money, etc.?
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
| Income       | Int (¥)  | The student's income level in Chinese Yuan.                  |

*The subjects of our study are limited to undergraduates. 

#### Response Variable

| **Variable**             | **Type**         | **Description**                                              |
| ------------------------ | ---------------- | ------------------------------------------------------------ |
| Choice of transportation | Vector of floats | Each student assigns scores to transportation options*, then the scores are converted into a probability distribution using the softmax function. If we decide to use categorical variables later, we can perform `argmax` to get the students' choices. |

*Options include: 0 for subway/bus, 1 for taxi, 2 for bikes/e-bikes, 3 for walking. 

### Data Collection

Questionnaires that collect

1. Basic information, i.e. the demographic variables mentioned above.
2. Decisions. We will design some situations with different combinations of situational variables and let students assign a score to each means of transportation by adjusting rating sliders.

### Methods 

#### Data Pre-process

In `Clean.ipynb`, we

1. Drop trivial columns.
2. Fill NaN with 0. If the student does not adjust the rating slider for a particular option, we assume that he/she has no preference for that option.
3. Rename the remaining columns according to **Description** in [Situational Variables](#situational-variables).
4. Transform each students' preference under each circumstance with softmax function. 
   - We will not add $e^0$ into denominators. The probability that was originally 0 remains 0 after softmax operation.
   - Since the scores are in range [0, 100], we actually calculate softmax with `score/=100`.

#### Question 1

1. We tried to apply 3 Factor ANOVA in the first place. Specifically, each group is defined by a triple $S = (D, W, C)$, where $D \in \{0, 1, 2\}$,  $W \in \{0, 1\}$ , $C \in \{0, 1\}$, denote distance, weather and time constraint respectively. We then carry out ANOVA tests, each filling all the groups with the normalized probabilities of one transportation option. Then let Python calculate $SSD,\ SSW,\ SSC$, sum of squares due to interactions and $SSE$. Finally, we reach our conclusion via F-test. **However**, we failed for the distribution of the statistics doesn't follow the normal distribution.

2. We managed to apply **Independence test with Pearson's $\chi^2$**. 
   - $H_0$: under any given situation, the proportions of the transportation options are equal. If we reject $H_0$, we can conclude there are interactions between situational variables. 
   - For each transportation option, fill in the number of people in each group who most prefer(i.e. `argmax`) that option under the group situation. The test statistic is
   $$
   \sum_{o=0}^{n_o - 1} \sum_{s}^{S} \frac{(f_{os} - e_{os})^2}{e_{os}} \sim \chi^2\Big((n_o - 1)(n_S - 1)\Big)
   \nonumber
   $$
   where $o$ denotes transportation options, $S$ is the set of all situations, $n_o = 4$, $n_S = 12$.

3. Adjusted Marascuilo procedure with Bonferroni correction.
   - Why adjusted? In our textbook, 
   - Why Bonferroni correction? 

#### Question 2

Multivariate Logistic Regression. Pending.

### Visulization

1. Basic description. We draw pie charts for demographic variables.
2. For question 1, 