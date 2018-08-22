"""Nonlinear activation functions."""

from abc import ABC, abstractmethod

import numpy as np

from nn.weights import initialise_weights


class Activation(ABC):

    @property
    @abstractmethod
    def trainable(self) -> bool:
        pass

    @abstractmethod
    def forward(self, x: np.ndarray) -> np.ndarray:
        pass

    @abstractmethod
    def backward(self, x: np.ndarray) -> np.ndarray:
        pass


class Linear(Activation):
    """Linear layer"""

    def __init__(self, in_size: int, out_size: int, initialisation_method: str='xavier-average'):
        self.weights = initialise_weights((in_size, out_size), method=initialisation_method)
        self.biases = np.zeros((1, out_size))

        self._cached_activations = None
        self._weight_gradients = np.zeros(self.weights.shape)
        self._bias_gradients = np.zeros(self.biases.shape)

    @property
    def trainable(self) -> bool:
        return True

    def forward(self, x: np.ndarray) -> np.ndarray:
        activations = np.dot(x, self.weights) + self.biases
        self._cached_activations = activations
        return activations

    def backward(self, error: np.ndarray) -> np.ndarray:
        # Update the gradients
        self._bias_gradients = np.sum(error, 0)
        self._weight_gradients = np.dot(self._cached_activations.T, error)
        return np.dot(error, self.weights.T)


class Sigmoid(Activation):
    """Logistic sigmoid activation"""

    def __init__(self):
        self.cached_input = None

    @staticmethod
    def _sigmoid(x: np.ndarray) -> np.ndarray:
        return 1 / (1 + np.exp(-x))

    @property
    def trainable(self) -> bool:
        return False

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Compute the logistic function for a given input x.

        Parameters
        ----------
        x : ndarray of float

        Returns
        -------
        activation : ndarray
           the sigmoid of x

        """
        self.cached_input = x
        return self._sigmoid(x)

    def backward(self, error: np.ndarray) -> np.ndarray:
        """Compute the derivative of the sigmoid function for the given input x.

        Parameters
        ----------
        error : ndarray of float
            Where the derivative will be evaluated

        Returns
        -------
        derivative : ndarray of float
            The derivative of the sigmoid function at x

        """
        derivative = self._sigmoid(self.cached_input) * (1 - self._sigmoid(self.cached_input))
        return error * derivative


class Tanh(Activation):
    """Tanh activation"""

    def __init__(self):
        self._cached_input = None

    @property
    def trainable(self) -> bool:
        return False

    @staticmethod
    def _tanh(x: np.ndarray) -> np.ndarray:
        return -1 + 2 / (1 + np.exp(-2 * x))

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Compute the nonlinear tanh function for the input x.

        Parameters
        ----------
        x : ndarray of float

        Returns
        -------
        activation : ndarray of float

        """
        self._cached_input = x
        return self._tanh(x)

    def backward(self, error: np.ndarray) -> np.ndarray:
        """Compute the derivative of the tanh function at x.

        Parameters
        ----------
        error : ndarray of float

        Returns
        -------
        derivative : ndarray of float

        """
        return error * (1 - self._tanh(self._cached_input) ** 2)


class ReLU(Activation):
    """Rectified Linear Unit activation"""

    def __init__(self):
        self.cached_input = None

    @property
    def trainable(self) -> bool:
        return False

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Rectified Linear Unit.
        Computes max(0, x) i.e. negative values of x are set to zero.

        Parameters
        ----------
        x : ndarray of float

        Returns
        -------
        out : ndarray of float

        """
        self.cached_input = x
        return np.maximum(0, x)

    def backward(self, error: np.ndarray) -> np.ndarray:
        """Compute the derivative of the ReLU function with respect to it's input at x.

        Parameters
        ----------
        error : ndarray of float

        Returns
        -------
        derivative : ndarray of float

        """
        return error * np.asarray(self.cached_input >= 0, np.float)
