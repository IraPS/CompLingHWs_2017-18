

1. Using NMF and LDA (sklearn). Basic stopwords set from sklearn, models are set for 20 topics: seems too many as we can see topics like:

Topic 13:
mortgage, rates, rate, mortgages, home, fixed, loan, week, housing, freddie

Topic 14:
fed, rates, federal, reserve, policy, greenspan, inflation, rate, term, chairman

And we need to introduce proper stopwords list.

2. Broaden stopwords set from MySQL, 20 topics (as some kind of a standard) : better, but some words from different topics coincide so it’s hard to distinguish them

4. Broaden stopwords set from MySQL, 10 topics: much better, seems like I can tell many of the topics apart (and NMF seems better than LDA as the former has numbers as top words and some light verbs). I will further use only NMF. The description of topics by NMF that I can see:

Topic 0: about stock markets and Dow Jones index

stock, stocks, market, dow, points, index, average, jones, york, industrial

<br/>
Topic 1: about the US president and discussion on budget and taxes (raising taxes to raise budget?)

tax, president, house, budget, bush, state, congress, government, taxes, administration

<br/>
Topic 2: about international trades between the US and Japan and how dollar and yen sort with each other

dollar, yen, currency, euro, japanese, japan, foreign, marks, trading, york

<br/>
Topic 3: about the trade deficit (imports exceed exports, probably breaking the record point of imports)

billion, deficit, trade, budget, imports, exports, fiscal, year, record, spending

<br/>
Topic 4: about unemployment crisis for the previous month?

percent, rate, unemployment, yesterday, labor, month, department, reported, jobs, rose

<br/>
Topic 5: about inflation and its effects on the federal budget of the US

fed, federal, reserve, bank, policy, rates, interest, inflation, greenspan, central

<br/>
Topic 6: about inflation and its effects on consumers (prices grow?, but why «sales» then)

prices, inflation, consumer, economy, growth, sales, department, quarter, economic, month

<br/>
Topic 7: about mortgage and loans rates

mortgage, rates, interest, rate, home, loans, mortgages, loan, housing, fixed

<br/>
Topic 8: about corporations and how much they earn and cost

million, company, quarter, share, companies, stock, cents, earnings, corp, shares

<br/>
Topic 9: about some financial structure (seems like investment banking) and how its market is growing (market yield)

bond, funds, bonds, investors, fund, treasury, yield, market, yields, year

As all the topics are about some economics problems it seems desirable to have some background in the area to interpret the top-words. And as it was told at the lecture, one sometimes seeks erudition and needs to google proper names as in Topic 5 to find out that greenspan is for Alan Greenspan who was the Chairman of the Federal Reserve of the US.

It’s also useful that even though it’s only unigrams, they form n-grams and make it easier to recognise the topic.

4. Going for only bigrams gives a better picture of texts in the topics but somehow reduces the clarity of the main point of the topics:

Topic 0:
interest rates, short term, term interest, interest rate, long term, lower interest, higher interest, economic growth, bond prices, low interest

Topic 1:
industrial average, dow jones, jones industrial, standard poor, poor 500, stock index, 500 stock, composite index, nasdaq composite, index rose

Topic 2:
white house, social security, budget deficit, health care, president bush, tax cut, federal budget, tax cuts, mr bush, fiscal year

Topic 3:
stock market, million shares, stock exchange, york stock, jones average, average 30, dow jones, ap stock, nasdaq stock, big board

Topic 4:
30 year, fixed rate, 10 year, year treasury, rate mortgages, freddie mac, year fixed, mortgage rates, percent week, adjustable rate

Topic 5:
united states, trade deficit, south korea, west german, west germany, years ago, international monetary, world bank, soviet union, middle east

Topic 6:
real estate, estate investment, estate market, commercial real, investment trusts, estate investors, estate values, investment trust, housing market, washington area

