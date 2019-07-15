def _will_bid(percent):

    import random

    return random.randrange(100) < percent


def _get_truncated_normal(mean=0, sd=1, low=0, upp=10):

    from scipy.stats import truncnorm

    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)


def _player_specs(n):

    import numpy as np

    players = np.zeros([n, 6])

    # create player max_bids
    values = _get_truncated_normal(10.1, 9.9, 0.2, 20)
    players[:, 0] = values.rvs(n)

    # create player budget columns
    values = _get_truncated_normal(200, 450, 50, 500)

    # starting budget
    players[:, 1] = values.rvs(n)

    # running budget
    players[:, 2] = players[:, 1]

    # fill rate
    values = _get_truncated_normal(50, 80, 10, 90)
    players[:, 3] = values.rvs(n)

    # sort based on max_bid
    players = players[players[:, 0].argsort()]

    return players


def market_simulator(no_of_players=10, to_csv=False):

    '''Simulates a programmatic media trading marketplace. Returns a
    pandas dataframe with the simulation results.

    Example use:

            market_simulator(2)

    no_of_players : int
        The number of market participants in the simulation. Note that
        100 participants will take roughly one hour on a standard
        laptop because of the high number of bid events involved.
    to_csv : False or string
        If set to string, then the results will be exported to a file
        of that name on the local drive.
    '''

    import random
    import dedomena

    import numpy as np
    import pandas as pd

    # create the player specs
    players = _player_specs(no_of_players)

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
        potential_bidders = np.where(players[:, 0] >= ask)[0]

        # will they bid
        for bidder in potential_bidders:

            # enough budget is left
            if players[bidder][2] < impression_cost:
                potential_bidders = potential_bidders[potential_bidders != bidder]

            # is currently active
            if _will_bid(players[bidder][3]) is False:
                potential_bidders = potential_bidders[potential_bidders != bidder]

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

        if players[:, 2].sum() < 0:
            players[:, 5] = players[:, 5] / players[:, 4]
            break

    df = pd.DataFrame(players)
    df.columns = ['max_bid', 'start_budget',
                  'remain_budget', 'target_fill',
                  'impressions', 'quality']
    df['eCPM'] = df.start_budget / df.impressions * 1000

    if to_csv is not False:
        df.to_csv(to_csv, index=False)

    return df
