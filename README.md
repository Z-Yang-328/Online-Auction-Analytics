# Springboard-Capstone-Project

## Kaggle Competition: Human or Robot?

### About the Problem

__This is the final report of my approach in a interesting _[Kaggle competition](https://www.kaggle.com/c/facebook-recruiting-iv-human-or-bot)_ hosted by Facebook. We are giving data describing bidders' bidding behaviors in an online auction website. The goal of the competition is to come up with a predictive model that can recognize whether a bidder is human or robot.__

### Exploratory Data Analysis

* A quick dive in to data before building predictive models by plotting bidding behaviors over time indicates that there are obvious behavioral difference between human bidders and robot bidders. Robot bidders usually make series of bids in a short period of time (high bidding speed), while human bidders have much lower bidding speed;


* Robot bidders do make much more bids in average than human bidders;


* The merchandises in which robot bidders are more likely to make bids, in decreasing order, are mobile, sporting goods, and jewelry. And bidding behaviors could be very different between different merchandises;


* Some countries (like Japan, Korea and Macau) have much more percentage of robot bidders while some countries have much lower percentage of robot bidders.

### Summary 

    Among all three sets of models, Random Forest (RF) and AdaBoost (AB) have the best auc scores (scores of RF is a little bit better than those of AB). Other modeling algorithms like k-Nearest-Neighbors and Logistic Regression have much lower AUC scores in average. 

    I used 5-fold cross validation, which is a relatively better number of folds (not too time-consuming), to fine-tuning and evaluating the models. Fine-tuning RF models takes relatively more time, but it is still very much tolerable. I tuned models using AUC scoring because AUC scores are the only way to evaluate prediction results in this Kaggle competition. And since the data are imbalanced (5% labeled robots, 95% human), we must consider resampling the data to get better results. According to the number of observations of data, over-sampling method will result in better results.
    
    Here is the table of results of all the models:
    
    
|        Models       | Original Features| Original Features         |       Additional Features      |
|:-------------------:|:-------------:|:----------------------------:|:------------------------------:|
|                     | AUC (untuned) | AUC (tuned and over-sampled) |   AUC (tuned and over-sampled) |
|    Random Forest    |  0.80         |   0.82                       |   0.84                         |
| k-Nearest-Neighbors |  0.72         |   0.76                       |   0.76                         |
| Logistic Regression |  0.66         |   0.74                       |   0.69                         |
|       AdaBoost      |  0.81         |   0.84                       |   0.84                         |
|  Anomaly Detection  |  0.80         |   N/A                        |   0.73                         |

### Ideas for Further Research

* **Feature Engineering**  
   Feature engineering is always a very important part in building predictive models. According to the results, adding more features do not increase the models' AUC scores significantly (for some models, AUC score even decreased). Therefore, in the future, I need to spend more time on exploring the data set, and then come up with more meaningful ideas to create new features.


* **Trying more modeling algorithms**  
   In this capstone project, I only used 5 algorithms (4 supervised and 1 unsupervised) to build models. However, there may be other algorithms which could be more suitable for this problem.
   
### Recommandations

According to my findings, the following recommandations will help the company to better recognize robot bidders:  

* **Countries**  
   Focus on bidders in certain countries/districts like Japan, Korea, Macau, Taiwan, German, US. Because in these countries, bidders much more likely to be classified as robots.  
   
   
* **Devices**  
   Certain models of devices that robot biders are more likely to use to making bids. Focusing on these models will increase the chance of recognizing robot bidders.  
   
   
* **Bidding Speed**  
   Bidding speed is an very important difference between human and robot bidders. Robots are able to make a large number of bids in a short period of time. So in real bidding events, once a bidder's bidding speed is recognized as "abnormal", the bidder should be classified as a robot bidder.  
