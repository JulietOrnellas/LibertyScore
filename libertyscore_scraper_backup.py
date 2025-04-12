

# Liberty Score parser
    # Finds the Liberty Score
def get_liberty_score(name):
    url = f"https://libertyscore.conservativereview.com/{name.lower().replace(' ', '-')}"
    response = requests.get(url)
    if response.status_code != 200:
        return "Could not retrieve Liberty Score"
    
    
    soup = BeautifulSoup(response.text, 'html.parser')
    score_div = soup.find("div", class_="score-card-score")
    return score_div.text.strip() if score_div else "Liberty Score not found."
