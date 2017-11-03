I collected following features for each token: POS-tag, position in the sentence, case (if applicable, else 0), voice (if applicable, else 0), verbform (if applicable, else 0).

I trained several classifiers, the result was:

| Classifier| Accuracy |
| ------------- | ------------- |
| Nearest Neighbors | 0.62  |
| Decision Tree | 0.60  |
| Random Forest | 0.53  |
| Neural Net | **0.67** |
| Naive Bayes | 0.26 |
| Logistic Regression | 0.48 |

I looked into the weights regression model assigns to the features but as it is multi-class labelling, it is "one vs. all" approach and we cannot establish the most valuable features for the whole corpus. All the weights are quite low, from some observations: position is the most important for Punc and VerbForm for Root (which makes sense).
