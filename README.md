# translate-squad  
Machine Translating SQuAD1.1 with Google Cloud Translation API
 
This is an application for translating the popular Question Answering Dataset 
[SQuAD](https://rajpurkar.github.io/SQuAD-explorer/) using Machine Translation with 
[Google Cloud Translation API](https://cloud.google.com/translate/docs). 

## Important notes
**WARNING CLOUD TRANSLATION CAUSES COSTS!**   
You need a valid *Google Cloud Platform* (GCP) Account and an activated *Cloud Translation API* for real translation 
(see [Google's  Setup Guide](https://cloud.google.com/translate/docs/setup)). **Note that Cloud Translation API is NOT 
for free and will cause high costs if you translate the whole dataset** 
(see [Pricing](https://cloud.google.com/translate/pricing/)). The 
SQuAD training dataset (train-v1.1.json) has about 20 million characters, so translation costs will be over 400$. 
You can also translate only a subset of the dataset using the *-c* parameter (see usage below) with the number of 
characters to translate. Note that the application will not stop exactly when this number is reached and will finish 
the current paragraph to always output a valid JSON and SQuAD structure that can be used to continue translation or for 
training Machine Learning System like BERT. 

#### Further notes
If you sign up new to GCP you get a 300$ free trial for 30 days, that you can use.

This application will create checkpoint files after each translated paragraph for reliability reasons and to allow 
to continue translation later on.
  
## Usage

### translate_squad_1_1.py
The main file and starting point for translation. You should run the script in a VirtualEnv (`venv`) and install the 
requirements first using `pip` or similar.


#### Example usages
Getting Help:  
`python translate_squad_1_1.py --help` 

Translate the whole dataset with default settings:   
`python translate_squad_1_1.py data/train-v1.1.json data/translated` 

Parameter `-m` allows mocking the translations without using Google Translate. This is meant 
for testing purposes, to see whether the JSON structure is correct or similar.  
`python translate_squad_1_1.py data/train-v1.1.json data/translated -m`  

Parameter `-c` limits the number of characters sent to Google Translate to reduce costs. **Note:** The 
application does not stop immediately when the limit is reached, but finishes the current paragraph to 
always get a well formed JSON and SQuAD structure that can be used for training ML systems. This means 
if you set the limit to 1000 (costs 0,02$) it might be 1300 (costs 0,026$) characters in total.  
`python translate_squad_1_1.py data/train-v1.1.json data/translated -c 1000`

Parameter `-t` allows you to change the threshold probability a answer must exceed in the 
translated context, to be recognized as the correct answer.  
`python translate_squad_1_1.py data/train-v1.1.json data/translated -t 0.6` 

#### Prerequisites
 
Needs PyTorch before installing flair: https://pytorch.org/get-started/locally/  
If you get errors while installing flair, try to install tiny-tokenizer first: `pip install tiny-tokenizer`

Tested with Python 3.8 on Windows
 