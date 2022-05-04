import numpy as np

inputs = [1, 0.5, 0.7]
weights = [[[0.5, 0, 0.3], [0.4, 0.6, 0.7], [0.2, 0.3, 0.5]],  # first layer
           [[0.6, 0.9, 0.2], [0.3, 0.1, 0.8], [0.5, 0.3, 0.7]]]  # second layer
bias = [[0.2, 0, 0.7],  # bias for first layer
        [0.2, 0.8, 0.7]]  # bias for second layer
expected_outputs = [0.820, 0.884, 0.952]
sum_of_products = 0
new_inputs = []
new_weights = []
all_sigmoids = []
saved_layer_outputs = []  # should be of length 2 in our case
learning_factor = 0.01
temp_weights = []

for t in inputs:
    saved_layer_outputs.append(t)


def activation_func(receive_sum_of_prod):
    func_result = 1 / (1 + np.exp(-receive_sum_of_prod))
    func_result = round(func_result, 5)
    new_inputs.append(func_result)
    saved_layer_outputs.append(func_result)


def build_nn():
    global sum_of_products
    for layer_weights, layer_bias in zip(weights, bias):
        print("inputs", inputs)
        for nodal_weights, nodal_bias in zip(layer_weights, layer_bias):
            for input_data, link_weight in zip(inputs, nodal_weights):
                sum_of_products = sum_of_products + (input_data * link_weight)
            sum_of_products += nodal_bias
            activation_func(sum_of_products)
            sum_of_products = 0
        inputs.clear()
        for i in new_inputs:
            inputs.append(i)
        new_inputs.clear()


def get_sum():
    return 0


def s_for_hidden_layer(output_value, current_layer_weights):

    sum_result = 0
    idx_weights = (len(temp_weights))-1

    for i in all_sigmoids:
        sum_result += (temp_weights[idx_weights]*i)

        idx_weights -= 1

    return round(output_value * (1 - output_value) * sum_result, 5)


def s_for_output_layer(output_value, expected_output_value):

    return round(output_value * (1 - output_value) * (expected_output_value - output_value), 5)


def back_propagate():

    output_layer_check = True
    index = (len(saved_layer_outputs)) - 1  # for our obtained outputs ie:- saved layer outputs
    index2 = (len(expected_outputs)) - 1  # for expected outputs
    index3 = (len(all_sigmoids))-1
    for reversed_layer_weights in reversed(weights):
        idx = weights.index(reversed_layer_weights)

        if reversed_layer_weights == weights[-1]:
            output_layer_check = True
        else:
            output_layer_check = False

        if output_layer_check is False:
            g = len(weights[idx + 1])
            h = len(weights[idx + 1][0])

            for q in range(g):
                for w in range(h):
                    temp_weights.append(weights[idx + 1][w][q])

        offset = 0
        for reversed_nodal_weights in reversed(reversed_layer_weights):

            nodal_output = saved_layer_outputs[index]
            index -= 1

            this_index = saved_layer_outputs.index(nodal_output) + offset

            offset += 1

            if output_layer_check:  # for output layer
                s = s_for_output_layer(nodal_output, expected_outputs[index2])
                index2 -= 1
                all_sigmoids.append(s)
            else:  # for input layer

                s = s_for_hidden_layer(nodal_output, weights[idx+1])
                all_sigmoids.append(s)
            for reversed_link_weight in reversed(reversed_nodal_weights):
                # get previous output of respective weight
                prev_output = saved_layer_outputs[this_index - len(reversed_layer_weights)]
                # print("nodal output ", nodal_output, " w ", reversed_link_weight, " last output ", prev_output)
                new_w = round((reversed_link_weight + learning_factor*(s*prev_output)), 5)
                new_weights.append([reversed_link_weight, new_w])
                this_index -= 1

    for layer_weights in weights:
        for nodal_weights in layer_weights:
            for f in new_weights:
                if nodal_weights.count(f[0]) > 0:
                    nodal_weights[nodal_weights.index(f[0])] = f[1]


for i in range(1000):
    build_nn()
    # print("final outputs", inputs)
    print("saved layer outputs", saved_layer_outputs)
    back_propagate()
    saved_layer_outputs.clear()

# loss()
