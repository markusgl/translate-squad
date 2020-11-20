import hashlib
import shutil
from unittest import TestCase

from translate_squad_1_1 import SquadTranslation


class TestSquadTranslation(TestCase):
    def test_squad_translation_with_mock_dev(self):
        input_file_path = "../data/dev-v1.1.json"
        output_dir = "data/test_translated"
        squad_translation = SquadTranslation(mock=True)
        squad_translation.translate_squad_dataset(input_file_path, output_dir, threshold=0.5, mock=True,
                                                  character_limit=-1, verbose=False)

        input_md5 = hashlib.md5(open(input_file_path, 'rb').read()).hexdigest()
        output_md5 = hashlib.md5(open(output_dir + "/dev-v1.1_translated.json_chkp47", 'rb').read()).hexdigest()

        shutil.rmtree(output_dir)
        assert input_md5 == output_md5

    def test_squad_translation_with_mock_train(self):
        input_file_path = "../data/train-v1.1.json"
        output_dir = "data/test_translated"
        squad_translation = SquadTranslation(mock=True)
        squad_translation.translate_squad_dataset(input_file_path, output_dir, threshold=0.5, mock=True,
                                                  character_limit=-1, verbose=False)

        input_md5 = hashlib.md5(open(input_file_path, 'rb').read()).hexdigest()
        output_md5 = hashlib.md5(open(output_dir + "/train-v1.1_translated.json_chkp441", 'rb').read()).hexdigest()

        shutil.rmtree(output_dir)
        assert input_md5 == output_md5

