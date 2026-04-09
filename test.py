import math
import copy

def simulate_match(teama,team_a_rating,teamb,team_b_rating):
    # Simulate a match between team a and team b
    # Inputs; team a rating and team b rating
    # Output; result +1 means team a wins, -1 means team a loses
    # Ranking points exchange after match given result
    # based on probability according to initial rankins

    import random

    diff = team_a_rating - team_b_rating
    p_act = random.uniform(0, 1)
    p_win = 1 / (1 + 10 ** (-diff / 10))
    if p_act <= p_win:
        p = 1
        winner = teama
    else:
        p = -1
        winner = teamb

    if abs(diff) >= 10:
        diff = math.copysign(10,diff)
    delta = (-diff/10) +p

    return p, delta, winner


def simulate_pool(teams,rankings,order):
    points = [0, 0, 0, 0, 0]
    rankings_temp = rankings
    for i in order:
        indTeam1 = i[0]-1
        indTeam2 = i[1]-1
        # Simulate match
        result, delta, winner = simulate_match(teams[indTeam1],rankings[indTeam1],teams[indTeam2],rankings[indTeam2])
        # Update table
        points[indTeam1] += (1 + result)/2
        points[indTeam2] += (1 - result)/2 
        # Update ranking
        rankings_temp[indTeam1] += delta
        rankings_temp[indTeam2] -= delta

        table = list(zip(teams,rankings,points))
        table.sort(reverse = True, key=lambda x: (x[2], x[1]))
                                   
    return table[0][0], table[0][1], table[1][0], table[1][1]


# Input data for each pool and xchedule

teamsA = ["NZL", "FRA", "ITA", "URG", "NAM"]
rankingsA0 = [89.06, 89.22, 75.63, 66.63, 61.61]
orderA = [[2,1],[3,5],[2,4],[1,5],[3,4],[2,5],[4,5],[1,3],[1,4],[2,3]]

teamsB = ["IRE", "RSA", "SCO", "TON", "ROM"]
rankingsB0 = [91.82, 91.08, 84.01, 70.29, 64.56]
orderB = [[1,5],[2,3],[1,4],[2,5],[2,1],[3,4],[3,5],[2,4],[1,3],[4,5]]

teamsC = ["WAL", "AUS", "FIJ", "GEO", "POR"]
rankingsC0 = [78.26, 79.87, 80.28, 76.23, 68.61]
orderC = [[2,4],[1,3],[1,5],[2,3],[4,5],[1,2],[3,4],[2,5],[1,4],[3,5]]

teamsD = ["ENG", "JAP", "ARG", "SAM", "CHI"]
rankingsD0 = [79.95, 73.29, 80.86, 76.19, 60.49]
orderD = [[1,3],[2,5],[4,5],[1,2],[3,4],[1,5],[2,4],[3,5],[1,4],[2,3]]


# Main black, run stochastically for Nr runs and count wins
Nr = 10000
# List for counting
all_teams = teamsA + teamsB + teamsC + teamsD
all_teams_dict = {element: 0 for index, element in enumerate(all_teams)}

for i in range(Nr):

    


    # reinitialize rankings for each run
    rankingsA = copy.copy(rankingsA0)
    rankingsB = copy.copy(rankingsB0)
    rankingsC = copy.copy(rankingsC0)
    rankingsD = copy.copy(rankingsD0)


    # Simulate pools

    wA, rwA, ruA, rruA = simulate_pool(teamsA,rankingsA,orderA)
    wB, rwB, ruB, rruB = simulate_pool(teamsB,rankingsB,orderB)
    wC, rwC, ruC, rruC = simulate_pool(teamsC,rankingsC,orderC)
    wD, rwD, ruD, rruD = simulate_pool(teamsD,rankingsD,orderD)

    
    
    # Simulate quarter finals
    # Winner C bs runner-up D
    p, delta, winnerQF1 = simulate_match(wC,rwC,ruD,rruD)
    rwQF1 = ((1+p)/2)*rwC  + ((1-p)/2)*rwD + p*delta 

    # Winner B bs runner-up A
    p, delta, winnerQF2 = simulate_match(wB,rwB,ruA,rruA)
    rwQF2 = ((1+p)/2)*rwB  + ((1-p)/2)*rwA + p*delta 

    # Winner D bs runner-up C
    p, delta, winnerQF3 = simulate_match(wD,rwD,ruC,rruC)
    rwQF3 = ((1+p)/2)*rwD  + ((1-p)/2)*rwC + p*delta 

    # Winner A bs runner-up B
    p, delta, winnerQF4 = simulate_match(wA,rwA,ruB,rruB)
    rwQF4 = ((1+p)/2)*rwA  + ((1-p)/2)*rwB + p*delta 

    

    # Simulate semi finals
    # Winner QF1 bs winner QF2
    p, delta, winnerSF1 = simulate_match(winnerQF1,rwQF1,winnerQF2,rwQF2)
    rwSF1 = ((1+p)/2)*rwQF1  + ((1-p)/2)*rwQF2 + p*delta 

    # Winner QF3 vs winner QF4
    p, delta, winnerSF2 = simulate_match(winnerQF3,rwQF3,winnerQF4,rwQF4)
    rwSF2 = ((1+p)/2)*rwQF3  + ((1-p)/2)*rwQF4 + p*delta 


    # Simulate final
    # Winner SF1 bs winner SF2
    p, delta, Champion = simulate_match(winnerSF1,rwSF1,winnerSF2,rwSF2)
    rwSF1 = ((1+p)/2)*rwSF1  + ((1-p)/2)*rwSF2 + p*delta

    all_teams_dict[Champion] += 1
    


for key in all_teams_dict:
    prob = all_teams_dict[key]*100/Nr
    if prob > 1:
        print(key, prob)