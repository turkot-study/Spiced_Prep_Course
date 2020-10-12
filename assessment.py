#!/usr/bin/env python3

import matplotlib.pyplot as plt


def read_data(str_file):
    ''' Read the x/y data from 'str_file' and return:
            - tuple with the data labels
            - data as a list of 2-tuples (x, y) '''
    labels = ()
    x = []
    y = []
    # Index lines:
    i = 0
    with open(str_file) as fobj:
        for line in fobj:
            if i == 0:
                labels = tuple(line.rstrip().split(','))
                i += 1
            else:
                x_val, y_val = map(float, line.rstrip().split(','))
                x.append(x_val)
                y.append(y_val)
    return labels, x, y


def plot_data(x, y, labels, str_file, title="Scatter plot"):
    ''' Plot the x/y data as a scatter plot and 
        save it in 'str_file' '''
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.scatter(x=x, y=y, marker='.', c='b')
    ax.set_title(title)
    ax.set_xlabel('$' + labels[0] + '$')
    ax.set_ylabel('$' + labels[1] + '$')
    fig.savefig(str_file, bbox_inches='tight')
    
    
def line_func(x, a, b):
    ''' Returns a list of 
            y = a*x + b 
        for every value in x '''
    res = []
    for x_val in x:
        res.append( a*x_val + b )
    return res
    
    
def calc_MSE(y, y_true):
    ''' Calculates the MSE as:
        MSE = 1/N sum{ (y - y_true)**2 } '''
    N = len(y_true)
    mse_sum = 0
    for i, y_val in enumerate(y):
        mse_sum += (y_val - y_true[i])**2
    return (1/N)*mse_sum
        

if __name__ == "__main__":
    
# Task 1: Read the x/y data points
    labels, data_x, data_y = read_data("data/datapoints.csv")
    #print(labels)
    #for i, x in enumerate(data_x):
    #    print(x, data_y[i])
    
    
# Task 2: Plot the data
    plot_data(data_x, data_y, labels, "plots/fig_task2.pdf", "Task 2: Input data")
    
    
# Task 3: evaluate y = 10*x + 0
    a = 10
    b = 0
    y = line_func(data_x, a, b)
    #for i, x in enumerate(data_x):
    #    print(x, ',', y[i])
    
    
# Task 4: evaluate the MSE
    cur_mse = calc_MSE(y, data_y)
    print('Task 4: MSE = ' + str(cur_mse))
    
    
# Task 5: optimize parameter 'a'
    tmp_a = a
    for i in range(100):
        tmp_a += 0.1
        y = line_func(data_x, tmp_a, b)
        new_mse = calc_MSE(y, data_y)
        if new_mse < cur_mse:
            a = tmp_a
            cur_mse = new_mse
        #else:
        #    break  # Don't use break to be consistent with 'repeat the procedure 100 times'
    print('Task 5: a = ' + str(a) + '; MSE = ' + str(cur_mse))
    # In this case it would make more sense to decrease 'a', but the task clearly states to 'increase a by 0.1'
    
    
# Task 6: optimize parameter 'b'
    tmp_b = b
    for i in range(100):
        tmp_b += 0.1
        y = line_func(data_x, a, tmp_b)
        new_mse = calc_MSE(y, data_y)
        if new_mse < cur_mse:
            b = tmp_b
            cur_mse = new_mse
        #else:
        #    break  # Don't use break to be consistent with 'repeat the procedure 100 times'
    print('Task 6: b = ' + str(b) + '; MSE = ' + str(cur_mse))
    # It would make more sense to decide whether to increase or decrease 'b' on the first iteration, but the task clearly states to 'increase a by 0.1'


# Task 7: How the algorithm could be improved:
#    7.1: Similar to Task 5 and 6, but define the sign for delta a/b on the first iteration:
    a = 10
    b = 0
    tmp_a = a
    d_a = 0.1
    for i in range(100):
        tmp_a += d_a
        y = line_func(data_x, tmp_a, b)
        new_mse = calc_MSE(y, data_y)
        if i == 0:
            if new_mse > cur_mse:
                d_a = -d_a
                tmp_a = a
        else:
            if new_mse < cur_mse:
                a = tmp_a
                cur_mse = new_mse
            else:
                break
    print('Task 7.1a: a = ' + str(a) + '; MSE = ' + str(cur_mse))
    tmp_b = b
    d_b = 0.1
    for i in range(100):
        tmp_b += d_b
        y = line_func(data_x, a, tmp_b)
        new_mse = calc_MSE(y, data_y)
        if i == 0:
            if new_mse > cur_mse:
                d_b = -d_b
                tmp_b = b
        else:
            if new_mse < cur_mse:
                b = tmp_b
                cur_mse = new_mse
            else:
                break
    print('Task 7.1b: b = ' + str(b) + '; MSE = ' + str(cur_mse))
    
#    7.2: Simultaneously optimize a and b:
    a = 10
    b = 0
    cur_mse = calc_MSE(line_func(data_x, a, b), data_y)
    # Until what improvement to continue optimization
    epsilon = 0.000000000000001
    impr = 0.1
    
    tmp_a = a
    d_a = 0.1
    tmp_b = b
    d_b = 0.1
    i_up = 0
    i = 0
    while impr > epsilon:
        i += 1
        tmp_a += d_a
        mse_a = calc_MSE(line_func(data_x, tmp_a, b), data_y)
        if mse_a > cur_mse:
            d_a = -d_a/2
            tmp_a = a
        tmp_b += d_b
        mse_b = calc_MSE(line_func(data_x, a, tmp_b), data_y)
        if mse_b > cur_mse:
            d_b = -d_b/2
            tmp_b = b
        if mse_a > cur_mse and mse_b > cur_mse:
            if i_up < 1:
                i_up += 1
            else:
                print('Iteration finished after no update twice in a row.')
                break
        else:
            i_up = 0
            if mse_a < mse_b:
                a = tmp_a
                impr = (cur_mse - mse_a) / cur_mse
                cur_mse = mse_a
            else:
                b = tmp_b
                impr = (cur_mse - mse_b) / cur_mse
                cur_mse = mse_b
    print('Task 7.2: a = ' + str(a) + '; b = ' + str(b) + '; MSE = ' + str(cur_mse) + ' in ' + str(i) + ' iterations.')
    
    






