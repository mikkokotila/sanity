def will_bid(percent):
    return random.randrange(100) < percent

def get_truncated_normal(mean=0, sd=1, low=0, upp=10):

    from scipy.stats import truncnorm
    
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)

def player_specs(n):

    players = np.zeros([n, 6])

    # create player max_bids
    values = get_truncated_normal(10.1, 9.9, 0.2, 20)
    players[:,0] = values.rvs(n)

    # create player budget columns
    values = get_truncated_normal(200, 450, 50, 500)
    
    # starting budget
    players[:,1] = values.rvs(n)
    
    # running budget
    players[:,2] = players[:,1]
    
    # fill rate
    values = get_truncated_normal(50, 80, 10, 90)
    players[:,3] = values.rvs(n)
    
    return players

# create the players
players = player_specs(100)

# sort the players into order by max_bid
players = players[players[:,0].argsort()]

# get the site data
programmatic = dedomena.datasets.autonomio('programmatic_ad_fraud')
data = programmatic[['cpm', 'score_median']].dropna().values

# create running index for sites
sites = len(data)

while True:

    # get the site with ask
    site = data[random.randint(0, sites-1)]

    # get the actual ask for impression
    ask = site[0]
    impression_cost = ask / 1000

    # who bids for the impression
    potential_bidders = np.where(players[:,0] >= ask)[0]

    # will they bid
    for bidder in potential_bidders:
        
        # enough budget is left
        if players[bidder][2] < impression_cost:
            potential_bidders = potential_bidders[potential_bidders !=  bidder]

        # is currently active
        if will_bid(players[bidder][3]) is False:
            potential_bidders = potential_bidders[potential_bidders !=  bidder]
            
    # who has the highest bid?
    if len(potential_bidders) > 0:
        highest_id = potential_bidders[-1]

    # second highest bid is present
    if len(potential_bidders) > 1:
        second_id = potential_bidders[-2]

    # nobody else is bidding
    else:
        second_id = highest_id

    # make changes to the record
    players[highest_id][2] -= players[second_id][0] / 1000
    players[highest_id][4] += 1
    players[highest_id][5] += site[1]
    
    if players[:,2].sum() < 0:
        players[:,5] = players[:,5] / players[:,4]
        break

df = pd.DataFrame(players)
df.columns = ['max_bid', 'start_budget' , 'remain_budget', 'target_fill', 'impressions', 'quality']
df['eCPM'] = df.start_budget / df.impressions * 1000
df
