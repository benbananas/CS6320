from torch import nn
from torch import optim
import torch


class Model(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.layer_1 = nn.Linear(
            in_features=input_dim, out_features=hidden_dim)
        self.layer_2 = nn.Linear(
            in_features=hidden_dim, out_features=output_dim)
        # self.layer_3 = nn.Linear(
        #     in_features=hidden_dim, out_features=output_dim)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # x = x.view(-1, self.input_dim)
        x = self.layer_1(x)
        x = self.relu(x)
        x = self.layer_2(x)
        # x = self.relu(x)
        # x = self.layer_3(x)
        return self.sigmoid(x)


def train_regression_model(xTr, yTr, model, num_epochs, loss_fn, lr=1e-3, print_freq=100, display_loss=True):
    """Train loop for a neural network model. Please use the Adam optimizer, optim.Adam.

    Input:
        xTr:     n x d matrix of regression input data
        yTr:     n-dimensional vector of regression labels
        model:   nn.Model to be trained
        num_epochs: number of epochs to train the model for
        lr:      learning rate for the optimizer
        print_freq: frequency to display the loss

    Output:
        model:   nn.Module trained model
    """
    model.train()
    optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=1e-3)

    for epoch in range(num_epochs):
        # need to zero the gradients in the optimizer so we don't
        # use the gradients from previous iterations
        optimizer.zero_grad()
        # run the forward pass through the model to compute predictions
        pred = model(xTr)
        loss = loss_fn(pred.squeeze(1), yTr)
        loss.backward()  # compute the gradient wrt loss
        optimizer.step()  # performs a step of gradient descent
        if display_loss and (epoch + 1) % print_freq == 0:
            print('epoch {} loss {}'.format(epoch+1, loss.item()))

    return model  # return trained model
