import os
import requests
from dotenv import load_dotenv


def scrape_linked_in_profile(linkedin_profile_url: str, mock: bool = False):
    print("start")
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/jaivinder-singh/e64fa1a706891646bd90265bfc9f945a/raw/daa2c8b31019999a63787ab5c0d5eb2cc1cb2f12/test_profile.json"
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
        scrape_linked_in_profile(linkedin_profile_url="https://www.linkedin.com/in/eden-marco",mock=True)
    )