Topic 7:
federal reserve, reserve board, central bank, monetary policy, reserve chairman, alan greenspan, reserve bank, money supply, chairman alan, open market

Topic 8:
wall street, street journal, stock market, chief executive, cents share, year earlier, exchange commission, securities exchange, nasdaq stock, years ago

Topic 9:
labor department, annual rate, commerce department, unemployment rate, price index, department reported, consumer spending, consumer price, reported yesterday, seasonally adjusted

5. Going for uni- and bigrams doesn’t change the result much as there are only few bigrams (so the algorithm doesn’t consider them as «important» as unigrams) and if there are they usually repeat the unigrams:

Topic 3:
fed, rates, federal, reserve, federal reserve, interest, bank, interest rates, policy, rate - «rates», «interest», «interest rates»

6. Coming back to the description in point 3, 10 topics seem to be a good number though I think Topic 8 and Topic 9 might be merged. But reducing the number of topics to 9 and increasing the number of top words to 15 it turned out that the two topics needed to be merged were Topic 0 and Topic 8 from point 3. They are one topic on the US(?) stock market for the quarter and Dow Jones index is the measurement of the market represented by some corporations. 

Summary:

I assume there are 9 topica in this dataset, which are:

- US president’s discussion and decision on budget and taxes (raising taxes to raise budget?) 

- international trades, especially between the US and Japan and how dollar and yen sort with each other

- about the trade deficit (imports exceed exports, probably breaking the record point of imports)

- unemployment rates for the recent times

- inflation and its effects on the federal budget of the US

- inflation and its effects on consumers

- mortgage and loans rates

- the US stock market for the quarter and it’s measurements

I also thought that Topic on inflation and federal budget and inflation and consumers could be merged, but reducing the number of topics to 7 ruined the picture, topics became mixed and some pretty certain ones were lost.

Thus even though I didn’t use any sophisticate methods for choosing the top-words, even without lemmatization (so having different wordforms of the same lemma) it was enough to understand the meaning of those top-words sets.

Using lemmatization required some new stopwords (as «n’t» or «’s») and it seems that lemmas made the results worse:

Topic 0:
stock, point, market, dow, index, average, york, jones, wa, share, industrial, trading, day, gain, today

Topic 1:
dollar, yen, u, currency, euro, mark, japanese, japan, trading, york, trader, late, market, german, trade

Topic 2:
bond, yield, treasury, fund, investor, price, market, year, note, rate, interest, security, investment, benchmark, stock

Topic 3:
tax, state, president, house, budget, ha, bush, congress, government, republican, cut, bill, program, job, administration

Topic 4:
price, consumer, inflation, month, economy, economist, growth, sale, department, economic, report, quarter, labor, increase, year

Topic 5:
company, million, share, fund, bank, stock, year, corp, firm, ha, billion, earnings, business, loan, market

Topic 6:
billion, deficit, trade, budget, import, fiscal, export, year, u, spending, record, surplus, commerce, month, gap

Topic 7:
percent, rate, mortgage, unemployment, year, week, yesterday, home, interest, reported, month, wa, average, department, increase

Topic 8:
fed, rate, bank, reserve, interest, federal, policy, central, inflation, loan, credit, greenspan, chairman, economy, meeting

It is not that clear anymore what the topic is about and also mortgage topic is mixed with unemployment topic (Topic 7). Taking both uni- and bigrams from lemmas has the same effect as before (top bigrams are composed from top unigrams - not much new information from this), we lose unemployment topic at all, but we now know that the first topic (US president’s discussion and decision on budget and taxes) is about George Bush.

I am not sure why lemmatization has less clear results than just tokenization, but as it was said before NMF with 9 topics represented by top unigrams, stopwords list from MySQL and no lemmatization was enough. And seems that topic modelling isn’t likely to give the precise list of top words perfectly describing the topics and it’ll usually require figuring out the meaning involving general knowledge and erudition especially for texts from newspapers or political and economical magazines. 
