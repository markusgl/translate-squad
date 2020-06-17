import json
import os
import ntpath
import logging
import argparse

if __package__ is None or __package__ == '':
    from answer_start.answer_finder import AnswerFinder
    from sentence_tokenizer import SentenceTokenizer
else:
    from .answer_start.answer_finder import AnswerFinder
    from .sentence_tokenizer import SentenceTokenizer

from google.cloud import translate


logger = logging.getLogger('translate_squad')
fh = logging.FileHandler('translate_squad.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


class SquadTranslation:
    def __init__(self):
        self.tokenizer = SentenceTokenizer()
        self.answer_finder = AnswerFinder()
        self.answer_start_not_found_count = 0
        self.mock = True
        self.translated_characters = 0

    def safe_json_to_file(self, file_path, json_data):
        self.create_directory_for_file(file_path)
        with open(file_path, 'w+', encoding='utf-8') as f:
            logger.info(f'writing paragraph to file {file_path}')
            json.dump(json_data, f)

    @staticmethod
    def read_json_file(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.loads(f.read())

    def translate_text(self, text, target_lang = "de") -> object:
        if self.mock:
            logger.debug('mocking translation...')
            return text

        logger.debug('sending text to Translation API ...')
        client = translate.TranslationServiceClient()
        # TODO project id
        project_id = '1234'
        translation = client.translate_text(contents=[text],
                                            parent=client.location_path(project_id, 'us-central1'),
                                            source_language_code='en',
                                            target_language_code=target_lang)

        return translation['translatedText']

    @staticmethod
    def strip_filename_from_path(file_path):
        file_name = ntpath.basename(file_path)
        return file_path.replace(file_name, '')

    def create_directory_for_file(self, file_path):
        path_name = self.strip_filename_from_path(file_path)

        if os.path.exists(path_name):
            logger.debug(f'path {path_name} already exists')
        else:
            try:
                os.makedirs(path_name)
                logger.info(f'creating directory {path_name}')
            except FileNotFoundError:
                logger.error(f'path name "{path_name}" not found or invalid')

    def read_stored_dataset(self, filename):
        if os.path.exists(filename):
            json_data = self.read_json_file(filename)
        else:
            json_data = {"data": [], "version": "1.1"}

        return json_data

    def store_paragraph_to_file(self, translated_paragraphs, out_file, chkp_file):
        logger.debug(f'reading previous chkp-file {chkp_file}')
        current_squad = self.read_stored_dataset(chkp_file)
        current_data = current_squad['data']

        logger.debug(f'appending translate paragraph ...')
        current_data.append(translated_paragraphs)
        current_squad['data'] = current_data

        self.safe_json_to_file(f'{out_file}', current_squad)

    def find_sentence_number(self, answer_start, context):
        """
        find in which sentence the original answer was
        :param answer_start: original answer start number
        :param context: original context (english)
        :return: sentence number of the sentenized context
        """
        sentences = self.tokenizer.tokenize_sentence(context)

        char_count = 0
        for i, sent in enumerate(sentences):
            char_count += len(sent) + 1
            if char_count >= answer_start:
                return i

    def get_answer_start_in_context(self, sentence_number, answer_start_in_sentence, context):
        """
        determines the final answer_start inside the translated context based on the sentence number, answer start
        inside the sentence and translated context
        :param context: translated context
        :param sentence_number:
        :param answer_start_in_sentence:
        :return: answer_start number in translated context
        """
        sentenized_context = self.tokenizer.tokenize_sentence(context)

        context_len_bef_answer = 0
        for sent in sentenized_context[:sentence_number]:
            context_len_bef_answer += len(sent) + 1  # add one for the space after each full stop

        return answer_start_in_sentence + context_len_bef_answer

    def translate_squad_dataset(self, input_file_path, output_dir, threshold=0.5, mock=True, character_limit=-1,
                                verbose=False):
        self.mock = mock
        if verbose:
            logger.setLevel(logging.DEBUG)
            fh.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
            fh.setLevel(logging.INFO)

        qas_count = 0
        question_count = 0
        input_file_name = ntpath.basename(input_file_path)
        output_filename = input_file_name.replace('.json', '_translated.json')
        output_filepath = f'{output_dir}/{output_filename}'

        if mock:
            logger.info('Mocking translation... Text will not be send to Translate API')

        if character_limit > 1:
            logger.info(f'Character limit set to {character_limit}. '
                        f'After limit is reached the current paragraph will be finished.')

        with open(input_file_path, 'r', encoding='utf-8') as f:
            raw_data = json.loads(f.read())
            squad_dataset = raw_data['data']
            count_paragraphs = 0
            count_paragraphs, squad_dataset = self.proceed_existing_chkp_file(count_paragraphs, output_filepath,
                                                                              squad_dataset)

            logger.info('Starting translation...')
            for squad_data in squad_dataset:
                if self.translated_characters >= character_limit > 0:
                    logger.info(f'Character limit of {character_limit} exceeded.')
                    break

                # take title as is without translation
                translated_data = {'title': squad_data['title']}
                translated_paragraphs = []

                qas_count, question_count= self.iterate_paragraphs(character_limit,
                                                                   qas_count,
                                                                   question_count,
                                                                   squad_data,
                                                                   threshold,
                                                                   translated_paragraphs)
                translated_data['paragraphs'] = translated_paragraphs
                self.store_paragraph_to_file(out_file=f'{output_filepath}_chkp{count_paragraphs}',
                                             chkp_file=f'{output_filepath}_chkp{count_paragraphs-1}',
                                             translated_paragraphs=translated_data)
                count_paragraphs += 1
                logger.info(f'translated characters {self.translated_characters}')

            logger.info(f'Translation finished. \n\n**** Summary **** \n'
                        f'Translated_characters: {self.translated_characters} \n'
                        f'answer_starts not found: {self.answer_start_not_found_count}\n'
                        f'Pargraphs: {count_paragraphs} \n'
                        f'QAS: {qas_count} \n'
                        f'Questions: {question_count}\n'
                        f'Final chkp-file: {output_filepath}_chkp{count_paragraphs-1}\n'
                        f'Out file: {output_filepath}\n')

    def iterate_paragraphs(self, character_limit, qas_count, question_count, squad_data, threshold,
                           translated_paragraphs):
        for paragraph in squad_data['paragraphs']:
            if self.translated_characters >= character_limit > 0:
                logger.info(f'Character limit of {self.translated_characters} exceeced ')
                break

            qas_data = []
            orig_context = paragraph['context']
            translated_context = self.translate_text(paragraph['context'])
            self.translated_characters += len(translated_context)
            qas_count += 1
            question_count, translated_characters = self.iterate_qas(orig_context,
                                                                     paragraph,
                                                                     qas_data,
                                                                     question_count,
                                                                     threshold,
                                                                     translated_context)
            translated_paragraphs.append({'context': translated_context, 'qas': qas_data})

        return qas_count, question_count

    def iterate_qas(self, orig_context, paragraph, qas_data, question_count, threshold, translated_context):
        for qa in paragraph['qas']:
            question = self.translate_text(qa['question'])
            question_count += 1
            self.translated_characters += len(question)
            answers = qa['answers']

            answer_texts = self.iterate_answers(answer_texts, answers, orig_context, threshold, translated_context)

            qas_data.append({'answers': answer_texts, 'question': question, 'id': qa['id']})

        return question_count

    def iterate_answers(self, answers, orig_context, threshold, translated_context):
        answer_texts = []
        for answer in answers:
            translated_answer = self.translate_text(answer['text'])

            if self.mock:  # use original answer_start to save time
                answer_start = answer['answer_start']
            else:
                answer_start, translated_answer = self.answer_start_probability(answer,
                                                                                orig_context,
                                                                                threshold,
                                                                                translated_answer,
                                                                                translated_context)
            self.translated_characters += len(translated_answer)
            if not answer_start == -1:
                answer_texts.append({'answer_start': answer_start, 'text': translated_answer})

        return answer_texts

    def answer_start_probability(self, answer, orig_context, threshold, translated_answer, translated_context):
        """
        Use 'answer_start' and the answer found in the translated context if word embedding matching probability is
        higher than 0.5 - otherwise use original answer_start
        """
        answer_pos, p_result, sentence_number, substring = self.search_answer_in_translated_context(answer,
                                                                                                    orig_context,
                                                                                                    threshold,
                                                                                                    translated_answer,
                                                                                                    translated_context)
        if p_result > threshold:
            answer_start = self.get_answer_start_in_context(sentence_number=sentence_number,
                                                            answer_start_in_sentence=answer_pos,
                                                            context=translated_context)
            logger.debug(f'answer_start found - probability {p_result} \n translated answer "{translated_answer}" '
                         f'- most similar substring in translated context "{substring}"')
            # use tje substring from translated context as answer
            translated_answer = substring
        else:
            self.answer_start_not_found_count += 1
            logger.warning(f'answer_start for "{translated_answer}" not found, probability '
                           f'{p_result} lower than threshold {threshold} - using original '
                           f'answer_start')
            # TODO otherwise delete the whole question and answer as it is not helpful for training a neural net
            # answer_start = answer['answer_start']
            # set to negative number to indicate that this answer should be deleted from translated data set
            answer_start = -1

        return answer_start, translated_answer

    def search_answer_in_translated_context(self, orig_answer, orig_context, threshold, translated_answer,
                                            translated_context):
        """
        find in which sentence of the context the original answer is and search only in the same sentence as in the
        original context. If the sentence array of the translated context is longer than in of the original context,
        searches in whole context. This mostly comes from a different sentence splitting in original and translated
        context.
        """
        sentence_number_orig_context = self.find_sentence_number(answer_start=orig_answer['answer_start'],
                                                                 context=orig_context)
        sentence_tokenized_translated_context = self.tokenizer.tokenize_sentence(translated_context)

        if sentence_number_orig_context >= len(sentence_tokenized_translated_context):
            logger.warning("could not find sentence of answer - using whole context for search")
            answer_pos, p_result, substring = self.answer_finder.find_answer_in_context(translated_answer,
                                                                                        translated_context)
        else:
            sentence_to_search = sentence_tokenized_translated_context[sentence_number_orig_context]
            logger.debug(f'Sentence to search: "{sentence_to_search}"')
            answer_pos, p_result, substring = self.answer_finder.find_answer_in_context(translated_answer,
                                                                                        sentence_to_search)

            # Search again in whole context if the answer was not found in the specific sentence
            # This is because the sentence tokenizing does not split always properly
            if p_result < threshold:
                logger.warning("could not find answer in sentence   - using whole context for search")
                answer_pos, p_result, substring = self.answer_finder.find_answer_in_context(translated_answer,
                                                                                            translated_context)
        return answer_pos, p_result, sentence_number_orig_context, substring

    def proceed_existing_chkp_file(self, count_paragraphs, output_filepath, squad_dataset):
        """
        check if checkpoint file from previous translation exists and use it
        """
        for j in reversed(range(len(squad_dataset))):
            if os.path.exists(f'{output_filepath}_chkp{j}'):
                logger.info(f'checkpoint file found at "{output_filepath}_chkp{j}" - restoring file..."')
                json_data = self.read_stored_dataset(f'{output_filepath}_chkp{j}')
                len_stored_data = len(json_data['data'])
                squad_dataset = squad_dataset[len_stored_data:]
                count_paragraphs = len_stored_data
                break
        return count_paragraphs, squad_dataset

    @staticmethod
    def concatenate_datasets():
        concat_squad = {"data": []}

        with open('data/concat/dev-v1.1.json', 'r', encoding='utf-8') as f:
            raw_data = json.loads(f.read())
            squad_dataset = raw_data['data']

        with open('data/concat/dev-v1.1_de_10000.json', 'r', encoding='utf-8') as f:
            raw_data = json.loads(f.read())
            squad_de_dataset = raw_data['data']

        for data in squad_de_dataset:
            squad_dataset.append(data)

        concat_squad['data'] = squad_dataset

        with open('data/concat/dev-v1.1_de_en.json', 'w+', encoding='utf-8') as f:
            json.dump(concat_squad, f)

    def analyze_dataset(self, filename):
        squad_dataset = self.read_json_file(filename)
        squad_data = squad_dataset['data']

        qas_length = 0
        characters = 0
        paragraphs_length = len(squad_data)

        for data in squad_data:
            paragraphs = data['paragraphs']
            for paragraph in paragraphs:
                qas_length += len(paragraph['qas'])
                characters += len(paragraph['context'])

                for qas in paragraph['qas']:
                    characters += len(qas['question'])
                    for answer in qas['answers']:
                        characters += len(answer['text'])

        print(f'\nparagraphs: {paragraphs_length}')
        print(f'qas: {qas_length}')
        print(f'translated characters: {characters}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Translation of SQuAD1.1 via Google Translate API')
    parser.add_argument('squadinputfile',
                        help='file path to the SQuAD1.1 train or dev file (e.g. "data/train-v1.1.json")')
    parser.add_argument('outputdir',
                        help='output directory without file ending (e.g. "data/translated")'
                             ' \nNote: There will be many checkpoint files wirtten to this directory '
                             '(one for each paragraph inside SQuAD!)')
    parser.add_argument('-m', '--mock',
                        help="if set, don't send any text to Google Translate API (default: False)",
                        action='store_true',
                        default=False)
    parser.add_argument('-t', '--threshold',
                        help="threshold for the probability of matching an answer inside the translated context"
                             "default: 0.5",
                        type=float,
                        default=0.5)
    parser.add_argument('-c', '--character_limit',
                        help='limits the number of chracters to be send to Google Translate API. '
                             'Note: the current paragraph will be finished after the limit is reached, to store '
                             'a valid JSON file. '
                             'This means, that usually more characters will be translated than set'
                             '-1 for no limit (default)',
                        type=int,
                        default=-1)
    parser.add_argument('-v', '--verbose',
                        help='print out all debug infos',
                        action='store_true',
                        default=False)
    args = parser.parse_args()

    SquadTranslation().translate_squad_dataset(input_file_path=args.squadinputfile,
                                               output_dir=args.outputdir,
                                               mock=args.mock,
                                               threshold=args.threshold,
                                               character_limit=args.character_limit,
                                               verbose=args.verbose)
