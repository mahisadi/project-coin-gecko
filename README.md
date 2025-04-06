# project-coin-gecko

# Hosted Application link

[Crypto Dashboard ](https://d193fp0j30s8f9.cloudfront.net/)

# How to Run and Test:

## For UI:

1) Go to the UI folder.  
2) To install dependencies, run the command - `npm install`.  
3) To run the server locally, run the command - `npm run serve`.  
4) This will directly make requests to the hosted backend.  

## For Backend:

1) Go to the backend folder.  
2) Create a virtual environment: `python -m venv venv`.  
3) Activate the virtual environment: `source venv/bin/activate`.  
4) To install dependencies, run the command - `pip install -r requirements.txt`.  
5) From the command line, run (to mimic DynamoDB):  
   i) `pip install localstack`  
   ii) `localstack start`  
6) To run a specific request, go to `ServiceManager` (ServiceLayer).  
7) Define the function you would like to call, e.g., below:  
    ```python
    response = ServiceManager().fetch_coin_dataset("Bitcoin", "USD")
    print("response", response)
    ```  
8) Use the debugger (launch.json, added to git) to run `service_manager.py`. 
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debugger",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/backend/service/service_manager.py",
            "console": "integratedTerminal",
            "env": {
                "PYTHONPATH": "${workspaceFolder}/backend",
                "IS_LOCAL": "true",
                "COIN_CURRENCY_TRACKER_TABLE": "CryptoCurrencyTracker",
                "API_URL_BASE_PATH": "https://api.coingecko.com/api/v3",
                "API_PRICE_RESOURCE_PATH": "/simple/price"
            }
        }
    ]
}
```
9) Replace your `COIN_GECKO_API_KEY` at `API_KEY = None`, so you don't need to call AWS Secrets Manager.  
10) We'll see the expected results for the `fetch_coin_price` operation only, as others rely on the Persistence Layer (DynamoDB).  

# Project Architecture
[Project Architecture](https://github.com/mahisadi/project-coin-gecko/blob/master/coin_dashboard_archirecture.png)

# Functional Requirements (As per the instructions)

1) It should provide the price for a given combination (e.g., bitcoin, usd).  
    * Using the CoinGecko API, I am able to fetch data from CoinGecko and, before sending, store it in DynamoDB.  
    * This stored data will have a TTL (Time to Live) for 24 hours (I am only maintaining data for 24 hours).  
    * If needed, it can be coded to consider that particular day's data.  
2) It should provide the dataset of the previous 24 hours of collected data for the requested combination.  
    * I'm using datasets in DynamoDB and sending them in the format of price and dateTime. This data can be displayed on the charts.  
3) It should calculate the ranks for the previously requested combination based on standard deviation.  
    * Dynamically generating ranks using the datasets above.  
    * Sorting (reverse) based on the deviation and adding ranks for the sorted items.

# Non-Functional Requirements:

* AWS Services Used:  
    * Backend - API Gateway, Lambda, DynamoDB, CloudWatch.  
    * UI - CloudFront, Route53, S3 (hosting website).  
* Scaling:  
    * All of the used services are serverless.  
    * Lambda:  
        * Can adjust concurrency.  
        * Cold start - ping every 5 minutes.  
    * API-GW:  
        * Throttling to control the number of requests per second.  
        * Quota adjustments, such as 100k requests per day.  
    * DynamoDB:  
        * On-demand capacity to handle loads.

# Assumptions:

* I assumed a 24-hour period for data, with a TTL set for every stored record.  
* Only show ranks and collected prices over the 24-hour period with stored data.  
* We don't need different tables. I felt like only one table is needed, and we can calculate responses during runtime with the fetched data.  
* There may be some issues with load testing and manual UI testing due to some unknown issues.  
* I didn't cover unit and integration test cases (technical debt).

# Next Steps:

* It's dev-ready. Considering the non-functional requirements (scalability), it's PROD-ready.  
* Cover unit and integration test cases.
* Need to wrapup CICD setup, creating alias for both backend and ui.
* Enhancements:  
    * We can make this a personal application with a signup feature.  
    * We can store the portfolio and send notifications for the marked price.  
    * For this, we may need to run a scheduler that runs every 5 seconds to call CoinGecko APIs.  
    * If we have the scheduler, we don't need to call the CoinGecko API for price check requests. Instead, we can query DynamoDB for the latest coin-price combo record.

# Use of Coding Assistant Tools:

* I typically use ChatGPT or other LLM assistants to answer questions about software, as a “better than Google and Stack Overflow” search tool. I am doing the same during this exercise.  
* I use ChatGPT or other LLM assistants for grammar corrections for my text with the phrase "Just do grammar corrections for the below text..."

# Time spent on the assignment
* Approx 10 hours