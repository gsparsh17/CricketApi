from flask import Flask, render_template, jsonify
import requests
from flask_cors import CORS
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

@app.route('/api/live-score', methods=['GET'])
def home():
    # URL of Cricbuzz's live score page
    url = "https://www.cricbuzz.com/cricket-match/live-scores"

    # Send a GET request to the Cricbuzz URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Scrape the necessary data from the HTML
    # Example: Finding the first live score card
#     score_section = soup.find('div', class_='cb-mtch-lst')
#     score_section1 = soup.find('div', class_='cb-scr-wll-chvrn')
    
#     if score_section:
#         match_title = score_section.find('h3', class_='cb-lv-scr-mtch-hdr').text.strip()
#         print(match_title)
#         # live_score1 = score_section1.find('div', class_='cb-ovr-flo').text.strip()
#         # print(live_score1)
#         # live_score2 = score_section1.find_next_sibling('div', class_='cb-ovr-flo').text.strip()
#         # print(live_score2)
#         batting_team = score_section1.find('div', class_='cb-hmscg-bat-txt cb-ovr-flo')
#         batting_team_name = batting_team.find('div', class_='cb-ovr-flo cb-hmscg-tm-nm').text.strip()
#         batting_team_score = batting_team.find_all('div', class_='cb-ovr-flo')[1].text.strip()

# # Scraping the bowling team's score
#         bowling_team = score_section1.find('div', class_='cb-hmscg-bwl-txt')
#         bowling_team_name = bowling_team.find('div', class_='cb-ovr-flo cb-hmscg-tm-nm').text.strip()
#         bowling_team_score = bowling_team.find_all('div', class_='cb-ovr-flo')[1].text.strip()

# # Scraping the match result
#         match_result = soup.find('div', class_='cb-text-complete').text.strip()

    match_section = soup.find('div', class_='cb-mtch-lst cb-col cb-col-100 cb-tms-itm')

    if match_section:
        match_title_element = match_section.find('h3', class_='cb-lv-scr-mtch-hdr')
        match_title = match_title_element.text.strip() if match_title_element else 'No Match Title Found'

        match_title_element2 = match_section.find('span', class_='text-gray')
        match_title2 = match_title_element2.text.strip() if match_title_element2 else 'No Match Title Found'
        
        # Extract match time and venue
        match_time_element = match_section.find('span', class_='ng-binding')
        match_time = match_time_element.text.strip() if match_time_element else 'No Match Time Found'
        
        # Extract score details
        score_section = match_section.find('div', class_='cb-scr-wll-chvrn cb-lv-scrs-col')
        if score_section:
            batting_team = score_section.find('div', class_='cb-hmscg-bat-txt cb-ovr-flo')
            batting_team_name = batting_team.find('div', class_='cb-ovr-flo cb-hmscg-tm-nm').text.strip()
            batting_team_score = batting_team.find_all('div', class_='cb-ovr-flo')[1].text.strip()

            bowling_team = score_section.find('div', class_='cb-hmscg-bwl-txt')
            bowling_team_name = bowling_team.find('div', class_='cb-ovr-flo cb-hmscg-tm-nm').text.strip()
            bowling_team_score = bowling_team.find_all('div', class_='cb-ovr-flo')[1].text.strip() if len(bowling_team.find_all('div', class_='cb-ovr-flo')) > 1 else 'Not Available'

            match_result = score_section.find('div', class_='cb-text-live').text.strip() if score_section.find('div', class_='cb-text-live') else 'Result Not Available'

# Printing the results
            print(f"{batting_team_name}: {batting_team_score}")
            print(f"{bowling_team_name}: {bowling_team_score}")
            print(f"Result: {match_result}")

        else:
            batting_team_name = 'Not Available'
            batting_team_score = 'Not Available'
            bowling_team_name = 'Not Available'
            bowling_team_score = 'Not Available'
            match_result = 'Not Available'

        data = {
            'match_title': match_title,
            'match_title2': match_title2,
            'match_time': match_time,
            'batting_team_name': batting_team_name,
            'batting_team_score': batting_team_score,
            'bowling_team_name': bowling_team_name,
            'bowling_team_score': bowling_team_score,
            'match_result': match_result
        }

        return jsonify(data)
    else:
        match_title = "No Live Match Found"

    # Pass the scraped data to the HTML template
    return render_template('index.html', match_title=match_title, match_title2=match_title2, batting_team_name=batting_team_name, batting_team_score=batting_team_score, bowling_team=bowling_team, bowling_team_name=bowling_team_name, bowling_team_score=bowling_team_score, match_result=match_result)

if __name__ == '__main__':
    app.run(debug=True)
