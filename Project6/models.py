import nn


class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        "*** YOUR CODE HERE ***"
        return nn.DotProduct(x, self.get_weights())

    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        "*** YOUR CODE HERE ***"
        if(nn.as_scalar(self.run(x)) >= 0):
            return 1
        return -1

    def train(self, dataset):
        """
        Train the perceptron until convergence.
        """
        "*** YOUR CODE HERE ***"
        #https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html
        while True:
            i = 0
            for (x, y) in dataset.iterate_once(1):
                if self.get_prediction(x) != nn.as_scalar(y): 
                    nn.Parameter.update(self.w, x,nn.as_scalar(y))
                    i += 1 
            if i == 0:
                break   

class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    Hidden layer size 512
    Batch size 200
    Learning rate 0.05
    One hidden layer (2 linear layers in total)
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.w1 = nn.Parameter(1, 512)
        self.w2 = nn.Parameter(512, 1)
        self.b1 = nn.Parameter(1, 512)
        self.b2 = nn.Parameter(1, 1)

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** YOUR CODE HERE ***"
        """
        f(x) = linear(h2, b2) + b2
        h2 = ReLU(h1 + b1)
        h1 = linear(x, w1)
        """
        h1 = nn.Linear(x, self.w1)
        h2 = nn.ReLU(nn.AddBias(h1, self.b1))
        return nn.AddBias(nn.Linear(h2, self.w2), self.b2)


    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        predicted_y = self.run(x)
        return nn.SquareLoss(predicted_y, y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        while True:
            i = 0 
            for (x, y) in dataset.iterate_once(200):
                loss = (self.get_loss(x, y))
                if nn.as_scalar(loss) > 0.02:
                    i+= 1
                    grad_wrt =  nn.gradients(loss, [self.w1, self.b1, self.w2, self.b2])
                    self.w1.update(grad_wrt[0], -0.05)
                    self.b1.update(grad_wrt[1], -0.05)
                    self.w2.update(grad_wrt[2], -0.05)
                    self.b2.update(grad_wrt[3], -0.05)
                    nn.as_scalar(loss)
            if i == 0: 
                break


class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Initialize your model parameters here
        """
        Hidden layer size 200
        Batch size 100
        Learning rate 0.5
        Two hidden layer (3 linear layers in total)
        """
        "*** YOUR CODE HERE ***"
        #hidden layer weight and bias
        self.w1 = nn.Parameter(784, 200)
        self.w2 = nn.Parameter(200, 200)
        self.b1 = nn.Parameter(1, 200)
        self.b2 = nn.Parameter(1, 200) 

        #output layer weight and bias
        self.w3 = nn.Parameter(200, 10)
        self.b3 = nn.Parameter(1,10)

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        h1 = nn.Linear(x, self.w1)
        h2 = nn.ReLU(nn.AddBias(h1, self.b1))
        h3 = nn.Linear(h2,self.w2)
        h4 = nn.ReLU(nn.AddBias(h3, self.b2))
        return nn.AddBias(nn.Linear(h4,self.w3),self.b3)

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        predicted_y = self.run(x)
        return nn.SquareLoss(predicted_y, y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        while dataset.get_validation_accuracy() < 0.976:
            for (x, y) in dataset.iterate_once(100):
                loss = (self.get_loss(x, y))
                grad_wrt =  nn.gradients(loss, [self.w1, self.b1, self.w2, self.b2, self.w3, self.b3])
                self.w1.update(grad_wrt[0], -0.5)
                self.b1.update(grad_wrt[1], -0.5)
                self.w2.update(grad_wrt[2], -0.5)
                self.b2.update(grad_wrt[3], -0.5)
                self.w3.update(grad_wrt[4], -0.5)
                self.b3.update(grad_wrt[5], -0.5)
            
class LanguageIDModel(object):
    """
    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Our dataset contains words from five different languages, and the
        # combined alphabets of the five languages contain a total of 47 unique
        # characters.
        # You can refer to self.num_chars or len(self.languages) in your code
        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]
        self.num_layer = 2

        # Initialize your model parameters here
        """
        Hidden layer size 400
        Batch size 100
        Learning rate 0.5
        Two hidden layer (3 linear layers in total)
        """
        "*** YOUR CODE HERE ***"
        self.w = nn.Parameter(self.num_chars, 200)

        #hidden layer weight and bias
        self.w1 = nn.Parameter(200, 200)
        self.w2 = nn.Parameter(200, 200)
        self.b1 = nn.Parameter(1, 200)
        self.b2 = nn.Parameter(1, 200)

        #output layer weight and bias
        self.w3 = nn.Parameter(200, 5)
        self.b3 = nn.Parameter(1, 5)

    def hidden_layer(self, x):
        output = x
        output = nn.ReLU(nn.AddBias(nn.Linear(output, self.w1), self.b1))
        output = nn.ReLU(nn.AddBias(nn.Linear(output, self.w2), self.b2))
        return output

    def run(self, xs):
        """
        Runs the model for a batch of examples.

        Although words have different lengths, our data processing guarantees
        that within a single batch, all words will be of the same length (L).

        Here `xs` will be a list of length L. Each element of `xs` will be a
        node with shape (batch_size x self.num_chars), where every row in the
        array is a one-hot vector encoding of a character. For example, if we
        have a batch of 8 three-letter words where the last word is "cat", then
        xs[1] will be a node that contains a 1 at position (7, 0). Here the
        index 7 reflects the fact that "cat" is the last word in the batch, and
        the index 0 reflects the fact that the letter "a" is the inital (0th)
        letter of our combined alphabet for this task.

        Your model should use a Recurrent Neural Network to summarize the list
        `xs` into a single node of shape (batch_size x hidden_size), for your
        choice of hidden_size. It should then calculate a node of shape
        (batch_size x 5) containing scores, where higher scores correspond to
        greater probability of the word originating from a particular language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
        Returns:
            A node with shape (batch_size x 5) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        
        for i in range(len(xs)):
            if i == 0:
                 h_output = nn.Linear(xs[0], self.w)
            else:
                h_output = nn.Add(self.hidden_layer(h_output), nn.Linear(xs[i], self.w))
        return nn.AddBias(nn.Linear(h_output, self.w3), self.b3)

    def get_loss(self, xs, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 5). Each row is a one-hot vector encoding the correct
        language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
            y: a node with shape (batch_size x 5)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        predicted_y = self.run(xs)
        return nn.SquareLoss(predicted_y, y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        while True:
            i = 0 
            for (x, y) in dataset.iterate_once(100):
                loss = (self.get_loss(x, y))
                if dataset.get_validation_accuracy() < 0.87:
                    i+= 1
                    grad_wrt =  nn.gradients(loss,[self.w1, self.b1, self.w2, self.b2, self.w3, self.b3, self.w])
                    self.w1.update(grad_wrt[0], -0.5)
                    self.b1.update(grad_wrt[1], -0.5)
                    self.w2.update(grad_wrt[2], -0.5)
                    self.b2.update(grad_wrt[3], -0.5)
                    self.w3.update(grad_wrt[4], -0.5)
                    self.b3.update(grad_wrt[5], -0.5)
                    self.w.update(grad_wrt[6], -0.5)
            if i == 0: break