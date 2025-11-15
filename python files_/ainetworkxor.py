import numpy as np

# Define neural network structure
input_size = 2
hidden_size = 3
output_size = 1
learning_rate = 0.01

# Initialize weights and biases
np.random.seed(42)
W1 = np.random.randn(input_size, hidden_size)
b1 = np.zeros((1, hidden_size))
W2 = np.random.randn(hidden_size, output_size)
b2 = np.zeros((1, output_size))

# Sigmoid activation function and its derivative
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

# Forward propagation
def forward_propagation(X):
    z1 = np.dot(X, W1) + b1
    a1 = sigmoid(z1)
    z2 = np.dot(a1, W2) + b2
    a2 = sigmoid(z2)
    return z1, a1, z2, a2

# Backward propagation
def backward_propagation(X, y, z1, a1, z2, a2):
    global W1, b1, W2, b2
    error_output = y - a2
    delta_output = error_output * sigmoid_derivative(a2)
    error_hidden = delta_output.dot(W2.T)
    delta_hidden = error_hidden * sigmoid_derivative(a1)
    W2 += a1.T.dot(delta_output) * learning_rate
    b2 += np.sum(delta_output, axis=0, keepdims=True) * learning_rate
    W1 += X.T.dot(delta_hidden) * learning_rate
    b1 += np.sum(delta_hidden, axis=0, keepdims=True) * learning_rate

# XOR dataset
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [0]])

# Training loop
for epoch in range(10000):
    z1, a1, z2, a2 = forward_propagation(X)
    backward_propagation(X, y, z1, a1, z2, a2)
    if epoch % 1000 == 0:
        loss = np.mean(np.square(y - a2))
        print(f'Epoch {epoch}, Loss: {loss}')

# Test the neural network
z1, a1, z2, a2 = forward_propagation(X)
print('Predicted outputs:')
print(a2)
