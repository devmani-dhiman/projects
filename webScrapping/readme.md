This scrapper was built to scrape the job posted on facebook career page and was pushed to database for further process.

The scrapper uses Python requests, bs4, and html2text library to get the task completed.

Steps Involved in scrapper are: -

      1. Sending GET/POST (whichever is applicable) using the requests module of python.
      
      2. Parsing the response of the request using BeautifulSoup (BS) module.
      
      3. Extracting the relevent delails from the webpages using tags and converting the html format to text format using html2text module.
     
      4. The scrapped details was uploaded to MySQL database using mysql library in python.
