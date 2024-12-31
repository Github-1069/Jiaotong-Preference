## 'Jiao Tong' Preference of Jiao Tong Undergraduates

### Topic

At weekends, SJTU undergraduates face a dilemma—they want to get refreshed in the downtown area of Shanghai, but they either have to spend a lot of time on the railway or pay a relatively high amount for taxiing. We are interested in what factors affect SJTU undergraduates' choices of transportation.

### Questions

1. Given some situations, which vary in distance, weather, time constraint, etc., will the students' travel mode choices differentiate? What is the most important factor among these *situational variables*? Note that we do not consider the characters of students in this question.
2. For any given situation, i.e. a vector of situational variables, will the students' choices differentiate due to their *fixed variables* including gender, origins, grades, major, family income, etc.?
3. (Optional) Take all the variables into consideration. Are there any interactions? Can we build a simple model to predict students' decisions under different circumstances?

### Background information

We may need to use statistical learning methods not mentioned in the course, like logistic regression. Fortunately, there are lots of online resources to help us learn.

### Variables

#### Situational Variables

| **Variable**            | **Type** | **Description**                             |
| ----------------------- | -------- | ------------------------------------------- |
| Weather conditions      | Dummy    | 0 for sunny, 1 for rainy.                   |
| Time constraint         | Dummy    | 0 for time-abundant, 1 for time-constrained |
| Distance to destination | Category | 0/1/2 - short/medium/long-distance          |

#### Fixed Variables

| **Variable** | **Type** | **Description**                                              |
| ------------ | -------- | ------------------------------------------------------------ |
| Gender       | Dummy    | 0 for female, 1 for male.                                    |
| Origin       | Category | 0 for eastern, 1 for middle, 2 for western.                  |
| Grade        | Category | (we simply delve into the option of undergrduates so) 0 for freshman, 1 for sophomore, 2 for junior, 3 for senior.                         |
| Major        | Category | 0 for STEM, 1 for ACEM, 2 for liberal arts and social science, 3 for medical. |
| Income       | Int (¥)  | The student's income level in Chinese Yuan.                  |

#### Response Variable

| **Variable**             | **Type**         | **Description**                                              |
| ------------------------ | ---------------- | ------------------------------------------------------------ |
| Choice of transportation | Vector of floats | Each student assigns scores to transportation options*, then the scores are converted into a probability distribution using the softmax function. If we decide to use categorical variables later, we can perform `argmax` to get the students' choices. If we decide to use continuous variables in ANOVA, then the softmax score of each option will be compared. |

*Options include: 0 for subway/bus, 1 for taxi, 2 for bikes/e-bikes, 3 for walking. 

### Data Collection

Questionnaires that collect

1. Basic information, i.e. the fixed variables mentioned above.
2. Decisions. We will design some situations with different combinations of situational variables and let students assign a score to each means of transportation.

### Methods 

#### Data Pre-process

1. Drop trivial columns.
2. Fill NaN with 0.
3. Rename the remaining columns and convert all independent variables into int 0, 1, 2...
4. Transform each students' preference under each circumstance with softmax function. Note that we will not add $e^0$ into denominators. The probability that was originally 0 remains 0 after softmax operation.
   
**How this part is done will be shown in _Clean.ipynb_**

#### Question 1

1. We tried to apply 3 Factor ANOVA in the first place. Specifically, each group is defined by a triple $S = (D, W, C)$, where $D \in \{0, 1, 2\}$,  $W \in \{0, 1\}$ , $C \in \{0, 1\}$, denote distance, weather and time constraint respectively. We then carry out **ANOVA tests**, each filling all the groups with the normalized probabilities of **one transportation option**. Then let Python calculate $SSD,\ SSW,\ SSC$, sum of squares due to interactions and $SSE$. Finally, we reach our conclusion via F-test. **However**, we failed for the distribution of the statistics doesn't follow the normal distribution.

2. We managed to apply **Independence test with Pearson's $\chi^2$**. If we reject $H_0$, we can conclude there are interactions between situational variables. Try `argmax` for normalized probabilities. For each transportation option, fill in the number of people in each group who most prefer that option under the group conditions. The test statistic is
   $$
   \sum_i\sum_d^D \sum_w^W \sum_c^C \frac{(f_{dwci} - e_{dwci})^2}{e_{dwci}} \sim \chi^2(3\times11)
   \nonumber
   $$


#### Question 2

Multivariate Logistic Regression. Pending.

### Visulization

Pending.