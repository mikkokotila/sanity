from ipywidgets import interact, widgets, fixed

@interact(budget=widgets.IntSlider(min=1000, max=1000000, step=1000, value=10000),
          true_cpm=widgets.FloatSlider(min=0.01, max=20, step=0.01, value=6),
          commissions=widgets.FloatSlider(min=0.1, max=0.9, step=0.01, value=0.55),
          fraud=widgets.FloatSlider(min=0.02, max=1, step=0.01, value=0.25),
          inview=widgets.FloatSlider(min=0.01, max=1, step=0.01, value=0.75),
          ctr=widgets.FloatSlider(min=0.0005, max=0.01, step=0.0001, value=0.001, readout_format='.3f'),
          action=widgets.FloatSlider(min=0.01, max=0.5, step=0.01, value=0.05),
          goal=widgets.FloatSlider(min=0.01, max=1, step=0.01, value=0.2),
          revenue=widgets.FloatSlider(min=1, max=1000, step=1, value=10))

def test(budget, true_cpm, commissions, fraud, inview, ctr, action, goal, revenue):
    
    
    revenue = int(budget / true_cpm * 1000 * (1 - commissions) * (1 - fraud) * (inview) * ctr * action * goal * revenue)
    
    # results preparation
    
    profit = round(revenue - budget)
    roi = round(revenue / budget, 4) - 1
    
    to_commissions = budget * commissions
    to_fraud = budget * (1 - commissions) * fraud 
    to_viewability = (budget - to_commissions - to_fraud) * (1 - inview)
    to_working = budget - to_commissions - to_fraud - to_viewability
    
    impressions = budget / (true_cpm / commissions) * 1000
    clicked = impressions * ctr
    acted = clicked * action
    spent = acted * goal

    
    # results output
    print("RESULTS \n-------")
    print("Net Revenue: $%d" % profit)
    print("ROI: %f" % roi)
    
    print("\nBREAKDOWN \n-----")
    print("Commissions : $%d" % to_commissions)
    print("Fraud: $%d" % to_fraud)
    print("Out of View: $%d" % to_viewability)
    print("Working Media: $%d" % to_working)
    
    print("\nFUNNEL \n-----")
    print("Impressions: %d" % impressions)
    print("Clicked: %d" % clicked)
    print("Acted: %d" % acted)
    print("Bought: %d" % spent)
