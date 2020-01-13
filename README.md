# translate-squad
Machine Translation of SQuAD1.1 using Google Translate API  
**Warning: Running this script may cause costs!**  

## translate_squad_1_1.py 
Parameter `-m` allows mocking the translations without Google Translate

Example usage: `translate_squad_1_1.py data/train-v1.1.json data/translated_train`  
Help: `translate_squad_1_1.py --help` 
 
Needs PyTorch before instlling flair: https://pytorch.org/get-started/locally/
If you get errors while installing flair, try to install tiny-tokenizer first: `pip install tiny-tokenizer`