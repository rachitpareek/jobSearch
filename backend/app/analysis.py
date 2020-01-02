from app import routes
def run():
    import time
    start_time = time.time()
    # Import necessary packages and silence silly warnings.
    print("Importing items...")
    import re
    import random
    import os
    import warnings
    import pandas as pd 
    import numpy as np
    from nltk.corpus import words
    from nltk.stem import WordNetLemmatizer 
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn import metrics
    from sklearn.metrics import precision_score
    from sklearn.metrics import recall_score
    from sklearn.metrics import confusion_matrix
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import roc_curve
    from sklearn.metrics import roc_auc_score
    from sklearn.preprocessing import StandardScaler
    from sklearn.exceptions import DataConversionWarning
    from pandas.core.common import SettingWithCopyWarning
    warnings.filterwarnings(action='ignore', category=DataConversionWarning)
    warnings.filterwarnings(action='ignore', category=SettingWithCopyWarning)
    print("Imported!")

    for_return = {}

    print("Defining functions...")
    def text_cleaner(string):
        """ This function will clean the text of email bodies by: 1. removing numbers, 
            2. keeping only words longer than 4 letters, and lemmatizing each word.
            Ensuring each word is part of the NLTK english language corpus led to exponential runtime.
        """
        split_words = re.findall("[^\d_\W]+", string)
        lemmatizer = WordNetLemmatizer() 
        split_words = [lemmatizer.lemmatize(word.lower()) for word in split_words if len(word) > 4]
        return " ".join(split_words)

    def in_school_year(date):
        """Returns 1 if the date inputted is during a school month (Jan-Apr, Sept-Dec), and 0 otherwise.
        """
        month = int(re.findall(".+?(?=/)", date)[0])
        school_months = [1, 2, 3, 4, 9, 10, 11, 12]
        if month > 0 and month < 13:
            if month in school_months:
                return 1
            else:
                return 0
        else:
            return None
        
    def preprocessor(table):
        """The inputted table must have the following columns:
        "Date & Time Received": Strings formatted like "3/14/1972".
        "From": String, an email address like "me@example.com".
        "Subject": String of free-form text.
        "Email Text": String of free-form text.
        "Related": 1 if this email is internship-related, 0 if it's not.
        NOTE: The fact that the features being used are dynamically selected by this notebook based on the input
            makes it somewhat unsupervised learning."""
        # Basic pre-processing: 
        # 1. Select only relevant columns.
        table = table[["Date & Time Received", "From", "Subject", "Email Text", "Related"]].dropna().reset_index()
        # 2. Use regex to help extract the sender domain from the emails.
        table["From"] = table["From"].apply((lambda x: re.findall("(?<=@)[^.]+(?=\.)", x)[0].replace("-", " ")))
        # 3. Clean email subject and body text using function defined above. 
        table["Email Text"] = table["Email Text"].apply(text_cleaner)
        table["Subject"] = table["Subject"].apply(text_cleaner)

        # Let's do some feature engineering:
        # 1. Add a few feature that indicate 1 if the email was sent during a school month (Jan-Apr, Sept-Dec), and 0 otherwise.
        table["In School Year"] = table["Date & Time Received"].apply(in_school_year)
        # 2. Add a few feature that shows the normalized length of the email.
        table["Length"] = table["Email Text"].apply(lambda string: len(string))
        table["Length"] = StandardScaler().fit_transform(np.array(table["Length"]).reshape(-1, 1))
        # 3. Create vectorized representations of whether email is from a specific top sender.
        sv = CountVectorizer(lowercase=True, ngram_range = (1,2))
        sender_counts = sv.fit_transform(table['From'])
        sender_vectors = pd.DataFrame(sender_counts.todense(), columns=["Sender: " + i for i in sv.get_feature_names()])
        # 4. Reorder columns and rename the final column.
        table = table[["From", "Subject", "Email Text", "In School Year", "Length", "Related"]].rename(columns={"Related": "Internship-Related"})
        # 5. Add the vectors of senders to the table.
        table = pd.concat([table, sender_vectors], axis=1)
        # 6. Add the vectors of words from the email bodies to the table.
        cv_word_vectors, tv_word_vectors = cv_and_tfidf_vectorize(table)
        table = pd.concat([table, cv_word_vectors], axis=1)
        
        return table

    def get_top_senders(table, count):
        """Given a table, return the top count number of email senders as a table.
        """
        return table["From"].value_counts().to_frame().head(count).rename(columns={"From": "Counts"})

    def cv_and_tfidf_vectorize(table):
        """ Use CountVectorizer and TfidfVectorizer to create a matrix representation of the words used across all emails, 
            ensuring that all words included are real English words as in the NLTK English Corpus.
        """    
        cv = CountVectorizer(lowercase=True, stop_words='english', ngram_range = (1,1))
        cv_word_counts = cv.fit_transform(table['Email Text'])
        cwc = pd.DataFrame(cv_word_counts.todense(), columns=cv.get_feature_names())

        tv = TfidfVectorizer(lowercase=True, stop_words='english', ngram_range = (1,1))
        tv_word_counts = tv.fit_transform(table['Email Text'])
        tvc = pd.DataFrame(tv_word_counts.todense(), columns=tv.get_feature_names())
        
        cwc.columns.sort_values()
        tvc.columns.sort_values()
        
        real_word_list = []
        s = set(words.words())
        for i,x in enumerate(cwc.columns.sort_values()):
            if x in s:
                real_word_list.append(x)
        cwc = cwc[real_word_list]

        real_word_list = []
        for i,x in enumerate(tvc.columns.sort_values()):
            if x in s:
                real_word_list.append(x)
        tvc = tvc[real_word_list]
        
        return cwc, tvc

    def vector_table_sum(table, title):
        """ Given a sparse array of vectors, returns a table with the columns summed."""
        return (table
            .sum(axis = 0, skipna = True)
            .to_frame()
            .rename(columns={0: title})
            .sort_values(by=[title], ascending=False))

    def make_modeling_data(table, num_words, num_senders):
        """Use this to create a dataframe we can use for modeling."""
        top_senders = get_top_senders(table, num_senders)
        temp, word_vectors = cv_and_tfidf_vectorize(table)
        #Use a sample of the top words from the emails that are correctly tagged as features.
        #Purposely use asymptotically half from the training emails that are and aren't internship-related.
        top_related_words = list(vector_table_sum(cv_and_tfidf_vectorize(table[table["Internship-Related"] == 1])[0], "Sum of Scores").index)
        top_unrelated_words = list(vector_table_sum(cv_and_tfidf_vectorize(table[table["Internship-Related"] == 0])[0], "Sum of Scores").index)
        top_words = top_related_words[:num_words] + top_unrelated_words[:num_words]
        #top_words = random.sample(top_words, int(len(top_words)/2))
        # 1. Word features (from body text):
        modeling_data = word_vectors[top_words[:(num_words * 2)]] 
        # 2. Whether the email was during the school year:
        modeling_data["In School Year"] = table["In School Year"]
        # 3. Normalized length of the email's body.
        modeling_data["Length"] = table["Length"]
        # 4. Whether the email was from one of my top senders. 
        # The way .head() works means this will function even if num_senders > len(top_senders). 
        indices = ["Sender: " + i for i in top_senders.head(num_senders).index]
        modeling_data[indices] = table[indices]
        return modeling_data

    print("Defined!")

    print("Reading in data and splitting it into sets...")
    # Read in and view raw input file.
    # TODO: Take away head after tagging all emails.
    #3712, 9541
    data = pd.read_csv('./app/' + routes.FILENAME).head(3500)
    os.remove('./app/' + routes.FILENAME)
    if len([True for i in ["Date & Time Received", "From", "Subject", "Email Text", "Related"] if i not in data.columns.values]) > 0:
        return False

    #Run preprocessor on data table. See function definition for description.
    data = preprocessor(data)

    for_return["table_shape"] = data.shape

    #Split data into training and test sets.
    X_train, X_test, y_train, y_test = train_test_split(data.drop(["Internship-Related"], axis=1),
                                                        data["Internship-Related"].to_frame(),
                                                        test_size=0.2,
                                                        random_state=42)
    training_data = pd.concat([X_train, y_train], axis=1).sort_index().reset_index()
    testing_data = pd.concat([X_test, y_test], axis=1).sort_index().reset_index()

    print(str(round(training_data["Internship-Related"].sum()*100/len(training_data), 2)) + "% of the training emails are internship-related.")
    print(f'Training set size: {len(training_data)} emails')
    print(f'Test set size: {len(testing_data)} emails')

    for_return["tss"] = len(training_data)
    for_return["testss"] = len(testing_data)

    print("Let's try and find out which words are the most important...")
    # Let's try and find out which words are the most important.
    cv_word_vectors, tv_word_vectors = cv_and_tfidf_vectorize(training_data[training_data["Internship-Related"] == 0])

    # Because the matrices are sparse, we can't interpret much from them. Let's visualize which words are the most 
    # common & have the most importance under both vectorization schemes:
    cv_sums = vector_table_sum(cv_word_vectors, "Sum of Counts")
    tv_sums = vector_table_sum(tv_word_vectors, "Sum of Scores")
    print("Found the most common words from the training emails that aren't truly internship-related.")
    print(list(np.array(tv_sums.head(15).index)))
    for_return["top_unrelated_words"] = np.array(tv_sums.head(15).index).tolist()
    cv_word_vectors, tv_word_vectors = cv_and_tfidf_vectorize(training_data[training_data["Internship-Related"] == 1])

    # Because the matrices are sparse, we can't interpret much from them. Let's visualize which words are the most 
    # common & have the most importance under both vectorization schemes:
    cv_sums = vector_table_sum(cv_word_vectors, "Sum of Counts")
    tv_sums = vector_table_sum(tv_word_vectors, "Sum of Scores")
    print("Found the most common words from the training emails that are truly internship-related.")
    print(list(np.array(tv_sums.head(15).index)))
    for_return["top_related_words"] = np.array(tv_sums.head(15).index).tolist()

    print("Finding top senders...")
    top_senders = get_top_senders(training_data, 15)
    print(list(np.array(top_senders.index)))
    for_return["top_senders"] = np.array(top_senders.index).tolist()

    print("Found them!")

    print("Finding connection between month and # of internship-related emails...")
    # This visualization seems to show that there's a strong connection between whether the email was sent during a school
    # month and whether it was an internship-related email. The grind really concentrates itself in school months, and
    # it would be odd, after all, to already be searching for another internship while working another one during the summer!
    both = len(training_data[(training_data["In School Year"] > 0) & (training_data["Internship-Related"] > 0)])/len(training_data[(training_data["Internship-Related"] > 0)])
    summer_internship = len(training_data[(training_data["In School Year"] == 0) & (training_data["Internship-Related"] > 0)])/len(training_data[(training_data["Internship-Related"] > 0)])
    print(f'Related & In School Year: {round(both, 3)}')
    print(f'Related but in Summer: {round(summer_internship, 3)}')

    for_return["prop_during_school"] = round(both, 3)
    print("Found!")
    for_return["ttr"] = round((time.time() - start_time)/60, 2)

    return for_return

    # print("Let's find out what the best number of words to use as features might be...")
    # # Let's try finding out what the best number of words to use as features is.
    # results = []
    # percent_done = 0
    # for num in range(10, 500, 20):
        
    #     percent_done += 100/((500-0)/20)
        
    #     word_num = num
    #     senders = 0

    #     X_train = make_modeling_data(training_data, word_num, senders)
    #     X_test = make_modeling_data(testing_data, word_num, senders)

    #     logistic_model = LogisticRegression(max_iter=5000)
    #     logistic_model.fit(X_train, training_data["Internship-Related"])

    #     score = logistic_model.score(X_test, testing_data["Internship-Related"])
    #     coefs = logistic_model.coef_
    #     logistic_model_probabilities = logistic_model.predict_proba(X_test)[:, 1]
    #     auc = roc_auc_score(y_test, logistic_model_probabilities)
    #     results.append((word_num, score, auc))
    #     print(percent_done, "% done")

    # word_nums, aucs = [i[0] for i in results], [i[2] for i in results]

    # best_word_num = word_nums[aucs.index(max(aucs))]
    # print("It seems the best number of words to use is", best_word_num)
    # print("It has an AUC of", max(aucs))

    # print("Let's find out what the best number of senders to use as features might be...")

    # results = []
    # percent_done = 0
    # for num in range(5, 50, 5):
        
    #     percent_done += 100/((50-0)/5)
        
    #     word_num = best_word_num
    #     senders = num

    #     X_train = make_modeling_data(training_data, word_num, senders)
    #     X_test = make_modeling_data(testing_data, word_num, senders)

    #     logistic_model = LogisticRegression(max_iter=5000)
    #     logistic_model.fit(X_train, training_data["Internship-Related"])

    #     score = logistic_model.score(X_test, testing_data["Internship-Related"])
    #     coefs = logistic_model.coef_
    #     logistic_model_probabilities = logistic_model.predict_proba(X_test)[:, 1]
    #     auc = roc_auc_score(y_test, logistic_model_probabilities)
    #     results.append((senders, score, auc))
    #     print(percent_done, "% done")

    # sender_nums, aucs = [i[0] for i in results], [i[2] for i in results]
    # best_senders_num = sender_nums[aucs.index(max(aucs))]
    # print("It seems the best number of senders to use is", best_senders_num)
    # print("It has an AUC of", max(aucs))

    # print("Now, let's fit the model using", best_word_num, "words as features and", best_senders_num, "senders as features...")

    # # It seems that the best number of words and senders to use are 75 and 25. 
    # X_train = make_modeling_data(training_data, best_word_num, best_senders_num)
    # X_test = make_modeling_data(testing_data, best_word_num, best_senders_num)

    # #Now, let's fit our model.
    # logistic_model = LogisticRegression(max_iter=5000)
    # logistic_model.fit(X_train, training_data["Internship-Related"])

    # score = logistic_model.score(X_test, testing_data["Internship-Related"])
    # precision = precision_score(y_test, logistic_model.predict(X_test))
    # recall = recall_score(y_test, logistic_model.predict(X_test))
    # logistic_model_probabilities = logistic_model.predict_proba(X_test)[:, 1]
    # auc = roc_auc_score(y_test, logistic_model_probabilities)
    # print("Done fitting!")
    # print(f'Number of features: {len(X_train.columns)}')

    # print(f'Score: {score}')
    # print(f'Precision: {precision}')
    # print(f'Recall: {recall}')
    # print(f'AUC: {auc}')

    #print("My program took about", round((time.time() - start_time)/60, 2), "minutes to run")