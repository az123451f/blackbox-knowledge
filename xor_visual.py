import numpy as np
import matplotlib.pyplot as plt

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def dsigmoid(x):
    s = sigmoid(x)
    return s * (1 - s)

def train_xor(epochs=5000, lr=0.1):
    # XOR dataset
    X = np.array([[0,0],[0,1],[1,0],[1,1]], dtype=float)
    y = np.array([[0],[1],[1],[0]], dtype=float)

    # Weights
    np.random.seed(42)
    W1 = np.random.randn(2, 4) * 0.5
    b1 = np.zeros((1, 4))
    W2 = np.random.randn(4, 1) * 0.5
    b2 = np.zeros((1, 1))

    losses = []

    for epoch in range(epochs):
        # Forward
        z1 = X @ W1 + b1
        a1 = sigmoid(z1)
        z2 = a1 @ W2 + b2
        y_hat = sigmoid(z2)

        # Loss (MSE)
        loss = np.mean((y_hat - y) ** 2)
        losses.append(loss)

        # Backward
        dloss = 2 * (y_hat - y) / y.shape[0]
        dz2 = dloss * dsigmoid(z2)
        dW2 = a1.T @ dz2
        db2 = np.sum(dz2, axis=0, keepdims=True)

        da1 = dz2 @ W2.T
        dz1 = da1 * dsigmoid(z1)
        dW1 = X.T @ dz1
        db1 = np.sum(dz1, axis=0, keepdims=True)

        # Update
        W1 -= lr * dW1
        b1 -= lr * db1
        W2 -= lr * dW2
        b2 -= lr * db2

        if epoch % 1000 == 0:
            print(f"Epoch {epoch}, Loss: {loss:.6f}")

    print("Expected outputs:\n", y)
    print("Predicted outputs:\n", np.round(y_hat, 3))

    # Visualize loss curve
    plt.figure(figsize=(7,4))
    plt.plot(losses, color='purple')
    plt.title("XOR training loss")
    plt.xlabel("Epoch")
    plt.ylabel("MSE loss")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    train_xor(epochs=8000, lr=0.1)
