from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Enable CORS for your Chrome extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your extension origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "PUT_YOUR_HUNTER_API_KEY_HERE"  # replace with your Hunter.io key


@app.post("/fetch")
async def fetch_data(request: Request):
    print("/fetch endpoint called")

    body = await request.json()
    org = body.get("organisation", "").strip()
    full_name = body.get("fullName", "").strip()

    print(f"Received organisation: {org}, full_name: {full_name}")

    if not org or org.lower() == "n/a":
        raise HTTPException(
            status_code=400,
            detail="Organisation not provided or could not be extracted from LinkedIn profile."
        )

    # Check for generic terms
    generic_terms = [
        "performance management", "human resources", "hr", "talent acquisition",
        "employee engagement", "operations", "branding", "intelligence", "strategy",
        "compliance", "recruitment", "department", "team", "group", "division"
    ]
    if any(term in org.lower() for term in generic_terms):
        return {
            "email": None,
            "organisation": org,
            "domain": None,
            "message": "Organisation appears to be a generic term. Please provide a valid company name."
        }

    # Ensure domain is valid
    domain = org.lower().replace(' ', '')
    if not any(domain.endswith(ext) for ext in ['.com', '.net', '.org', '.in', '.co', '.ai', '.io']):
        domain += '.com'
    print(f"Using domain: {domain}")

    # Call Hunter.io Domain Search API
    url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={API_KEY}"
    print(f"Calling Hunter.io domain search API: {url}")
    try:
        res = requests.get(url)
        print(f"Domain search response status: {res.status_code}")
        print(f"Domain search response text: {res.text}")
        data = res.json()
    except Exception as domain_e:
        raise HTTPException(status_code=500, detail=f"Hunter.io Domain Search API error: {domain_e}")

    # Split name
    first_name, last_name = "", ""
    if full_name:
        name_parts = full_name.split()
        if len(name_parts) > 1:
            first_name, last_name = name_parts[0], name_parts[-1]
        elif len(name_parts) == 1:
            first_name = name_parts[0]

    print(f"Trying Hunter.io Email Finder with: domain={domain}, first_name={first_name}, last_name={last_name}, full_name={full_name}")

    # Try Email Finder
    email = None
    try:
        if first_name and last_name:
            finder_url = f"https://api.hunter.io/v2/email-finder?domain={domain}&first_name={first_name}&last_name={last_name}&api_key={API_KEY}"
        else:
            finder_url = f"https://api.hunter.io/v2/email-finder?domain={domain}&full_name={full_name}&api_key={API_KEY}"

        print(f"Requesting: {finder_url}")
        finder_res = requests.get(finder_url)
        print(f"Email finder response status: {finder_res.status_code}")
        print(f"Email finder response text: {finder_res.text}")
        finder_data = finder_res.json()
        if "data" in finder_data and "email" in finder_data["data"]:
            email = finder_data["data"]["email"]
    except Exception as api_e:
        print("Error calling Hunter.io Email Finder API:", api_e)

    # Fallback to domain search
    email_list = []
    if not email and "data" in data and "emails" in data["data"] and data["data"]["emails"]:
        email_list = [email_obj.get("value") for email_obj in data["data"]["emails"] if "value" in email_obj]

    if email:
        return {"email": email, "organisation": org, "domain": domain}
    elif email_list:
        return {"emails": email_list, "organisation": org, "domain": domain}
    else:
        return {
            "emails": [],
            "organisation": org,
            "domain": domain,
            "message": "No emails found for this organisation/domain/person."
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
