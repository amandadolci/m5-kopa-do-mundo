from datetime import datetime as dt
from exceptions import (NegativeTitlesError,
                        ImpossibleTitlesError,
                        InvalidYearCupError)


def data_processing(country_team):
    if country_team['titles'] < 0:
        raise NegativeTitlesError('titles cannot be negative')

    wc_years = list(range(1930, dt.now().year, 4))
    first_cup = dt.strptime(country_team['first_cup'], '%Y-%m-%d')
    if first_cup.year not in wc_years:
        raise InvalidYearCupError('there was no world cup this year')

    first_cup_index = wc_years.index(first_cup.year)
    if country_team['titles'] > len(wc_years[first_cup_index:]):
        raise ImpossibleTitlesError(
            'impossible to have more titles than disputed cups'
            )
