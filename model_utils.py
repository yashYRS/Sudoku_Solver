import numpy as np
from tqdm import tqdm
from pathlib import Path

import torch
import torch.nn
from torchvision import datasets, transforms

test_transforms = transforms.Compose([transforms.Resize((28, 28)),
                                      transforms.ToTensor()])


class LogisticRegression(torch.nn.Module):
    def __init__(self, inputSize=28, numClasses=10, channels=1):
        super(LogisticRegression, self).__init__()
        self.linear = torch.nn.Sequential(
              torch.nn.Linear(inputSize*inputSize*channels, numClasses)
        )

    def forward(self, x):
        outputs = self.linear(x)
        return outputs


def getNumCorrect(correct, outputs, labels):
    # For computing Accuracy
    _, predicted = torch.max(outputs.data, 1)
    labelsTemp = labels.to("cpu")
    predicted = predicted.to("cpu")
    return correct + (predicted == labelsTemp).sum().item()


def get_dataset(batchsize=64):
    # Function to import datasets to be used for training
    norm_params = ((0.5,), (0.5,))
    train_transform = transforms.Compose([
                            transforms.ToTensor(),
                            transforms.Normalize(*norm_params)
                        ])
    try:
        trainset = datasets.MNIST(root='data', train=True,
                                  transform=train_transform, download=False)
    except Exception as e:
        trainset = datasets.MNIST(root='data', train=True,
                                  transform=train_transform, download=True)

    torch.backends.cudnn.deterministic = True
    torch.manual_seed(1)
    torch.cuda.manual_seed(1)
    np.random.seed(1)

    trainloader = torch.utils.data.DataLoader(
                            trainset, batch_size=batchsize, shuffle=True)
    return trainloader


def load_model(model_path):
    # Get the device on which model is to be trained
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    if Path(model_path).exists():
        model = LogisticRegression()
        model.load_state_dict(torch.load(model_path))
        model.to(device)
    else:
        print("MODEL NOT FOUND, TRAINING FROM SCRATCH")
        model = train_model(model_path)
    # Convert model to evaluation mode, and then return
    model.eval()
    return model


def predict_image(model, image, thresh=3):
    image_tensor = test_transforms(image)
    image_tensor = torch.flatten(image_tensor)
    # print(model(image_tensor).detach().numpy())
    output_arr = model(image_tensor).detach().numpy()
    if max(output_arr) > thresh:
        print(max(output_arr), np.argmax(output_arr))
        return np.argmax(output_arr)
    return 0


def train_model(model_path, epochs=100, lr=0.001, decay=1e-5):

    # Get important parameters for the MNIST dataset
    train_loader = get_dataset()
    # Get loss function
    lossfn = torch.nn.CrossEntropyLoss()
    # Get the device on which model is to be trained
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    # Create the Model
    model = LogisticRegression()
    model.to(device)
    model.train()
    # Get optimizer
    optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=decay)

    for epoch in tqdm(range(int(epochs))):
        correct, total, epoch_loss = 0, 0, 0.0

        # Training Epoch
        for data in train_loader:
            images, labels = data[0].to(device), data[1].to(device)
            images = images.reshape((images.shape[0], -1))
            optimizer.zero_grad()
            outputs = model(images)

            # Compute Loss
            loss = lossfn(outputs, labels)
            loss.backward()
            epoch_loss += loss.item()

            # Optimizer Step and scheduler step
            optimizer.step()

            # For computing Accuracy ; batch size added at each step
            total += labels.size(0)
            correct = getNumCorrect(correct, outputs, labels)

        train_accuracy = 100*correct/total
        print("Epoch", epoch, "Loss", epoch_loss, "Accuracy", train_accuracy)

    torch.save(model.state_dict(), model_path)
    return model
