import csv
import os.path
import lxml
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from multiprocessing import Pool
import requests


url = 'https://www.flashscore.com/'

driver = webdriver.Chrome()
driver.get(url + 'tennis')

matches = driver.find_elements_by_class_name('event__match')
ids = []

res = []

for match in matches:
    ids.append(match.get_attribute('id').split('_')[2])


def write_csv(res):
    dt = datetime.datetime.now().strftime('%d_%m_%Y')
    with open(f'{str(dt)}.csv', 'w', newline='') as f:
        a = csv.writer(f, delimiter=';')
        for i in res:
            row = []
            for key in i:
                row.append(i[key])
            a.writerow(row)


def get_date_info(id):
    try:
        info = {}
        it_url = url + 'match/' + str(id) + '#match-summary/match-summary'
        try:
            print(f"{ids.index(id)+1}/{len(ids)-1}")
        except:
            pass
        driver.get(it_url)
        time.sleep(1)
        info['tournament'] = driver.find_element_by_class_name('tournamentHeader__country').text.replace('\n', '')
        info['datetime'] = driver.find_element_by_class_name('duelParticipant__startTime').text
        info['player1_name'] = driver.find_elements_by_class_name('participant__participantName')[0].text.\
            replace('\n', '')
        info['player2_name'] = driver.find_elements_by_class_name('participant__participantName')[2].text.\
            replace('\n', '')
        try:
            info['player1_ATP'] = driver.find_elements_by_class_name('participant__participantRank')[0].text.\
                replace('\n', '')
        except:
            info['player1_ATP'] = '-'
        try:
            info['player2_ATP'] = driver.find_elements_by_class_name('participant__participantRank')[1].text.\
                replace('\n', '')
        except:
            info['player2_ATP'] = '-'

        info['game_status'] = driver.find_elements_by_class_name('fixedHeaderDuel__detailStatus')[-1].text
        info['player1_total_score'] = "-"
        info['player1_part1_score'] = "-"
        info['player1_part2_score'] = "-"
        info['player1_part3_score'] = "-"
        info['player1_part4_score'] = "-"
        info['player1_part5_score'] = "-"

        info['player2_total_score'] = "-"
        info['player2_part1_score'] = "-"
        info['player2_part2_score'] = "-"
        info['player2_part3_score'] = "-"
        info['player2_part4_score'] = "-"
        info['player2_part5_score'] = "-"

        if 'Finished' in info['game_status']:
            home_score = driver.find_elements_by_class_name('smh__home')
            info['player1_total_score'] = home_score[2].text
            info['player1_part1_score'] = home_score[3].text
            info['player1_part2_score'] = home_score[5].text
            info['player1_part3_score'] = home_score[7].text
            info['player1_part4_score'] = home_score[9].text
            info['player1_part5_score'] = home_score[11].text
            away_score = driver.find_elements_by_class_name('smh__away')
            info['player2_total_score'] = away_score[2].text
            info['player2_part1_score'] = away_score[3].text
            info['player2_part2_score'] = away_score[5].text
            info['player2_part3_score'] = away_score[7].text
            info['player2_part4_score'] = away_score[9].text
            info['player2_part5_score'] = away_score[11].text
        try:
            info['odd1'] = driver.find_elements_by_class_name('oddsValue')[0].text.replace('.', ',')
            info['odd2'] = driver.find_elements_by_class_name('oddsValue')[1].text.replace('.', ',')
        except:
            info['odd1'] = '-'
            info['odd2'] = '-'
        info['url'] = it_url
        res.append(info)
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    print('начинаем.')
    res = []
    for id in ids:
        get_date_info(id)
    write_csv(res)
    driver.quit()
    print('gotovo, записываю в таблицу...')
