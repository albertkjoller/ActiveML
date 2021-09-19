import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np


def dataload(dir):
    # Write directory of csv files - that's it!
    # Make sure there are equal amounts of samples in each
    ddata = []
    for file in os.listdir(dir):
        if file == '.DS_Store':
            pass
        else:
            ddata.append(pd.read_csv(dir + '/' + file).iloc[:, 1:])

    rowlabels = []
    for file in os.listdir(dir):
        if file == '.DS_Store':
            pass
        else:
            rowlabels.append(file.replace('.csv', ''))

    #ddata = [pd.read_csv(dir+'/'+file).iloc[:,1:] for file in os.listdir(dir)][1:]
    #rowlabels = [file.replace('.csv', '') for file in os.listdir(dir)][1:]
    vars = [f'{col}' for col in ddata[0].columns]

    return ddata, vars, rowlabels


# plotting
flatten = lambda t: [item for sublist in t for item in sublist]

def plotting(data, labels, only_base, compare):
    vars, name = labels
    #data = data.transpose().to_numpy()
    figure, axes = plt.subplots(nrows=1, ncols=len(vars))

    coloring = ['#1f77b4', '#ff7f0e']

    if compare:
        for idx, var in enumerate(vars):
            for i in range(2):
                if i == 0:
                    Base = data[i][var].to_numpy().transpose()
                    axes[idx].hist(Base, color = coloring[i], alpha = 0.5, label="Base")
                    axes[idx].set_xlim(np.min(Base)-2,np.max(Base)+2)
                    axes[idx].set_title(var)
                if i == 1: # invervened
                    Intervened = data[i][var].to_numpy().transpose()
                    axes[idx].hist(Intervened, color = coloring[i], alpha = 0.5, label='Invervened')
        figure.suptitle(name)
        plt.subplots_adjust(wspace = 0.4)
        plt.legend(frameon=False, loc='lower center', bbox_to_anchor=(-2.8,-0.16), ncol=2)
        plt.show()

    else:
        if only_base:
            coloring = coloring[0]
        else: # invervened
            coloring = coloring[1]

        for idx, var in enumerate(vars):
            var_data = data[var].to_numpy().transpose()
            axes[idx].hist(var_data, color = coloring, alpha = 0.7)
            axes[idx].set_xlim(np.min(var_data)-1,np.max(var_data)+1)
            axes[idx].set_title(var)

        figure.suptitle(name)
        plt.subplots_adjust(wspace = 0.7)
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

def condition_plotting(data, labels, only_base, compare):
    vars, name = labels
    #data = data.transpose().to_numpy()
    figure, axes = plt.subplots(nrows=1, ncols=len(vars))

    coloring = ['#1f77b4', '#ff7f0e']

    if compare:
        for idx, var in enumerate(vars):
            for i in range(2):
                if i == 0:
                    Base = data[i][var].to_numpy().transpose()
                    axes[idx].hist(Base, color = coloring[i], alpha = 0.5, label='Intervention')
                    axes[idx].set_xlim(np.min(Base)-2,np.max(Base)+2)
                    axes[idx].set_title(var)
                if i == 1: # invervened
                    Intervened = data[i][var].to_numpy().transpose()
                    axes[idx].hist(Intervened, color = coloring[i], alpha = 0.5, label='Intervention + Conditioning')
        figure.suptitle(name)
        plt.subplots_adjust(wspace = 0.4)
        plt.legend(frameon=False, loc='lower center', bbox_to_anchor=(-2.8,-0.16), ncol=2)
        plt.show()

