from ex_1_4_switch import sample_switch
import numpy as np


def calculateProbs(samples, intervene_blue=False, intervene_purple=False):
    mat = np.empty((3,4))

    blue = samples[:, 0]
    purple = samples[:, 1]

    # Marginal probs
    Pb = sum(blue) / n
    P_notb = 1 - Pb

    Pp = sum(purple) / n
    P_notp = 1 - Pp

    mat[0,:] = [Pb, P_notb, Pp, P_notp]



    # Conditional probs
    blue_pos = np.where(blue == 1)[0]
    Pp_given_b = sum(purple[blue_pos]) / len(blue_pos)
    Pnotp_given_b = 1 - Pp_given_b

    if intervene_blue:
        Pp_given_notb = float('nan')
        Pnotp_given_notb = float('nan')
    else:
        not_blue_pos = np.where(blue == 0)[0]
        Pp_given_notb = sum(purple[not_blue_pos]) / len(not_blue_pos)
        Pnotp_given_notb = 1 - Pp_given_notb

    mat[1,:] = [Pp_given_b, Pnotp_given_b, Pp_given_notb, Pnotp_given_notb]


    purple_pos = np.where(purple == 1)[0]
    Pb_given_p = sum(blue[purple_pos]) / len(purple_pos)
    Pnotb_given_p = 1 - Pb_given_p

    if intervene_purple:
        Pb_given_notp = float('nan')
        Pnotb_given_notp = float('nan')
    else:
        not_purple_pos = np.where(purple == 0)[0]
        Pb_given_notp = sum(blue[not_purple_pos]) / len(not_purple_pos)
        Pnotb_given_notp = 1 - Pb_given_notp

    mat[2,:] = [Pb_given_p, Pnotb_given_p, Pb_given_notp, Pnotb_given_notp]

    print(mat)
    print("")


if __name__ == '__main__':
    # Get some samples
    np.random.seed(0)
    n = 10000
    print("\nResults from initial experiment:")
    samples = sample_switch(n_samples=n)
    calculateProbs(samples)

    print("Results from intervening blue:")
    np.random.seed(0)
    samples = sample_switch(n_samples=n, intervene_blue=True)
    calculateProbs(samples, intervene_blue=True)

    print("Results from intervening purple:")
    np.random.seed(0)
    samples = sample_switch(n_samples=n, intervene_purple=True)
    calculateProbs(samples, intervene_purple=True)