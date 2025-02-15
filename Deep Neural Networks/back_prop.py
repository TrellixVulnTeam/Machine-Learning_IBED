import numpy as np

# define the number of iterations.
num_itr = 6000

# define batch size.
batchSize = 3.

# define the input data dimension.
inputSize = 2

# define the output dimension.
outputSize = 1

# define the dimension of the hidden layer.
hiddenSize = 3


class Neural_Network():
    def __init__(self):
        # weights
        self.U = np.random.randn(inputSize, hiddenSize)
        self.W = np.random.randn(hiddenSize, outputSize)
        self.e = np.random.randn(hiddenSize)
        self.f = np.random.randn(outputSize)

    def fully_connected(self, X, U, e):
        '''
        fully connected layer.
        inputs:
            U: weight 
            e: bias
        outputs:
            X * U + e
        '''

        return np.dot(X, U) + e

    def sigmoid(self, s):
        '''
        sigmoid activation function. 
        inputs: s
        outputs: sigmoid(s)  
        '''
        return 1 / (1 + np.exp(-s))

    def sigmoidPrime(self, s):
        '''
        derivative of sigmoid (Written section, Part a).
        inputs: 
            s = sigmoid(x)
        outputs: 
            derivative sigmoid(x) as a function of s 
        '''
        d_sigmoid = s * (1 - s)
        return d_sigmoid

    def forward(self, X):
        '''
        forward propagation through the network.
        inputs:
            X: input data (batchSize, inputSize) 
        outputs:
            c: output (batchSize, outputSize)
        '''
        Z = self.fully_connected(X, self.U, self.e)
        B = self.sigmoid(Z)
        H = self.fully_connected(B, self.W, self.f)
        c = self.sigmoid(H)

        return c

    def d_loss_o(self, gt, o):
        '''
        computes the derivative of the L2 loss with respect to 
        the network's output.
        inputs:
            gt: ground-truth (batchSize, outputSize)
            o: network output (batchSize, outputSize)
        outputs:
            d_o: derivative of the L2 loss with respect to the network's 
            output o. (batchSize, outputSize)
        '''

        return (o - gt)/o.shape[0]

    def error_at_layer2(self, d_o, o):
        '''
        computes the derivative of the loss with respect to layer2's output
        (Written section, Part b).
        inputs:
            d_o: derivative of the loss with respect to the network output (batchSize, outputSize)
            o: the network output (batchSize, outputSize)
        returns 
            delta_k: the derivative of the loss with respect to the output of the second
            fully connected layer (batchSize, outputSize).
        '''
        h = o * (1 - o)

        delta_k = d_o * self.sigmoidPrime(h)
        return delta_k

    def error_at_layer1(self, delta_k, W, b):
        '''
        computes the derivative of the loss with respect to layer1's output (Written section, Part e).
        inputs:
            delta_k: derivative of the loss with respect to the output of the second
            fully connected layer (batchSize, outputSize). 
            W: the weights of the second fully connected layer (hiddenSize, outputSize).
            b: the input to the second fully connected layer (batchSize, hiddenSize).
        returns:
            delta_j: the derivative of the loss with respect to the output of the second
            fully connected layer (batchSize, hiddenSize).
        '''
        z = b * (1 - b)

        temp = np.dot(delta_k, np.transpose(W))
        q=temp
        '''q = sum(temp)

        q = q * np.ones([temp.shape[0], temp.shape[1]])'''

        delta_j = q * self.sigmoidPrime(z)

        return delta_j

    def derivative_of_w(self, b, delta_k):
        '''
        computes the derivative of the loss with respect to W (Written section, Part c).
        inputs:
            b: the input to the second fully connected layer (batchSize, hiddenSize).
            delta_k: the derivative of the loss with respect to the output of the second
            fully connected layer's output (batchSize, outputSize).
        returns:
            d_w: the derivative of loss with respect to W  (hiddenSize ,outputSize).
        '''
        d_w = np.transpose(sum(delta_k * b)[np.newaxis, :])

        return d_w

    def derivative_of_u(self, X, delta_j):
        '''
        computes the derivative of the loss with respect to U (Written section, Part f).
        inputs:
            X: the input to the network (batchSize, inputSize).
            delta_j: the derivative of the loss with respect to the output of the first
            fully connected layer's output (batchSize, hiddenSize).
        returns:
            d_u: the derivative of loss with respect to U (inputSize, hiddenSize).
        '''
        d_u = np.dot(np.transpose(X), delta_j)

        return d_u

    def derivative_of_e(self, delta_j):
        '''
        computes the derivative of the loss with respect to e (Written section, Part g).
        inputs:
            delta_j: the derivative of the loss with respect to the output of the first
            fully connected layer's output (batchSize, hiddenSize).
        returns:
            d_e: the derivative of loss with respect to e (hiddenSize).
        '''
        d_e = sum(delta_j)

        return d_e

    def derivative_of_f(self, delta_k):
        '''
        computes the derivative of the loss with respect to f (Written section, Part d).
        inputs:
            delta_k: the derivative of the loss with respect to the output of the second
            fully connected layer's output (batchSize, outputSize).
        returns:
            d_f: the derivative of loss with respect to f (outputSize).
        '''
        d_f = sum(delta_k)

        return d_f

    def backward(self, X, gt, o):
        '''
        backpropagation through the network.
        Task: perform the 8 steps required below.
        inputs: 
            X: input data (batchSize, inputSize)
            y: ground truth (batchSize, outputSize)
            o: network output (batchSize, outputSize)        
        '''

        # 1. Compute the derivative of the loss with respect to c.
        # Call: d_loss_o

        # 2. Compute the error at the second layer (Written section, Part b).
        # Call: error_at_layer2

        # 3. Compute the derivative of W (Written section, Part c).
        # Call: derivative_of_w

        # 4. Compute the derivative of f (Written section, Part d).
        # Call: derivative_of_f

        # 5. Compute the error at the first layer (Written section, Part e).
        # Call: error_at_layer1 

        # 6. Compute the derivative of U (Written section, Part f).
        # Call: derivative_of_u

        # 7. Compute the derivative of e (Written section, Part g).
        # Call: derivative_of_e

        # 8. Update the parameters
        d_o = self.d_loss_o(gt, o)
        delta_k = self.error_at_layer2(d_o, o)
        Z = self.fully_connected(X, self.U, self.e)
        b = self.sigmoid(Z)
        d_w = self.derivative_of_w(b, delta_k)
        d_f = self.derivative_of_f(delta_k)

        delta_j = self.error_at_layer1(delta_k, self.W, b)
        d_u = self.derivative_of_u(X, delta_j)
        d_e = self.derivative_of_e(delta_j)

        alpha = X.shape[0]
        self.U -= d_u * alpha
        self.W -= d_w * alpha
        self.e -= d_e * alpha
        self.f -= d_f * alpha

        ''' Z = self.fully_connected(X, self.U, self.e)
        B = self.sigmoid(Z)
        H = self.fully_connected(B, self.W, self.f)
        c = self.sigmoid(H)
        print(o)'''

    def train(self, X, y):
        o = self.forward(X)
        self.backward(X, y, o)


def main():
    """ Main function """
    # generate random input data of dimension (batchSize, inputSize).
    a = np.random.randint(0, high=10, size=[3, 2], dtype='l')
    '''a = np.array([[1, 1], [5, 3], [3, 8]])'''
    # generate random ground truth.
    t = np.random.randint(0, high=100, size=[3, 1], dtype='l')
    '''t = np.array([[1], [2], [3]])'''
    # scale the input and output data.
    a = a / np.amax(a, axis=0)
    t = t / 100

    # create an instance of Neural_Network.
    NN = Neural_Network()
    for i in range(num_itr):
        print("Input: \n" + str(a))
        print("Actual Output: \n" + str(t))
        print("Predicted Output: \n" + str(NN.forward(a)))
        print("Loss: \n" + str(np.mean(np.square(t - NN.forward(a)))))
        print("\n")
        NN.train(a, t)


if __name__ == "__main__":
    main()
