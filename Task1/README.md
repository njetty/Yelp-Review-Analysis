# Z534 Task 1

## Running Instructions: 
./Initial_run.sh

This will create the required directory structure and also creates a virtual environment and installs the required modules for the task1 to run properly

Once done, follow the below process to download the nltk packages that are required for the task1

```
python
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
quit()
```
place the business, review and tip json files of Yelp in the `input/Dataset` directory without changing the names. These names are hardcoded in the file.

```
python createFeatureVectors.py
```

This will create a busicessDict.pickle file in `input/Dataset/` directory

```
python CreateClassifiers.py
python CreateClassifiersusingPOSTagger.py
```

These will create 4 output files each in the `input/Dataset/Task1/Results` directory each. One for each of the classifier used in these programs for predicting the categories of the reviews.
