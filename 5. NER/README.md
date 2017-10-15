I used Natasha for NER and ran it on RuEval2016 test set. Natasha has limited opportunities for NER (three extractors: NamesExtractor, DatesExtractor, MoneyExtractor).
I used only NamesExtractor which is kind of equivalent for "objects" in the RuEval tasks (but not the same).

I calculated precision, recall and f1-score myself as I was doing only "objects" recognition.
The result on 132 test docs was:

Precision 0.84<br/>
Recall 0.21<br/>
F1 score 0.34

The drawbacks I noticed are:

- Natasha doesn't recognize abbreviations as NEs though it seems easy to do with some kind of precision
- Natasha doesn't recognize organizations' names like «издание Los Angeles Times»
- Natasha doesn't consider toponyms as NEs («Южная Корея», «Россия», «Москва»)
- the dataset itself is not ideal and includes NEs as «телеканалу» or «пансионате Солнечная поляна подмосковном пансионате»
- the evaluation is rough as I read that for NER task the chunks but not the tokens are tested to match so if there's «Аньелли» in predicted and «Аньелли семья» in true, it wasn't taken into account (though it doesn't feel right)

However the precision is quite high, maybe due to the fact that Natasha extracts NEs basing on few features so there's nothing extra.

Obviously NER tasks are always different and a tool needs to be adjusted for a certain task.
