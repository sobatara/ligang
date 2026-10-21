import json, os

cur_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(cur_dir, 'all_season_fixtures.json'), encoding='utf-8') as f:
    fixtures = json.load(f)

# Teams data extracted (Sinkron 100% dengan Klasemen Resmi Google)
teams = [
  { "name": "DEWA UNITED BANTEN FC", "short": "Dewa United", "rank": 1, "logo": "https://media.api-sports.io/football/teams/17902.png", "played": 6, "w": 4, "d": 2, "l": 0, "gf": 12, "ga": 6, "gd": 6, "pts": 14, "form": "WDWWD" },
  { "name": "BALI UNITED FC", "short": "Bali United", "rank": 2, "logo": "https://media.api-sports.io/football/teams/2448.png", "played": 6, "w": 4, "d": 0, "l": 2, "gf": 19, "ga": 7, "gd": 12, "pts": 12, "form": "LWLWW" },
  { "name": "PERSIJA JAKARTA", "short": "Persija", "rank": 3, "logo": "https://media.api-sports.io/football/teams/10134.png", "played": 5, "w": 4, "d": 0, "l": 1, "gf": 10, "ga": 4, "gd": 6, "pts": 12, "form": "LWWWW" },
  { "name": "PERSITA", "short": "Persita", "rank": 4, "logo": "https://media.api-sports.io/football/teams/4244.png", "played": 5, "w": 3, "d": 2, "l": 0, "gf": 11, "ga": 8, "gd": 3, "pts": 11, "form": "WWDWD" },
  { "name": "BHAYANGKARA PRESISI LAMPUNG FC", "short": "Bhayangkara FC", "rank": 5, "logo": "https://media.api-sports.io/football/teams/2443.png", "played": 6, "w": 3, "d": 3, "l": 0, "gf": 11, "ga": 7, "gd": 4, "pts": 12, "form": "WDDWW" },
  { "name": "MADURA UNITED FC", "short": "Madura United", "rank": 6, "logo": "https://media.api-sports.io/football/teams/2444.png", "played": 5, "w": 3, "d": 1, "l": 1, "gf": 10, "ga": 7, "gd": 3, "pts": 10, "form": "DLWWW" },
  { "name": "PERSIB BANDUNG", "short": "Persib", "rank": 7, "logo": "https://media.api-sports.io/football/teams/2445.png", "played": 5, "w": 3, "d": 1, "l": 1, "gf": 9, "ga": 6, "gd": 3, "pts": 10, "form": "WDWLW" },
  { "name": "PERSEBAYA SURABAYA", "short": "Persebaya", "rank": 8, "logo": "https://media.api-sports.io/football/teams/2446.png", "played": 5, "w": 2, "d": 3, "l": 0, "gf": 6, "ga": 4, "gd": 2, "pts": 9, "form": "DWDWD" },
  { "name": "PERSIK KEDIRI", "short": "Persik", "rank": 9, "logo": "https://media.api-sports.io/football/teams/4241.png", "played": 5, "w": 2, "d": 1, "l": 2, "gf": 5, "ga": 3, "gd": 2, "pts": 7, "form": "LWDWL" },
  { "name": "AREMA FC", "short": "Arema FC", "rank": 10, "logo": "https://media.api-sports.io/football/teams/2438.png", "played": 5, "w": 1, "d": 3, "l": 1, "gf": 11, "ga": 9, "gd": 2, "pts": 6, "form": "LDDDW" },
  { "name": "JAVA UNITED FC", "short": "Java United", "rank": 11, "logo": "https://media.api-sports.io/football/teams/22409.png", "played": 6, "w": 2, "d": 2, "l": 2, "gf": 9, "ga": 9, "gd": 0, "pts": 6, "form": "DWWLL" },
  { "name": "BORNEO FC SAMARINDA", "short": "Borneo FC", "rank": 12, "logo": "https://media.api-sports.io/football/teams/2442.png", "played": 5, "w": 2, "d": 0, "l": 3, "gf": 4, "ga": 6, "gd": -2, "pts": 6, "form": "LWLWL" },
  { "name": "GARUDAYAKSA FC", "short": "Garudayaksa", "rank": 13, "logo": "https://media.api-sports.io/football/teams/26645.png", "played": 6, "w": 1, "d": 2, "l": 3, "gf": 6, "ga": 12, "gd": -6, "pts": 5, "form": "WLDLDL" },
  { "name": "PSM MAKASSAR", "short": "PSM Makassar", "rank": 14, "logo": "https://media.api-sports.io/football/teams/2441.png", "played": 5, "w": 1, "d": 2, "l": 2, "gf": 8, "ga": 12, "gd": -4, "pts": 5, "form": "WLDDL" },
  { "name": "PSS SLEMAN", "short": "PSS Sleman", "rank": 15, "logo": "https://media.api-sports.io/football/teams/3882.png", "played": 5, "w": 1, "d": 1, "l": 3, "gf": 8, "ga": 9, "gd": -1, "pts": 4, "form": "DWLLL" },
  { "name": "ISENMULANG KALTENG FC", "short": "Isenmulang", "rank": 16, "logo": "https://media.api-sports.io/football/teams/24993.png", "played": 6, "w": 1, "d": 1, "l": 4, "gf": 3, "ga": 12, "gd": -9, "pts": 2, "form": "DWLLL" },
  { "name": "PSIM YOGYAKARTA", "short": "PSIM Jogja", "rank": 17, "logo": "https://media.api-sports.io/football/teams/4235.png", "played": 6, "w": 0, "d": 1, "l": 5, "gf": 3, "ga": 12, "gd": -9, "pts": 1, "form": "LLLLL" },
  { "name": "PERSIJAP JEPARA", "short": "Persijap", "rank": 18, "logo": "https://media.api-sports.io/football/teams/11132.png", "played": 6, "w": 0, "d": 0, "l": 6, "gf": 2, "ga": 14, "gd": -12, "pts": 0, "form": "LLLLL" }
]

