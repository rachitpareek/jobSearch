https://github.com/NicolaLC/ElectronFloatingScreen
https://pythontips.com/2013/07/30/what-is-virtualenv/
https://www.geeksforgeeks.org/run-python-script-node-js-using-child-process-spawn-method/amp/
http://rwet.decontextualize.com/book/textblob/
https://www.google.com/search?q=precision+recall&sxsrf=ACYBGNTQTMnDEPGWwrNVN__MViNEtL6I7Q:1577357409073&tbm=isch&source=iu&ictx=1&fir=tmtmMVoERvLNrM%253A%252CrCa1-SuJ1Z_myM%252C%252Fm%252F03d144_&vet=1&usg=AI4_-kSWKI13Th0iwTfa5hLKCXI7Oiwp7g&sa=X&ved=2ahUKEwj7vrSgktPmAhXF3J4KHTa_AFoQ_B0wEnoECAoQAw#imgrc=tmtmMVoERvLNrM:

set up express app
download and tag all job related emails
reduce each email to a bag of imp words

goal is to classify remainder from ~100 (use oversampling)
then rerun and see what accuracy averages (make 4way error box)
make sankey diagram


# Overview
this is a markdown file, still under construction! `@autogiftcard`.

# Inherency
Understanding the engagement of customers with businesses on social media presents a phenomenal opportunity for businesses active on these sites to gain customer insight and assemble valuable stores of data on existing customers & potential leads. This application takes advantage of this situation and aims to consume mentions data for IG business accounts and store this information in a database. 



# Structure 
It contains two main applications:
- autoGiftCardApp: This is the main application. Written with Node, Express, and Mongoose, and hosted as a Firebase Cloud Function, this app has been validated through my Facebook Developer Account as the endpoint URL for all update POST requests coming from the Instagram Webhook API product. Whenever my business account receives a mention on IG, my Firebase endpoint will accept the JSON payload and store the parsed information into a Mongo Atlas instance. 
- displayApp: This is a simple client application that displays all of the saved mentions, along with their client IDs. It was written with Node, Express, and Mongoose and is meant to be run locally.

# Installation
```Javascript
cd autoGiftCard
cd displayApp
npm install
npm start
```

# Running
Visit `localhost:4000` to see the application. 

# Testing
Ideally using `Postman`, you can send `POST` requests of the following format to this URL: `https://us-central1-autogiftcard.cloudfunctions.net/app`. You can modify the value of the `media_id` field, but maintain the format of the payload otherwise as it reflects the payload sent by the Webhook API. I am able to send this same data directly through the API's test capability from my dashboard.

Format:
```JSON
{
    "object": "instagram"
}
```

# Issues
- Webhook functionality... (`https://stackoverflow.com/questions/58545332/why-is-the-instagram-graph-api-webhook-not-working`)
# Improvements
- Gift
