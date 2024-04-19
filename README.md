# Predict Horse Race Winner
We plan to use Machine Learning to make predictions on a horse race. The data can be used for sports betting. This project is for NTU SC1015 Introduction to AI and ML course. 

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
We scraped the data from Singapore Turf Club Website with Selenium. We first scraped the links to all active horses' previous race performances. The horses and their corresponding links. We then made use of the links to scrape each horse's past individual performance data, which will be used for our predictions later on.

You can view the data in the json files (horse_data.json, horse_profiles.json)

## Exploratory analysis
---fill in later---

## Data Cleaning
We removed any rows with missing columns, and converted categorical data into numerical data through Label Encoding and Target Encoding so that they can be used for Regression. We also created a binary column 'Top3' so that we can do Logistic Regression to predict a binary response.

## Predictive Models
We tried both Multiple Linear Regression as well as Logistic Regression models. We have ten different predictors. These predictors are made available to bettors on race day as well as before the race itself. 

The predictors we used are:
- Horse (encoded)
- Barrier (starting position of horse)
- Carried Weight (weight of jockey)
- Distance (length of track)
- Rating 
- Horse Weight
- Going (condition of track, encoded)
- Track (material of track, encoded)
- Jockey (encoded)
- Trainer (encoded)

For Multiple Linear Regression our response is Finish Time (in seconds). For Logistic Regression, our response is Top3, which determines whether a horse is predicted to finish in the top 3.

## Multiple Linear Regression
We used Linear Regression from Scikit-Learn library to predict the Finish Time of a given horse. The starting point of MLR is the specification of a linear model that describes the hypothesized relationship between the independent variables and the dependent variable. The predictors and response were specified in the section above. The coefficients of the predictors are then estimated. Once the coefficients are estimated, the fitted model can be used to predict the Finish Time for given values of the independent variables (carried weight, horse weight, etc).

We can compare the predicted Finish Time of all horses for an upcoming race, and thus deduce a probable winner. The quality of our fit is then evaluated by checking the Goodness of fit and the Mean Squared Error of both train and test dataset.

## Logistic Regression
We used Logistic Regression from Scikit-Learn library to predict whether a horse will finish Top 3 or not, since it is a binary classification problem. Unlike linear regression, logistic regression models the probability that a dependent variable (Y) is true (Y=1). The probability that each observation falls into one of the categories is modeled using a logistic function. Again, the coefficients of the predictors are estimated, and the fitted model can be used to predict the dependent variable.


However, since the model is predicting for each individual horse, it might predict more/less than 3 horses that will finish Top 3 in a race, based on the given predictors. The quality of fit is evaluated with a confusion matrix, and 

## Real World Application
(Insert result of actually using the models to predict upcoming race)

# Conclusion



