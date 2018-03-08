import pickle
import operator

# 가정: 모든 사람들의 실력은 문제 푼 갯수에 비례한다.
# ability = number_of_AC ** 1.2
# 풀려있는 문제들을 ability를 이용해 difficulty를 산출한다.
# 역으로 사람들의 실력을 difficulty를 이용해 보정한다.
# '적절한' 횟수로 반복한다.

READING_RANKING_PAGE = 100
NUM_OF_USERS = READING_RANKING_PAGE * 100

ranking_list_file = open('ranklist.bin', 'rb')
solved_list_file = open('solvedlist.bin', 'rb')
rank_list = pickle.load(ranking_list_file) # int: [str]
solved_list = pickle.load(solved_list_file) # str: [int]

ability = dict() # str : [float]
difficulty = dict() # int : [float]
num_of_solved_users = [0 for _ in range(20000)] # list of int
mid = 0.0

def init():
    for i in range(1, 10000+1):
        ability[rank_list[i]] = len(solved_list[rank_list[i]]) ** 1.1
    train_difficulty()

# 푼 사람 수의 영향을 줄이기 위한 코드인데 부작용이 많아 제외
#    for i in range(20000):
#        if num_of_solved_users[i] > 0:
#            difficulty[i] /= num_of_solved_users[i]

def train_ability():
    # init()으로 만든 difficulty를 이용해 사용자들의 실력을 평가한다.
    ability.clear()
    for i in range(1, NUM_OF_USERS+1):
        for num in solved_list[rank_list[i]]:
            if rank_list[i] in ability: ability[rank_list[i]] += 100.0 / difficulty[num]
            else: ability[rank_list[i]] = 100.0 / difficulty[num]

def train_difficulty():
    # train_ability()로 만든 ability를 이용해 문제의 난이도를 평가한다.
    total = 0.0
    for i in range(1, NUM_OF_USERS+1):
        total += ability[rank_list[i]]
    mid = total / NUM_OF_USERS

    difficulty.clear()
    for i in range(1, NUM_OF_USERS+1):
        for num in solved_list[rank_list[i]]:
            num_of_solved_users[num] += 1
            if num in difficulty:
                difficulty[num] += mid / ability[rank_list[i]]
            else:
                difficulty[num] = mid / ability[rank_list[i]]

def print_problem_rank():
    sorted_diff = sorted(difficulty.items(), key=operator.itemgetter(1))[::-1]
    for k in sorted_diff:
        if k[0] in solved_list["mhkim4886"]: print("%d: %.3f AC" % (k[0], k[1]))
        else: print("%d: %.3f" % (k[0], k[1]))

def print_ability_rank():
    sorted_abil = sorted(ability.items(), key=operator.itemgetter(1))[::-1]
    for i in range(10000):
        print("#%d %s: %.3f" % (i+1, sorted_abil[i][0], sorted_abil[i][1]))

init()
for i in range(2):
    train_ability()
    train_difficulty()
    sorted_abil = sorted(ability.items(), key=operator.itemgetter(1))[::-1]
    for j in range(10000):
        if sorted_abil[j][0] == "mhkim4886": print("mhkim4886: Ranked #%d" % (j+1))
        if sorted_abil[j][0] == "kipa00": print("kipa00: Ranked #%d" % (j+1))

print_ability_rank()
print_problem_rank()
