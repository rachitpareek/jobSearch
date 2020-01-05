# Overview
This application uses Node, Express, Jupyter Notebook, Pandas, NLTK, Scikit Learn, NLTK, Matplotlib, Plotly, Flask to help break down my internship search over the past recruiting season (for Summer 2020) and create a web application to help others track and visualize their processes as well. The application is live at `jobsearch.herokuapp.com`.

# Motivation
This project aims to understand the effectiveness of different strategies for applying to jobs (especially by looking at response rates for cold applications). Additionally, it's my first attempt at creating an email classifier using the Bag of Words method (through Scikit's CountVectorizer and a Naive Bayes model). The application first reduces the contents of emails to vectors of word counts from a general corpus (which, for the first 1231 emails was of size 17,700 after removing Scikit's default `english` stopwords.). Then, I trained a Naive Bayes model on my pre-tagged emails (1 if job-related, 0 otherwise). After classifying the emails, I created a confusion matrix (`this will soon be added below`). Finally, I filtered the emails to only those classified as job-related and manually created the Sankey diagram below (`also to be added soon`).

# Structure 
It contains two main applications:
- the express app
- the jupyter notebook

# Installation
`Make sure you have a correctly formatted email content file. A correct formatted file will...`
```Javascript
cd jobSearch
npm install
npm start
```

# Running
Visit `localhost:4000` to see the application. 

# Improvements
- Improve the classifier!

# Important Links
- `https://github.com/NicolaLC/ElectronFloatingScreen`
- `https://pythontips.com/2013/07/30/what-is-virtualenv/`
- `https://www.geeksforgeeks.org/run-python-script-node-js-using-child-process-spawn-method/amp/`
- `http://rwet.decontextualize.com/book/textblob/`
- `https://www.google.com/search?q=precision+recall&sxsrf=ACYBGNTQTMnDEPGWwrNVN__MViNEtL6I7Q:1577357409073&tbm=isch&source=iu&ictx=1&fir=tmtmMVoERvLNrM%253A%252CrCa1-SuJ1Z_myM%252C%252Fm%252F03d144_&vet=1&usg=AI4_-kSWKI13Th0iwTfa5hLKCXI7Oiwp7g&sa=X&ved=2ahUKEwj7vrSgktPmAhXF3J4KHTa_AFoQ_B0wEnoECAoQAw#imgrc=tmtmMVoERvLNrM:`
- `https://medium.com/@cristhianboujon/how-to-list-the-most-common-words-from-text-corpus-using-scikit-learn-dad4d0cab41d`

# TODO:
- Finish downloading and tagging all job related emails
- Use oversampling
- Make 4-way error box
- Make sankey diagram

