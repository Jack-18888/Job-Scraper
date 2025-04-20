class Job:
    def __init__(self, title: str, location: str, company: str, 
                 description: str, experience: str, jobType: str, url: str):
        self.title = title
        self.location = location
        self.company = company
        self.experience = experience # entry, associate, senior ...
        self.jobType = jobType # full time part time ...
        self.description = description
        self.url = url

    def print_info(self):
        print("-----------------------------------------------")
        print(f"Title: {self.title}")
        print(f"Location: {self.location}")
        print(f"Company: {self.company}")
        print(f"Experience Requirements: {self.experience}")
        print(f"Job Type: {self.jobType}")
        # print(f"Description: {self.description}")
        print("-----------------------------------------------")