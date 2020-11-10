# translate-squad  
Machine Translating SQuAD1.1 with Google Translate API
 
This is an application for translating the popular Question Answering Dataset 
[SQuAD](https://rajpurkar.github.io/SQuAD-explorer/) using Machine Translation with 
[Google Translate API](https://cloud.google.com/translate/docs). 
You need a valid GCP Account and add your key to the code. 

**Note that Google Translate API is NOT for free and will 
cause high costs if you translate the whole dataset** (see [Pricing](https://cloud.google.com/translate/pricing/)). The 
SQuAD training dataset (train-v1.1.json) has about 20 million characters, so translation costs will be over 400$. 
You can also only translate a subset of the dataset using the *-c* (character_limit) parameter with the number of characters 
to translate. Note that the application will not stop exactly when this number is reached and will finish the current 
paragraph to always output a valid JSON and SQuAD structure that can be used to continue translation and for training of 
some Machine Learning System like BERT.

The Application will also create checkpoint files after each translated paragraph for reliability reasons and to allow 
to continue translation later on.
  
## Usage
**Warning: Running this script with your GCP (Google Cloud Platform) key may cause high costs (read above)!**  

### translate_squad_1_1.py
The main file and starting point for translation. You should run the script in a VirtualEnv (`venv`) and install the 
requirements first using `pip` or similar.


#### Example usages
Getting Help:  
`python translate_squad_1_1.py --help` 

Translate the whole dataset:   
`python translate_squad_1_1.py data/train-v1.1.json data/translated` 

Parameter `-m` allows mocking the translations without Google Translate:  
`python translate_squad_1_1.py data/train-v1.1.json data/translated -m`  


```
python translate_squad_1_1.py data/train-v1.1.json data/translated -c 1000
```

```
python translate_squad_1_1.py data/train-v1.1.json data/translated -t 0.6
```  


 
Needs PyTorch before instlling flair: https://pytorch.org/get-started/locally/
If you get errors while installing flair, try to install tiny-tokenizer first: `pip install tiny-tokenizer`