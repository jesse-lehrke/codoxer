# Description
This package contains a model trained on code samples from the Google Code Jam Data
(see repo https://github.com/Jur1cek/gcj-dataset) to predict the author of a given code sample.

The package consists of a command line tool that can predict any new code sample by written
by one of the Google Code Jam participants included in the trained model (see usage below). Coders included in the trained model are listed in trained_classes.txt.

Also included is a Trainer class that contains the architecture of the model. It
allows one to retrain the model with any new data (see instructions below).

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

The package contains a pipeline for the model that can be used to retrain it on
new data. The data has to be in the following form:

- series of username (target) as a string
- series of code as a string

The class codoxer.Train() can then be trained using codoxer.Train.fit().
Afterwards predictions can be made with codoxer.Train.predict().



For file organization see file_tree.txt

.
├── codoxer \n
│   ├── basic_cnn.py\n
│   ├── cnn_model.py\n
│   ├── data\n
│   │   ├── data.csv.gz\n
│   │   ├── test\n
│   │   ├── testing_data.csv\n
│   │   └── tokens.csv\n
│   ├── data.py\n
│   ├── filter.py
│   ├── __init__.py
│   ├── lib.py
│   ├── make_tokens.py
│   ├── models.py
│   ├── mvp.py
│   ├── nb_mvp.py
│   ├── tfidf.py
│   ├── tokenizer.py
│   ├── trainer.py
│   ├── transformers.py
│   └── utils.py
├── file_tree.txt
├── Makefile
├── MANIFEST.in
├── notebooks
│   ├── Kafkaese_silly_model.ipynb
│   └── tokenizer.ipynb
├── README.md
├── requirements.txt
├── scripts
│   ├── codoxer-run
│   └── codoxer-run.py
├── setup.py
├── tests
│   └── __init__.py
└── trained_classes.txt

5 directories, 31 files
