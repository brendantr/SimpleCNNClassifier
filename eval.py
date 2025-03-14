############################################
# Nicola Altini (2020)
#
# This is the script which contains the code for evaluating the CNN.
# You have to train your CNN before. See train.py
############################################

import torch # type: ignore
import torchvision # type: ignore

from sklearn.metrics import confusion_matrix, classification_report # type: ignore
from PIL import ImageFile # type: ignore
ImageFile.LOAD_TRUNCATED_IMAGES = True

from config import *
from net import Net
from utils import make_pred_on_dataloader, get_classes, subsample_dataset


#%%  Create Train Dataloaders
print("Creating training   dataset from ", train_folder)

train_dataset = torchvision.datasets.ImageFolder(
        root=train_folder,
        transform=transform_test
    )
train_dataloader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size,
                                               shuffle=False, num_workers=num_workers)

val_dataset = torchvision.datasets.ImageFolder(
    root=val_folder,
    transform=transform_test
)
val_dataloader = torch.utils.data.DataLoader(val_dataset, batch_size=batch_size,
                                             shuffle=False, num_workers=num_workers)

classes, classes_dict = get_classes()
labels_idxs = []
target_names = []
for el in classes_dict:
    target_names.append(el)
    labels_idxs.append(classes_dict[el])

#%% Load the net and use eval mode
logs_dir = './logs'
net = Net(in_channels=CHANNELS, out_features=NUM_CLASSES)
PATH = os.path.join(logs_dir, 'dog_vs_cat.pth')
net.load_state_dict(torch.load(PATH))

# Move the net on CUDA
cuda = torch.cuda.is_available()
if cuda:
    net = net.cuda()
net = net.eval()

#%% Make prediction on train set
y_true_train, y_pred_train = make_pred_on_dataloader(net, train_dataloader)

#%% Compute metrics on train set
cf_train = confusion_matrix(y_true_train, y_pred_train, labels=labels_idxs)
cr_train = classification_report(y_true_train, y_pred_train, target_names=target_names, output_dict=True)

print(classification_report(y_true_train, y_pred_train, target_names=target_names, output_dict=False))

#%% Make prediction on val set
y_true_test, y_pred_test = make_pred_on_dataloader(net, val_dataloader)

#%% Compute metrics on val set
cf_test = confusion_matrix(y_true_test, y_pred_test, labels=labels_idxs)
cr_test = classification_report(y_true_test, y_pred_test, target_names=target_names, output_dict=True)

print(classification_report(y_true_test, y_pred_test, target_names=target_names, output_dict=False))