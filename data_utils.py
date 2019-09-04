class CoNLLDataset(object):
    """
    Class that iterates over CoNLL Dataset
    """

    def __init__(self, filename, processing_word=None, processing_tag=None,
                 max_iter=None, all_line=True):
        """
        Args:
            filename: path to the file
            processing_words: (optional) function thsat takes a word as input
            processing_tags: (optional) function that takes a tag as input
            max_iter: (optional) max number of sentences to yield
        """
        self.filename = filename
        self.processing_word = processing_word
        self.processing_tag = processing_tag
        self.max_iter = max_iter
        self.length = None
        self.all_line = all_line

    def __iter__(self):
        try:
            niter = 0
            with open(self.filename, encoding='euc-kr') as f:
                words, tags = [], []
                for line in f:
                    line = line.strip()
                    if (len(line) == 0 or line.startswith("-DOCSTART-")):
                        if len(words) != 0:
                            niter += 1
                            if self.max_iter is not None and niter > self.max_iter:
                                break
                            yield words, tags
                            words, tags = [], []
                    else:
                        word, tag = line.split(' ')
                        if self.processing_word is not None:
                            word = self.processing_word(word)
                        if self.processing_tag is not None:
                            tag = self.processing_tag(tag)
                        words += [word]
                        tags += [tag]
        except Exception as e:
            raise Exception(e)

    def __len__(self):
        """
        Iterates once over the corpus to set and store length
        """
        if self.length is None:
            self.length = 0
            for _ in self:
                self.length += 1

        return self.length


def get_vocabs(datasets):
    """
    Args:
        datasets: a list of dataset objects
    Return:
        a set of all the words in the dataset
    """
    try:
        print("Building vocab...")
        vocab_words = set()
        vocab_tags = set()
        sentences = []
        labels = []
        for dataset in datasets:
            for words, tags in dataset:
                print(words, tags)
                vocab_words.update(words)
                vocab_tags.update(tags)
                sentence = ' '.join(words)
                sentences.append(sentence)
                labels.append(tags)
        print("- done. {} tokens".format(len(vocab_words)))
        return vocab_words, vocab_tags, sentences, labels
    except Exception as e:
        print("error on get_vacabs {0}".format(e))
