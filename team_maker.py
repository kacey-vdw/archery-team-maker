# sort helpers - used for sorting by total score
def byScore(player): # total score for 1 person
    return player[1]

def byPair(pair): # total score for two people
    return pair[0][1] + pair[1][1]

def byTeam(team): # total score for full team
    if team_type == 2:
        return byPair(team)
    else:
        return team[0][1] + team[1][1] + team[2][1]

def imbalance(teams): # how imbalanced is this arrangement?
    total_scores = [byTeam(team) for team in teams]
    return sum((total - ideal) ** 2 for total in total_scores) # return sum of difference from ideal ^2

# get data
file = open("data.txt")
data = file.read()
file.close()

team_type = 0
while (team_type != 2) and (team_type != 3):
    print("Teams of 2 or 3?: ")
    try:
        team_type = int(input())
    except ValueError:
        print("Please enter a number")

# make data into list of [name, score]
data = data.splitlines()
for item in range(0,len(data)):
    if (data[item] == "") or (data[item] == '\n'):
        data.pop(item)
    else:
        data[item] = data[item].split(",") # item in list is [Name, Score]
        try:
            data[item][1] = int(data[item][1].strip()) # convert Score to int, sanitising input
        except ValueError:
            print("ERROR: Your input data is invalid. Ensure the score values are numbers [line " + str(item+1) + "]")
            exit()
        except IndexError:
            print("ERROR: Please ensure your values are comma separated (SURNAME name,score) [line " + str(item+1) + "]")
            exit()

length = len(data)
ideal = (sum(byScore(player) for player in data) / length) * team_type # ideal total team score

if team_type == 3:
    # if the archers cannot be divided into teams of 3
    if length % 3 != 0:
        if length % 3 == 1:
            print("You have one extra person for teams of 3")
        if length % 3 == 2:
            print("You have one missing person for teams of 3")
        exit()
elif team_type == 2:
    # if the archers cannot be divided into teams of 2
    if length % 2 != 0:
        print("You have one extra/missing person for teams of 2")
        exit()

# ---------------------------

# sort scores from lowest to highest
data.sort(key=byScore)

#points for splitting the data
low_med_bound = int(length/team_type) # also the length of teams
if team_type == 3:
    med_high_bound = int(2*(length/team_type))

# the data split into groups
low_group = data[0:low_med_bound]
if team_type == 2:
    high_group = data[low_med_bound:length]
elif team_type == 3:
    med_group = data[low_med_bound:med_high_bound]
    high_group = data[med_high_bound:length]

# empty list, then pairs from high group and low group
teams = []
for i in range(low_med_bound):
    teams.append([low_group[i], high_group[low_med_bound - i -1]])
teams.sort(reverse=True, key=byPair)

if team_type == 3:
    # add lowest med to highest pair etc
    for i in range(low_med_bound):
        teams[i].append(med_group[i])
    teams.sort(key=byTeam)

# ---------------------------

# local search to refine
best_score = imbalance(teams)
improved = True
while improved:
    improved = False

    for i in range(low_med_bound):
        for j in range(i + 1, low_med_bound):
            for a in range(team_type):
                for b in range(team_type):
                    teams[i][a], teams[j][b] = teams[j][b], teams[i][a] # swap players
                    new_score = imbalance(teams)

                    if new_score < best_score: # if closer to ideal, hooray!
                        best_score = new_score
                        improved = True
                    else:
                        teams[i][a], teams[j][b] = teams[j][b], teams[i][a] # undo swap

teams.sort(key=byTeam)

# ---------------------------

# print teams in order of low to high, with number and total score, and write data to file
output = open("result.txt", "w")
output.write("") # empty existing file contents

output = open("result.txt", "a")

print("The ideal team total is: " + str(round(ideal)))
print("The difference between the top and bottom team is: " + str(byTeam(teams[int(length/team_type)-1]) - byTeam(teams[0])))

for index, team in enumerate(teams):
    print("Team", index+1, "-", byTeam(teams[index]))
    output.write("Team " + str(index+1) + " - " + str(byTeam(teams[index])) + "\n")
    
    for player in team:
        print("     ", player[0], "-", player[1])
        output.write("     " + str(player[0]) + " - " + str(player[1]) + "\n")
        
    print()
output.close()

print("The values have been saved to result.txt. Press enter to close this window.")
input()