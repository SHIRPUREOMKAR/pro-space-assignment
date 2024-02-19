# Pro-Space-Assignment

## Prerequisites

- Python 3.6 or higher
- Libraries: `requests`, `beautifulsoup4`, `selenium`

## Setup

1. Install the required Python libraries with pip:

    ```bash
    pip install requests beautifulsoup4 selenium
    ```

## Process

> The data requirements are:
> - Name
> - Current Position
> - Skills
> - LinkedIn URL
>    ___

<br>

1. Initially, I considered using the LinkedIn APIs available for public or developer use. However, they were either deprecated or not relevant (mostly for scraping jobs, not profiles).

2. The most relevant and straightforward method I found was to use Google search with some filters, such as:

    - The site filter "site:" as `"site:linkedin.com/in/" OR "site:linkedin.com/pub/"`
    - And since searching for profiles the intitle filter as `-intitle:"profiles`
    - The job profile as simply `"Software Developer"`
    - Email by adding `"@gmail.com" OR "@yahoo.com"`
    - Location can also be added as a field with `Software Developer` (not done for this case).

- Final `url` used was `https://www.google.com/search?q=+"Software+Developers" -intitle:"profiles" -inurl:"dir/+"+site:linkedin.com/in/+OR+site:linkedin.com/pub/`

<br>

3. By this method, for each person, majority of the data as `name`, `profile URL`, `email`, `position` is obtained. We just need to extract the data from parsing the request by passing the URL (in which we applied filters)


4. For the fields as `Current Position`, `Skills` and other possible data is a bit tough. But I thought to get it by now parsing the individual `profile URL`, since we git it in previous step.

5. I've used `Selenium` to prevent the cached count of requested pages as it opens a completely new Chromium window each time.

<br>

> Linked prevents the multiple requests for profiles without logging in. It also hides some of the data which can be only viewed through login. Also, there are popups whose classes are needed to be found to access the page. 

<br>

6. After this, most of the processing is to be done by parsing the data recieved, finding the spans containing data using `BeautifulSoup` library.

7. In the end we get all the required data, namely, `name`, `profile URL`, `Current Position`, `Skills`. I've also included the fields of `email`, `About`, `Past Experiences`, `Achievements`, which can be potentially useful later.

<br>

> The data of `emails`, `Past Experience`, etc are controversial but is Public so I've proceeded to collect it.