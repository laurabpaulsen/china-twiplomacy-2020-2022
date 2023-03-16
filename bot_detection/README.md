# Bot detection
We train a logistic classifier on the cresci-2017 (Cresci et al., 2017) data set (available: https://botometer.osome.iu.edu/bot-repository/datasets.html) to classify Twitter handles as genuine or spam/bot/fake. We use the widely used fofo metric (e.g. Yang et al., 2013; Tavazoee et al., 2020) which is (following/followers) of an account. We use (following+1/followers+1) to avoid division with zero, and when an account appears more than once in a data set we use only the last appearance (i.e. the number of following and followers for the handle at that time). The intuition behind the metric is that bot-accounts tend to follow many other accounts (following) but they tend to have few followers. This means that they will generally have a high fofo-ratio (i.e. high following, low followers). Using the trained model, we estimate the fraction of genuine accounts vs. spam/bot/fake accounts in our own data set, as well as in a baseline data set consisting of vaccine-related tweets from 2020-2021 (https://www.kaggle.com/datasets/gpreda/all-covid19-vaccines-tweets). We estimate 27.22% of the accounts in the baseline (vaccine) data set to be non-genuine accounts and 44.84% of accounts in our data set of Chinese state media and diplomats to be non-genuine accounts. There is considerable uncertainty around this estimate since (1) our data set might differ in other respects than the amount of bot-activity from the baseline data set and (2) while the fofo-metric is widely used (Yang et al., 2013) it is not universally found to be accurate in detecting bots. 



## Bot detection pipeline. 

### preparation
(1) download "cresci-2017" data from https://botometer.osome.iu.edu/bot-repository/datasets.html
(2) unzip everything into datasets_full.csv folder
(3) download baseline dataset into baseline_data/vaccination_all_tweets.csv (https://www.kaggle.com/datasets/gpreda/all-covid19-vaccines-tweets)

### pipeline
(1) prepare our own data (prepare_fofo_data.py)
(2) train model (train_mdl.py)
(3) score records of our data and basline (scoring.py)
(4) generate summary stats and plots (plots_and_summary.py)