import numpy as np

# NETWORK
# we want to define our layers. 
#   input - health, weapon str, weapon last hit, num cards left, can avoid, 4 card values, 4 card types (13 input nodes)
#   middle layers - not sure yet, but we can just throw out some random stuff to try it
#   output - should we avoid, then 4 card selection nodes which we pick based on strength (5 output nodes)
# We then simply interpert the output network as follows:
#   if the AI has a high avoidance activation, we avoid the room
#   otherwise, list the nodes based on their activation strength, and then pick the nodes, strongets to weakest,
#       until we get 3 nodes. The AI is going to ineract with those nodes, in that order.

# our first layer is just the base inputs, so we don't need to do any math on that (it's just a col vector)
# for subsequent layers, we want to apply a set of weights and biasies to that initial layer 
#   z = wA + b, where 
#       z is the output of the first layer, 
#       w is the weights of the first layer, 
#       A is the activation values of the zeroth layer, 
#       and b is the biasies of the first layer
#   to get our activation value from z, we need to apply an activation function (like ReLU)
#   A = ReLU(Z)
#       btw. ReLU stands for Rectified Linear Unit. it's simply max(0, z[i])
#   for our output layer, we want to have our activation be tied to value between 0 and 1 as probabilities.
#       to do this, we can use the softmax activation function.
#       (e^zi)/(SUM from j=1 to K(e^zj)), where
#           e^zi represents an individual node from the output layer, 
#           K is the number of nodes in the output layer, 
#           and (SUM from j=1 to K(e^zj)) is simply the total value of all output layer nodes's activation values

class Network:
    def __init__(self, layer_sizes):
        self.weight_layers = []
        self.bias_layers = []
        for i in range(len(layer_sizes)-1):
            input_layer_size = layer_sizes[i]
            output_layer_size = layer_sizes[i+1]
            self.weight_layers.append(np.random.randn(output_layer_size, input_layer_size))
            self.bias_layers.append(np.random.randn(output_layer_size, 1))

    def ReLU(self, Z):
        return np.maximum(0, Z)

    def forward(self, X):
        A = X # our initial layer A0 is the same as the input layer X
        for i in range(len(self.weight_layers)):
            Z = self.weight_layers[i].dot(A) + self.bias_layers[i]
            A = self.ReLU(Z)
        # we don't want the output to go through the ReLU, so we can just leave it be.
        return Z
    
    def write_to_file(self, file_name="./network.txt"):
        file_text = ""
        for i in range(len(self.weight_layers)):
            layer_number = i+1
            weight_layer = self.weight_layers[i].flatten().tolist()
            bias_layer = self.bias_layers[i].flatten().tolist()
            file_text = file_text + f"W{str(layer_number)}[{len(weight_layer)}]: {str(weight_layer)}\n"
            file_text = file_text + f"b{str(layer_number)}[{len(bias_layer)}]: {str(bias_layer)}\n"
        with open(file_name, "w") as file:
            file.write(file_text)