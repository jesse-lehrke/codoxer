# Description
This package contains a model trained on code samples from the Google Code Jam Data
(see repo) to predict the author of a given code sample.

It consists of a command line tool that can predict any new code sample by written
by one of the Google Code Jam participants (see usage below).

Also included is a Trainer class that contains the architecture of the model. It
allows to retrain the model with any new data (see instructions below).

# Installation
- Downlaod repo
- Navigate to folder (codoxer) containing Makefile in Terminal
- Run:
```bash
    $ make install
```

# Usage

To predict code from one of the Google Code Jam participants:
- Navigate to folder containing code file in Terminal
- Run:
```bash
    $ codoxer-run <file>
```

# Retraining

The package contains a pipeline for the model that ca be used to retrain it on
new data. The data as to be in the following form:

include here

The class codoxer.Train() can then be trained using codoxer.Train.fit().
Afterwards predictions can be made with codoxer.Train.predict().