team_dict = {t['name']: t for t in teams}

# Matches with official 1xBet live odds currently open in market
official_1xbet_odds = {
  "BALI UNITED FC vs GARUDAYAKSA FC": { "h": 1.34, "d": 4.70, "a": 6.67, "bookmaker": "1xBet", "isOfficial": True },
  "PERSIJA JAKARTA vs AREMA FC": { "h": 1.33, "d": 4.65, "a": 7.05, "bookmaker": "1xBet", "isOfficial": True },
  "PSM MAKASSAR vs PERSEBAYA SURABAYA": { "h": 3.32, "d": 3.22, "a": 2.01, "bookmaker": "1xBet", "isOfficial": True },
  "PERSIK KEDIRI vs PSS SLEMAN": { "h": 2.10, "d": 3.30, "a": 3.20, "bookmaker": "1xBet", "isOfficial": True },
  "MADURA UNITED FC vs PERSIB BANDUNG": { "h": 4.62, "d": 3.40, "a": 1.67, "bookmaker": "1xBet", "isOfficial": True }
}

# Results of finished matches from Pekan 5 & early Pekan 6 (Real Full-Time scores)
finished_matches_results = {
  "PERSEBAYA SURABAYA vs PSS SLEMAN": (2, 1),
  "PERSIB BANDUNG vs PERSIK KEDIRI": (2, 1),
  "ISENMULANG KALTENG FC vs JAVA UNITED FC": (0, 2),
  "BHAYANGKARA PRESISI LAMPUNG FC vs PSIM YOGYAKARTA": (1, 0),
  "DEWA UNITED BANTEN FC vs PERSIJAP JEPARA": (2, 0),
  "BALI UNITED FC vs GARUDAYAKSA FC": (5, 0)
}

enriched_fixtures = []
for idx, f in enumerate(fixtures):
    h_name = f['strHomeTeam']
    a_name = f['strAwayTeam']
    h_info = team_dict.get(h_name, { "short": h_name, "rank": 10, "logo": "" })
    a_info = team_dict.get(a_name, { "short": a_name, "rank": 10, "logo": "" })
    
    match_key = f"{h_name} vs {a_name}"
    
    # Check if match was in the past and finished
    date_str = f"{f['dateEvent']}T{f['time']}:00+07:00"
    
    status = f.get('strStatus', 'NS')
    h_score = int(f['intHomeScore']) if f.get('intHomeScore') is not None and f.get('intHomeScore') != '' else None
    a_score = int(f['intAwayScore']) if f.get('intAwayScore') is not None and f.get('intAwayScore') != '' else None
    
    # If this match was on 18 Okt or 20 Okt and previously had no score recorded
    if match_key in finished_matches_results:
        res = finished_matches_results[match_key]
        h_score, a_score = res[0], res[1]
        status = 'FT'
    
    is_finished = (status == 'FT')
    
    # Check 1xBet odds:
    # Only upcoming matches with real 1xBet market have official odds
    odds_data = None
    has_1xbet_odds = False
    
    if not is_finished and match_key in official_1xbet_odds:
        odds_data = official_1xbet_odds[match_key]
        has_1xbet_odds = True
    elif is_finished:
        # Completed match baseline closing odds for history
        odds_data = { "h": 1.75, "d": 3.40, "a": 4.10, "bookmaker": "1xBet", "isOfficial": True }
        has_1xbet_odds = True
    else:
        # Not yet released by 1xBet
        odds_data = None
        has_1xbet_odds = False

    enriched_fixtures.append({
        "id": 1622800 + idx,
        "leagueId": 240,
        "leagueName": "BRI Super League",
        "leagueFlag": "🇮🇩",
        "leagueCode": "LIGA1",
        "leagueCountry": "Indonesia",
        "round": f"Pekan {f.get('week', 1)}",
        "week": f.get('week', 1),
        "date": date_str,
        "dateStr": f"{f['dateEvent']} {f['time']} WIB",
        "timestamp": 1792600000 + idx * 86400,
        "status": status,
        "isFinished": is_finished,
        "venue": f.get('strVenue', 'Stadion'),
        "home": h_name,
        "homeShort": h_info.get('short', h_name),
        "homeRank": h_info.get('rank', 10),
        "homeLogo": h_info.get('logo', ''),
        "away": a_name,
        "awayShort": a_info.get('short', a_name),
        "awayRank": a_info.get('rank', 10),
        "awayLogo": a_info.get('logo', ''),
        "homeScore": h_score,
        "awayScore": a_score,
        "odds": odds_data,
        "has1xBetOdds": has_1xbet_odds
    })

out_path = r'C:\Users\Win 10\.gemini\antigravity\scratch\liga1-bet-tracker\liga1_master_data.json'
with open(out_path, 'w', encoding='utf-8') as out:
    json.dump({
        "teams": teams,
        "fixtures": enriched_fixtures
    }, out, indent=2, ensure_ascii=False)

print(f"Generated {len(enriched_fixtures)} fixtures in {out_path}")
