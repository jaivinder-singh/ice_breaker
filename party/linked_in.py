import os
import requests
from dotenv import load_dotenv


def scrape_linked_in_profile(linkedin_profile_url: str, mock: bool = False):
    print("start")
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/jaivinder-singh/8aade1662db927836e73073849fd77cd/raw/92eb95da4ac3a9f62c31ee507479cbfbff45fb1f/test_profile.json"
        response = requests.get(linkedin_profile_url, timeout=10,)
       

    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        response = requests.get(
            api_endpoint,
            params={"url": linkedin_profile_url},
            headers=header_dic,
            timeout=10,
        )

    data = response.json()
    print("-------------------")
    print(data)
    print("-------------------")
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")


    return data


if(__name__ == "__main__"):
    print(
        scrape_linked_in_profile(linkedin_profile_url="https://www.linkedin.com/in/jaivinder-singh-21362657")
    )