def win_probability(team_a_rating, team_b_rating):
    # Return probability of team a winning based on ranking
    #Inputs',' team A ranking, team A ranking
    #Output' probability of team A winning
    diff = team_a_rating - team_b_rating
    return 1 / (1 + 10 ** (-diff / 10))