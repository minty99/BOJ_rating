import requests
from bs4 import BeautifulSoup
import pickle
import time

READING_RANKING_PAGE = 2

def get_AC_List(username):
    resp = requests.get('https://www.acmicpc.net/user/' + username)
    html = resp.text
    soup = BeautifulSoup(html, 'html.parser')
    all_prob = soup.select("div.col-md-9 > div > div.panel-body")
    prob_ac = all_prob[0].select("span.problem_number > a")
    ret = []
    for t in prob_ac:
        ret += [ int(t.text) ]
    return ret

def get_Ranklist(n):
    resp = requests.get('https://www.acmicpc.net/ranklist/' + str(n))
    html = resp.text
    soup = BeautifulSoup(html, 'html.parser')
    ranklist = soup.select("div.table-responsive > table > tbody > tr")
    ret = []
    for i in range(100):
        name = ranklist[i].select("td")[1].select("a")[0]
        ret += [ name.get("href")[6:] ]
    return ret

print("BOJ Parser")
print("1. Refresh ranking and user data")
print("2. Get data from database and print the data")
print("Your Selection:", end=" ")
sel = int(input())

if sel == 1:
    rank_list = dict() # int: [str]
    for i in range(1, READING_RANKING_PAGE+1):
        rlist = get_Ranklist(i)
        for j in range(1, 100+1):
            rank_list[(i-1)*100 + j] = rlist[j-1]
        print("Ranking: %d page parsing completed." % i)

    solved_list = dict() # str: [int]
    for i in range(1, READING_RANKING_PAGE*100+1):
        solved_list[rank_list[i]] = get_AC_List(rank_list[i])
        print("Rank %d: AC list parsing completed." % i)

    ranking_list_file = open('ranklist.bin', 'wb')
    solved_list_file = open('solvedlist.bin', 'wb')
    pickle.dump(rank_list, ranking_list_file)
    pickle.dump(solved_list, solved_list_file)

if sel == 2:
    ranking_list_file = open('ranklist.bin', 'rb')
    solved_list_file = open('solvedlist.bin', 'rb')
    rank_list = pickle.load(ranking_list_file)
    solved_list = pickle.load(solved_list_file)

    print("Print rank_list? (Y/N)", end=" ")
    s = input()
    if s == 'Y' or s == 'y': print(rank_list)
    
    print("Print solved_list? (Y/N)", end=" ")
    s = input()
    if s == 'Y' or s == 'y': print(solved_list)
