# Predict Horse Race Winner 🏇
We plan to use Machine Learning to make predictions on a horse race. The data can be used for sports betting. This project is for NTU SC1015 Introduction to AI and ML course. This readme document is only a summary. Please view the [Jupyter Notebook](https://github.com/TAN-AIK-CHONG/Horse-Race-Prediction/blob/master/Horse_race_prediction_FINAL.ipynb) for a full picture. Download to view the file if unable to view it on the webpage due to its large size.

## Libraries Used

1. Selenium: Automates browsers. Used for web scraping.
    
    ```bash
    pip install selenium
    ```

2. category-encoders: Encodes categorical data into numerical data.

    ```bash
    pip install category_encoders
    ```

3. Scikit-Learn: Used for regression models.

    ```bash
    pip install scikit-learn
    ```

## Data Scraping
We scraped the data from Singapore Turf Club Website with Selenium. We first [scraped](https://github.com/TAN-AIK-CHONG/Horse-Race-Prediction/blob/master/Selenium%20Scraping/scrape_links.py) the [links to all active horses'](https://github.com/TAN-AIK-CHONG/Horse-Race-Prediction/blob/master/Selenium%20Scraping/horse_data.json) previous race performances. We then made use of the links to [scrape](https://github.com/TAN-AIK-CHONG/Horse-Race-Prediction/blob/master/Selenium%20Scraping/scrape_profiles.py) each horse's past [individual performance data](https://github.com/TAN-AIK-CHONG/Horse-Race-Prediction/blob/master/Selenium%20Scraping/horse_profiles.json), which will be used for our predictions later on.


## Exploratory Data Analysis
We prepared the data for analysis by first removing any rows with empty columns as we had ~40k rows, and even after removing the rows with empty columns we still had a large dataset of ~10k rows.

The first thing we noticed is the extremely high correlation between Distance and Finish Time. This makes Distance not an ideal candidate to be included as a predictor for our regression models as it is a dominating factor. A dominating predictor might mask the effects of other predictors, leading to a loss of information about the true relationships between predictors and the outcome variable. Furthermore, the model might overfit the training data, capturing noise rather than the underlying patterns.

![Image of Distance compared to other variables](https://github.com/TAN-AIK-CHONG/Horse-Race-Prediction/blob/master/images/EDADist.png)

We also introduced a new variable WeightRatio, which is the ratio of the carried weight to the horse weight. We then checked for correlation with our numeric variables. As there is a high correlation between WeightRatio and CarriedWeight, we decided to omit CarriedWeight from our regression models to prevent collinearity issues. We decided that the ratio is the more important factor as it had a higher correlation to the horses' finish times.

![Correlation Matrix of numeric factors](https://github.com/TAN-AIK-CHONG/Horse-Race-Prediction/blob/master/images/NumericFactors.png)

We also further decided not to include categorical variables such as Barrier as it did not seem to have much impact on finish times. Going (condition of track) was also excluded as the vast majority of races had a Going value of Good, and only a few data points had a different value. The large class imbalance and low impact of Going on finish times lead to us leaving it out as well from our predictors. Lastly, the difference in finish times for horses running on a Polytrack compared to a Turf track was quite obvious, so we decided to do OHE (One Hot Encoding) on it and include it as a predictor.

![Image of difference in tracks](https://github.com/TAN-AIK-CHONG/Horse-Race-Prediction/blob/master/images/trackDiff.png)

## Data Cleaning
We first prepared the data for Regression by converting all string data type values into float data type. Furthermore, we converted data with awkward formatting, such as Finish Time (eg. 1:11.74) and Placing (eg. 3/12) into a numeric format.

![Image of before & after](https://github.com/TAN-AIK-CHONG/Horse-Race-Prediction/blob/master/images/numericcleaning.png)

Furthermore, we converted categorical data into numerical data through One Hot Encoding and Target Encoding. For target encoding, we replace categorical variables with the mean of the target variable for each category. In this case, we have used Lengths Behind Winner (LBW) as the target variable. We chose LBW as it is a good indicator of the horse's performance in a race, as seen earlier from our EDA. Below is an image of some random horses and their encoded values.

![Image of example of encoding](https://github.com/TAN-AIK-CHONG/Horse-Race-Prediction/blob/master/images/encodedexample.png)

We also feature engineered a new predictor, which is the ratio of the CarriedWeight to the HorseWeight. We see during EDA that it has a higher positive correlation to FinishTime_Numeric as compared to CarriedWeight and HorseWeight alone, which makes sense, as a horse having to carry a larger percentage of its own bodyweight should find it more difficult.

We chose to only work with data where Distance = 1200m. This is because from our EDA, we discovered that Distance is a dominating factor and it may lead to overfitting of our Regression models, as it will overshadow all other factors. In fact, below is an example of our model's performance on the train dataset, when we included distance as a predictor. 

![Image of overfitting](https://github.com/TAN-AIK-CHONG/Horse-Race-Prediction/blob/master/images/overfitting.png)

Lastly, we removed all outlier data from our DataFrame to help train our Regression models better.

## Predictive Models
We tried both Multiple Linear Regression as well as Logistic Regression models. We settled on 7 predictors. These predictors are made available to bettors (except for weight ratio, which was calculated) on race day as well as before the race itself. 

The predictors we used are:
- Horse (encoded)
- Weight Ratio (Ratio of jockey weight to horse weight)
- Rating 
- Horse Weight
- Track (material of track, One Hot Encoded)
- Jockey (encoded)
- Trainer (encoded)

For Multiple Linear Regression our response is Finish Time (in seconds). For Logistic Regression, our response is Top3, which determines whether a horse is predicted to finish in the top 3.

## Multiple Linear Regression
We used Linear Regression from Scikit-Learn library to predict the Finish Time of a given horse. The starting point of MLR is the specification of a linear model that describes the hypothesized relationship between the independent variables and the dependent variable. The predictors and response were specified in the section above. The coefficients of the predictors are then estimated. Once the coefficients are estimated, the fitted model can be used to predict the Finish Time for given values of the independent variables (rating, horse weight, etc).

We can compare the predicted Finish Time of all horses for an upcoming race, and thus deduce a probable winner. The quality of our fit can be seen below, where we plotted the predicted values against actual values for our test data set.

![Image of test dataset](https://github.com/TAN-AIK-CHONG/Horse-Race-Prediction/blob/master/images/MLRtest.png)

It is important to note that in a horse race, a tenth of a second could result in a different placing. As such, we have to keep the limitations of our model in mind.

## Logistic Regression
We used Logistic Regression from Scikit-Learn library to predict whether a horse will finish Top 3 or not, since it is a binary classification problem. Unlike linear regression, logistic regression models the probability that a dependent variable (Y) is true (Y=1). The probability that each observation falls into one of the categories is modeled using a logistic function. Again, the coefficients of the predictors are estimated, and the fitted model can be used to predict the dependent variable.

However, since the model is predicting for each individual horse, it might predict more/less than 3 horses that will finish Top 3 in a race, based on the given predictors. The quality of fit is can be seen below with a confusion matrix of our test data set.

![Confusion Matrix](https://github.com/TAN-AIK-CHONG/Horse-Race-Prediction/blob/master/images/cfmatrix_log.png)

We are aware that while the model has a relatively high True Positive Rate, its False Positive Rate is also relatively high. This is due to the large class imbalance - the vast majority of horses do not finish top 3 in a race. We had to pick our poison: either suffer from a low True Positive Rate, or train our model with balanced class weights, which will lead to an increase in False Positive Rates as well. In the end, we chose the latter.

## Real World Application
We used our models to predict a [race on 21 Apr 2024](https://racing.turfclub.com.sg/en/race-results/?raceno=6&date=2024-04-21).
These were the real results:
![Image of real results](https://github.com/TAN-AIK-CHONG/Horse-Race-Prediction/blob/master/images/realresults.png)

In the end, our linear regression models predicted 2/3 finishing horses, although it got the order of them wrong. However, our logistic regression model ended up predicting 6 different horses to finish top 3. It predicted that both 'STOP THE WATER' and 'COOL SIXTY-ONE' would finish top 3, but it failed to predict that 'PACIFIC ATLANTIC' would finish top 3 as well. 

![Image of predicted results](https://github.com/TAN-AIK-CHONG/Horse-Race-Prediction/blob/master/images/predicted21apr.png)

Our regression models did not perform extremely well, but this was already expected when we evaluated the goodness of fit of our model. This is also a small sample size of one race, and the models performances on their test data sets are more indicative of how good they are.

# Conclusion
Looking at how others have attempted to predict horse races, there is clearly room for improvement in our project. Firstly, we could have more engineered features, for example, a metric that measures a given horse's recent performance. We also learnt the importance of taking the time to explore and identify different predictors so that we can get a good model. Lastly, an improvement could be to come up with an algorithm to determine an appropriate bet sizing in order to beat the race books consistently in the long term and gain positive EV.


