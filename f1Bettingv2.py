import requests
from bs4 import BeautifulSoup
import re
import json

class SkyBets:
    def get_betting_odds(self):
        final_list = []
        request = requests.get('https://m.skybet.com/formula-1/dutch-gp/event/30137794')
        soup = BeautifulSoup(request.content, "html.parser")
        ul = soup.find("ul", {"class": "table-group"})
        lis = ul.find_all('li')
        for li in lis:
            if li is not None:
                h2 = (li.find("h2"))
                if h2 is not None:
                    table_title = (h2).text.strip()
                    if 'RequestABet' in table_title and 'RequestABets' not in table_title:
                        trs = li.find_all("tr")
                        for tr in trs:
                            tds = tr.find_all("td")
                            if len(tds) == 2:
                                final_list.append([tds[0].text.strip(), tds[1].find('span').text.strip()])
        return final_list


class DriverNotFoundException(Exception):
    pass

class PositionNotFoundException(Exception):
    pass


class StatisticalAnalysis:
    TO_WIN = 2.5
    PODIUM = 4
    TOP_6 = 7
    POINTS_FINISH = 11
    FINISH_RACE = 17
    f1_driver_results = {
        'Albon': (13,10,11),
        'Latifi': (16,16,16),
        'Leclerc': (1,2,1,6),
        'Sainz': (2,3,3),
        'Alonso': (9,17),
        'Ocon': (7,6,7,14),
        'Norris': (15,7,5,3),
        'Ricciardo': (14,6,18),
        'Hamilton': (4,10,4,13),
        'Russell': (3,5,3,4),
        'Verstappen': (1,1),
        'Perez': (4,2,2),
        'Schumacher': (11,13,17),
        'Magnussen': (5,9,14,9),
        'Tsunoda': (8,15,7),
        'Gasly': (8,9,12),
        'Vettel': (8,20),
        'Stroll': (12,13,12,10),
        'Bottas': (6,8,5),
        'Zhou': (10,11,11,15),
        'AlexAlbon': (13,10,11),
        'NicholasLatifi': (16,16,16),
        'CharlesLeclerc': (1,2,1,6),
        'CarlosSainz': (2,3,3),
        'FernandoAlonso': (9,17),
        'Ocon': (7,6,7,14),
        'LandoNorris': (15,7,5,3),
        'DanielRicciardo': (14,6,18),
        'LewisHamilton': (4,10,4,13),
        'GeorgeRussell': (3,5,3,4),
        'MaxVerstappen': (1,1),
        'SergioPerez': (4,2,2),
        'MickSchumacher': (11,13,17),
        'KevinMagnussen': (5,9,14,9),
        'Tsunoda': (8,15,7),
        'Gasly': (8,9,12),
        'SebastionVettel': (8,20),
        'LanceStroll': (12,13,12,10),
        'Bottas': (6,8,5),
        'Zhou': (10,11,11,15),
    }

    def __init__(self):
        self.driver_position = []

    def driver_average_placement(self):
        for key, value in self.f1_driver_results.items():
            print(key, 'Average place', (sum(value))/len(value))

    def _get_driver_name_from_string(self, string):
        for name in self.f1_driver_results.keys():
            if string.startswith(name):
                return name

    def get_driver_average(self, driver):
        return sum(self.f1_driver_results[driver]) / len(self.f1_driver_results[driver])

    def data_sorting(self, betting_odds):
        replacements = {
            "ToWin": self.TO_WIN,
            "towin": self.TO_WIN,
            "FastestLap": self.TO_WIN,
            "toWintheRace": self.TO_WIN,
            "Winner": self.TO_WIN,
            "Podium": self.PODIUM,
            "FinishonthePodium": self.PODIUM,
            "Top6Finish": self.TOP_6,
            "Top6": self.TOP_6,
            "PointsFinish": self.POINTS_FINISH,
            "PointFinish": self.POINTS_FINISH,
            "Points": self.POINTS_FINISH,
            "toScorePointsA": self.POINTS_FINISH,
            "toScorePoints": self.POINTS_FINISH,
            "AllPointsFinish": self.POINTS_FINISH,
            "Finsih": self.FINISH_RACE
        }
        bets = []

        for betting_string, odds in betting_odds:
            # betting_string='Hamilton To Win, Norris Top 6 Finish & Russell Points Finish'
            bet = {"original": betting_string, "parsed": []}
            betting_string = betting_string.replace(" ", "").replace(",", "").replace("&", "").replace(".", "").replace("SafetyCarintheRace", "")
            while betting_string != "":
                driver_names = []
                driver_position = None
                while name := self._get_driver_name_from_string(betting_string):
                    driver_names.append(name)
                    betting_string = betting_string[len(name):]
                if not driver_names:
                    raise DriverNotFoundException(betting_string)
                for key, value in replacements.items():
                    if betting_string.startswith(key):
                        betting_string = betting_string[len(key):]
                        driver_position = value
                if not driver_position:
                    raise PositionNotFoundException(betting_string)
                bet["parsed"].append([driver_names, driver_position])
            bets.append(bet)
        for bet in bets:
            place_bet = True
            for condition in bet["parsed"]:
                for driver in condition[0]:
                    if self.get_driver_average(driver) > condition[1]:
                        place_bet = False
            if place_bet:
                print(bet["original"])


sky_bets = SkyBets()
statistical_analysis = StatisticalAnalysis()
print (statistical_analysis.driver_average_placement())
betting_odds = sky_bets.get_betting_odds()
x = statistical_analysis.data_sorting(betting_odds)
