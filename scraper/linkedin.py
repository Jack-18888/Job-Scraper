import requests
from bs4 import BeautifulSoup
from typing import List
from job import Job
import time

def remove_spaces(s: str):
    return s.lstrip().rstrip()


# define the fields
def get_jobs(location: str, keywords: List[str], cap: int) -> List[Job]:

    available_jobs = []

    def helper(start = 0):
        url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={'%20'.join(keywords)}&location={location}&start={start}"
        print(url)

        res = requests.get(url)

        if not res.ok: return

        soup = BeautifulSoup(res.text, "html.parser")

        jobs = soup.find_all("div", class_="base-card")

        for job in jobs:
            time.sleep(1)

            title = remove_spaces(job.find("h3", class_="base-search-card__title").get_text())
            company = remove_spaces(job.find("a", class_="hidden-nested-link").get_text())
            job_location = remove_spaces(job.find("span", class_="job-search-card__location").get_text())
            job_link = job.find("a", class_="base-card__full-link")["href"]
            job_scrape_result = scrape_job(job_link)
            if job_scrape_result: description, experience_level, employment_type = job_scrape_result
            else: continue

            if not title: title = "Unavailable"
            if not company: company = "Unavailable"
            if not job_location: job_location = "Unavailable"
            if not job_link: job_link = "Unavailable"
            if not description: description = "Unavailable"
            if not experience_level: experience_level = "Unavailable"
            if not employment_type: employment_type = "Unavailable"

            j = Job(title, job_location, company, description, experience_level, employment_type, job_link)

            available_jobs.append(j)

            if len(available_jobs) >= cap:
                return

        if not jobs: return
        return helper(start + len(jobs))

    helper()

    return available_jobs



def scrape_job(url: str) -> Job:
    print(url)
    res = requests.get(url)

    if not res.ok: return 

    soup = BeautifulSoup(res.text, "html.parser")

    description = soup.find("div", class_="show-more-less-html__markup").get_text()
    if not description: description = "Unavailable"
    experience_level = "Unavailable"
    employment_type = "Unavailable"

    criteria_lst = soup.find("ul", class_="description__job-criteria-list").find_all("li")
    for criteria in criteria_lst:
        criteria_header = remove_spaces(criteria.find("h3").get_text())
        criteria_text = remove_spaces(criteria.find("span").get_text())

        if criteria_header == "Seniority level": experience_level = criteria_text
        if criteria_header == "Employment type": employment_type = criteria_text

    if not experience_level: experience_level = "Unavailable"
    if not employment_type: employment_type = "Unavailable"

    return description, experience_level, employment_type


def save_as_csv(jobs: list[Job]):
    pass