if __name__ == "__main__":
    # Set directory of interventions
    dir = './interventions'
    base = pd.read_csv('base_data.csv').iloc[:, 1:]
    intdata, vars, names = dataload(dir)

    # the base
    print('\n\n### Base data ###\n')
    print('Descriptive statistics')
    des = base.describe()
    print(des.to_latex())
    print('Correlation')
    df = round(pd.DataFrame(np.corrcoef(np.transpose(base)), columns=vars, index=vars),3)
    print(df.to_latex())
    plotting(base, (vars, 'Base data'), only_base = True, compare = False)

    for idx, name in enumerate(names):
        name = name.replace("_", ": ")
        print('\n\n### ' + name + '###\n')
        data = intdata[idx]
        print('Descriptive statistics')
        des = data.describe()
        print(des.to_latex()) # LaTeX: .to_latex()
        print('Correlation')
        df = pd.DataFrame(np.corrcoef(np.transpose(data)), columns=vars, index=vars)
        print(df.to_latex()) # LaTeX: .to_latex()
        print('Plot printed..')
        data2 = [base, data]
        plotting(data2, (vars, name), only_base = False, compare = True)


        stop = 0


    ######## her stoppede jeg at kode, mvh aron #######


    # Conditioning - a base file on which conditions will be applied

    # Conditioning A intervening B.

    for intervened, conditioned in [0, 'I'], [3, 'B']:
        condA_B = condition([(conditioned, '>', intdata[intervened][conditioned].mean())], intdata[intervened])[0]
        condData = [intdata[intervened], condA_B]
        if intervened == 0:
            name = 'Intervention: B=2, Conditioning: I>mean(I)'
        else:
            name = 'Intervention: I=-2, Conditioning: B>mean(B)'
        condition_plotting(condData, (vars, name), only_base=False, compare=True)

        print(f'Descriptive statistics of intervention')
        des = intdata[intervened].describe()
        print(des.to_latex()) # LaTeX: .to_latex()

        print(f'Descriptive statistics of intervention + conditioning')
        des = condA_B.describe()
        print(des.to_latex()) # LaTeX: .to_latex()

        print('Correlation of intervention')
        df = pd.DataFrame(np.corrcoef(np.transpose(intdata[intervened])), columns=vars, index=vars)
        print(df.to_latex()) # LaTeX: .to_latex()

        print('Correlation of intervention + conditioning')
        df = pd.DataFrame(np.corrcoef(np.transpose(condA_B)), columns=vars, index=vars)
        print(df.to_latex()) # LaTeX: .to_latex()

    stop = 0

    # Change the values, direction (< or >) and letters for different conditions.

    # Conditioning on basedata
    #cond_arrays = condition([('P', '>', base_['P'].mean()), ('I', '>', base_['I'].mean()), ('K', '>', base_['K'].mean()), ('A', '>', base_['A'].mean()), ('B', '>', base_['B'].mean()), ('S', '>', base_['S'].mean())], base_)
    # conditioning on intervened data
    #cond_arrays = condition([('B', '>', intdata[0]['B'].mean())], intdata[0])

    # Base case
    print(f'Descriptive statistics for conditionings \n{base_.describe()}')
    [print(arr.describe()) for arr in cond_arrays]
    print('Correlation of base:')
    print(pd.DataFrame(np.corrcoef(np.transpose(base_)), columns=vars, index=vars))
    print('Correlation of conditioning:')
    print(pd.DataFrame(np.corrcoef(np.transpose(cond_arrays[0])), columns=vars, index=vars))
    print('Correlation of intervention: I')
    print(pd.DataFrame(np.corrcoef(np.transpose(intdata[2])), columns=vars, index=vars))
    print('Correlation of intervention: P')
    print(pd.DataFrame(np.corrcoef(np.transpose(intdata[0])), columns=vars, index=vars))

    #print('Correlation of conditioning: I')
    #print(pd.DataFrame(np.corrcoef(np.transpose(cond_arrays[1])), columns=vars, index=vars))

    # Condition plots if basecase:
    conddata = cond_arrays + [base_]
    # Condition plots if intervened data:
    #conddata = cond_arrays + [intdata[0]]
    plot(conddata, (vars, rowlabs), ylabel=False)
    stop = 1