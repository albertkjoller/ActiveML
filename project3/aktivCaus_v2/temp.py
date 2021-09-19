


# plotting
flatten = lambda t: [item for sublist in t for item in sublist]
def plot(data, labels, ylabel=True):
    vars, rowlabels = labels
    data = data.transpose().to_numpy()
    nvars


    dd = [d[vars].transpose().to_numpy() for d in ddata]  # transform to work properly
    data = ddata.transpose().to_numpy()
    _shape = (len(dd), len(dd[-1])) # number of diff. dataframes \ number of variables.
    lims = [[min(lst + [-2]), max(lst + [2])] for lst in dd[-1]] # read columns of every variable and determine min and max

    f, a = plt.subplots(*_shape, figsize=(15,12))
    fs = 30 # font size

    if ylabel:
        f.suptitle('Interventions', fontsize=fs)
        for ax, col in zip(a[0], vars):
            ax.set_title(col)
        for ax, row in zip(a[:, 0], rowlabels):
            ax.set_ylabel(row, rotation=0, size='large', labelpad=30)

        a = a.ravel()
        for idx, ax in enumerate(a):
            ax.hist(flatten(dd)[idx], bins=12)  # flatten so every index are the samples for a variable.
            ax.set_xlim(lims[idx % 6])

    else:
        f.suptitle('Conditionings', fontsize=fs)
        for ax, col in zip(a[0], vars):
            ax.set_title(col)
        axx = a[-1, 0]
        axx.set_ylabel('Base Case', rotation=0, size='large', labelpad=40)

        a = a.ravel()
        for idx, ax in enumerate(a):
            ax.hist(flatten(dd)[idx], bins=12)# flatten so every index are the samples for a variable.
        ax.set_xlim(lims[idx % 6])

    plt.show()


# conditioning
def condition(cond, base):
    x = []
    for letter, direction, value in cond:
        if str(direction) == '>':
            x.append(base[base[letter] >= value])
        else:
            x.append(base[base[letter] < value])
    return x # the conditioned arrays.




