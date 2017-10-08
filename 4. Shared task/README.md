I used SGDClassifier and LogisticRegression classifiers from sklearn to determine emoji for tweets. I ran the script on 325K tweets with 10% for the test. The result is very low: f1-score is 0.28 for both, using sklearn metrics tool. Macro F-Score from official competition script is 22.765 for SGD and 22.428 for LogRegression. I also used GridSearch to establish some parameters.

Confusion matrices for both classifiers are available in .png.
The worst results are for 
 _red_heart_ - which is somehow weird, as it seems the easy one
 _face_with_tears_of_joy_ - seems also easy for a human
_two_hearts_
_blue_heart_ - very bad
_smiling_face_with_smiling_eyes_ - as it seems very common in many kinds of messages