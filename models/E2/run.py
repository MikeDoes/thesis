import torch
import json
import torch.nn.functional as F
from torchvision import datasets
from torchvision import transforms
import matplotlib.pyplot as plt
from torchtext.datasets import LanguageModelingDataset
from torchtext.data import Iterator, Field, BPTTIterator, BucketIterator
from torch.utils.data import DataLoader
import numpy as np

path = '/content/thesis/datasets/simple/simple.txt'
iterator_index = 0

tokenizer = lambda x: x.split(' ')

train_field = Field(tokenize=tokenizer,init_token='<sos>', eos_token='<eos>')

train_dataset = LanguageModelingDataset(path = path, text_field=train_field)
# build vocab, which constructs train_field.vocab

train_field.build_vocab(train_dataset)

# then create an iterator using ‘train_dataset‘
batch_size = 20

iterator = DataLoader(dataset=train_dataset, batch_size=batch_size)
field_chars = len(train_field.vocab.stoi)

with open("/content/thesis/datasets/simple/simple.txt") as f:
  text_examples = f.read().split('\n')
indexed_data = []
for i, example_sentence in enumerate(text_examples):
  indexed_data += [[train_field.vocab.stoi[i] for i in example_sentence.split(" ")]]

def custom_iterator(indexed_data, batch_size):
  global iterator_index
  indexed_data = torch.tensor(indexed_data)
  # randomize the data here
  mini_batch = indexed_data[iterator_index:(iterator_index+batch_size)]
  iterator_index += batch_size
  if(iterator_index >= len(indexed_data)):
    iterator_index = 0
  return mini_batch

custom_iterator(indexed_data, batch_size)

from torch.nn.modules.linear import Linear
# Reducing data matrix size to 28*28 = 784 > 128 > 64 > 36 > 18 > 9 and then reversd into 9 < 18 < 36 < 64 < 128 < 784 = 28*28
# Defining the neural network in pytorch
class AutoEncoderText(torch.nn.Module):
  def __init__(self, input_dim = 22, hidden_size = 64, num_layers = 2, embedding_length = 25):
    super().__init__()

    # Building a linear encoder with Linear layed followed by Relu activation function
    self.encoder = torch.nn.Sequential(
        torch.nn.Embedding(input_dim, embedding_length),
        torch.nn.LSTM(input_size = embedding_length, hidden_size = hidden_size, num_layers = num_layers)
    )

    # INPUT: "Sergei has a son Michael and has a wife called Nina"
    # Bottleneck: List of Triplets
    """
    (Michael, son, Sergei)
    # (Sergei, husband, Nina)
    """
    self.linear1 = torch.nn.Linear(64*6, 3)
    self.linear2 = torch.nn.Linear(3, 64*6)

    # OUTPUT: "Bob has a son Steward and has a wife called Marguerettte
    self.decoder = torch.nn.Sequential(
        torch.nn.LSTM(input_size = hidden_size, hidden_size = hidden_size, num_layers = num_layers)
    )
    self.decoder2 = torch.nn.Sequential(torch.nn.Linear(hidden_size, input_dim))

  def forward(self, x, save_bottleneck = False):
    encoded, (hn, cn) = self.encoder(x)
    encoded = encoded[:, -1, :]
    encoded = encoded.view(-1, 1, 64)
    encoded = encoded.repeat(1, 6, 1)

    # encoded = encoded.view(-1, 64*6)
    # encoded = self.linear1(encoded)
    # bottleneck = encoded.detach()
    # encoded = self.linear2(encoded).view(-1, 6, 64)

    reconstructed, (hn, cn) = self.decoder(encoded)
    reconstructed = self.decoder2(reconstructed)

    if save_bottleneck:
      return reconstructed, bottleneck
    return reconstructed

data = custom_iterator(indexed_data, batch_size)
data = data.cuda()
data.shape

# Model Initialization
model = AutoEncoderText(input_dim=field_chars).cuda()

# Validation using MSE Loss function
loss_fn = torch.nn.CrossEntropyLoss()

# Using an Adam Optimizer with lr = 0.1
optimizer = torch.optim.Adam(model.parameters(), lr = 0.01, weight_decay = 1e-5)


epochs = 70
outputs = []
losses = []

for epoch in range(epochs):
  for i in range(20):
    data = custom_iterator(indexed_data, batch_size)
    data = data.cuda()

    # Output of Autoencoder
    
    ### Output shape is 8, 6, 22
    ### Input shape is 8, 22

    reconstructed = model(data)
    reconstructed=reconstructed.transpose(1,2)

    # Calculating loss
    loss = loss_fn(reconstructed, data)

    # The gradients are set to zero.
    # The gradient is computed and stored
    # .step() performs parameters update

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    # Storing the losses in a list for plotting
    losses.append(loss)
  
  outputs.append((epochs, data, reconstructed))

original = data
reconstruction, bottleneck = model.forward(data, True)
print("Original:", original)
print("Reconstruction:", torch.argmax(reconstruction, dim=2))
print("Bottleneck:", bottleneck)

vis_bottlenecks = []
vis_original = []
original = original.detach()
bottleneck = bottleneck.detach()
for i in range(batch_size):
  unique_words = [original.cpu()[i][0]] + [original.cpu()[i][3]] + [original.cpu()[i][5]]
  sentence_bottleneck = bottleneck.cpu()[i]

  
  vis_original += unique_words
  vis_bottlenecks += sentence_bottleneck

print(len(vis_bottlenecks))
print(len(vis_original))

plt.scatter(vis_bottlenecks, vis_original, alpha = 0.1)
plt.show()

plt.style.use('fivethirtyeight')
plt.xlabel('Iterations')
plt.ylabel('Loss')

losses = [i.detach().cpu() for i in losses]
plt.plot(losses)