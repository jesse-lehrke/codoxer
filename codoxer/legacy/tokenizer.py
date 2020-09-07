import spacy

class TokenizerWhitespace():

    def __init__(self, charwise=False):
        self.charwise = charwise

    def tokenize(self, text):
        nlp = spacy.load('en_core_web_sm')
        doc=nlp(text)
        token_texts = []
        for token in doc:
            token_texts.append(token.text)
            if token.whitespace_:  # filter out empty strings
                token_texts.append(token.whitespace_)
        for i in range(len(token_texts) - 1):
            if token_texts[i]==' ' and token_texts[i+1].startswith(' '):
                token_texts[i+1] = token_texts[i+1] + ' '
                del token_texts[i]
        if self.charwise:
            token_chars = []
            for word in token_texts:
                for char in word:
                    token_chars.append(char)
            return token_chars
        else:
            return token_texts
