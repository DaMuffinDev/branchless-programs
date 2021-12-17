import os.path
from enum import Enum
import sys


__all__ = ['get_tokens']


with open("../documentation/tokenize-doc.txt", "r") as DOC_FILE:
    __doc__ = DOC_FILE.read()


class TOKEN(Enum):
    ID = 0
    STRING = 1  # "" or ''
    UNDERSCORE = 3  # _

    LPAREN = 100  # (
    RPAREN = 101  # )
    LBRACKET = 102  # [
    RBRACKET = 103  # ]
    LCURLY = 104  # {
    RCURLY = 105  # }

    EXLAM = 200  # !
    COMMA = 201  # ,
    PERIOD = 202  # .
    DOLLAR = 203  # $
    COLON = 204  # :
    SEMI = 205  # ;
    ANDSIGN = 206  # &
    EQUALS = 207  # =
    ATSIGN = 208  # @

    EXPON = 300  # **
    STAR = 301  # *
    SLASH = 302  # /
    PLUS = 303  # +
    MINUS = 304  # -
    PERCENT = 305  # %
    GREATERTHAN = 306  # >
    LESSTHAN = 307  # <
    GREATER_EQUALS = 308  # >=
    LESS_EQUALS = 309  # <=
    CARET = 310  # ^

    HASHTAG = 400  # #
    TILDE = 401  # ~
    QUESTION = 402  # ?
    BACKTICK = 403  # `


def init_token(__type, __value):
    return {
        'type': __type,
        'value': __value
    }


class Tokenizer:
    def __init__(self, __code):
        self.contents = __code
        self.index = 0
        self.char = self.contents[self.index]

    def __advance(self):
        self.index += 1
        self.char = self.contents[self.index]

    def advance(self):
        advance_conditional = {1: self.__advance}
        try: advance_conditional[(self.index < (len(self.contents)))]()
        except (KeyError, IndexError): pass

    def advance_with_token(self, token):
        self.advance()
        return token

    def skip_whitespace(self):
        while self.char == ' ' or self.char == "\n":
            self.advance()

    def collect_string(self, quotation):
        self.advance()

        string_template = ""
        while not self.char == quotation:
            string_template += self.char
            self.advance()

        self.advance()
        return init_token(TOKEN.STRING.value, string_template)

    def collect_id(self):
        id_template = ""
        while self.char.isalnum():
            id_template += self.char
            self.advance()

        return init_token(TOKEN.ID.value, id_template)

    def get_next_token(self):
        space_conditional = {1: self.skip_whitespace}
        id_conditional = {1: self.collect_id}
        is_single_quote_conditional = {1: (lambda: self.collect_string("'"))}
        is_double_quote_conditional = {1: (lambda: self.collect_string('"'))}

        is_underscore_conditional = {1: (lambda: self.advance_with_token(init_token(TOKEN.UNDERSCORE.value, "_")))}
        is_lparen_conditional = {1: (lambda: self.advance_with_token(init_token(TOKEN.LPAREN.value, "(")))}
        is_rparen_conditional = {1: (lambda: self.advance_with_token(init_token(TOKEN.RPAREN.value, ")")))}
        is_lbracket_conditional = {1: (lambda: self.advance_with_token(init_token(TOKEN.LBRACKET.value, "[")))}
        is_rbracket_conditional = {1: (lambda: self.advance_with_token(init_token(TOKEN.RBRACKET.value, "]")))}
        is_lcurly_conditional = {1: (lambda: self.advance_with_token(init_token(TOKEN.LCURLY.value, "{")))}
        is_rcurly_conditional = {1: (lambda: self.advance_with_token(init_token(TOKEN.RCURLY.value, "}")))}

        is_exlam_conditional = {1: (lambda: self.advance_with_token(init_token(TOKEN.EXLAM.value, "!")))}
        is_comma_conditional = {1: (lambda: self.advance_with_token(init_token(TOKEN.COMMA.value, ",")))}
        is_period_conditional = {1: (lambda: self.advance_with_token(init_token(TOKEN.PERIOD.value, ".")))}
        is_dollar_conditional = {1: (lambda: self.advance_with_token(init_token(TOKEN.DOLLAR.value, "$")))}
        is_colon_conditional = {1: (lambda: self.advance_with_token(init_token(TOKEN.COLON.value, ":")))}
        is_semi_conditional = {1: (lambda: self.advance_with_token(init_token(TOKEN.SEMI.value, ";")))}
        is_andsign_conditional = {1: (lambda: self.advance_with_token(init_token(TOKEN.ANDSIGN.value, "&")))}
        is_equals_conditional = {1: (lambda: self.advance_with_token(init_token(TOKEN.EQUALS.value, "=")))}
        is_atsign_conditional = {1: (lambda: self.advance_with_token(init_token(TOKEN.ATSIGN.value, "@")))}

        is_star_conditional = {1: (lambda: self.advance_with_token(init_token(TOKEN.STAR.value, "*")))}
        is_slash_conditional = {1: (lambda: self.advance_with_token(init_token(TOKEN.SLASH.value, "/")))}
        is_plus_conditional = {1: (lambda: self.advance_with_token(init_token(TOKEN.PLUS.value, "+")))}
        is_minus_conditional = {1: (lambda: self.advance_with_token(init_token(TOKEN.MINUS.value, "-")))}
        is_percent_conditional = {1: (lambda: self.advance_with_token(init_token(TOKEN.PERCENT.value, "%")))}
        is_geaterthan_conditional = {1: (lambda: self.advance_with_token(init_token(TOKEN.GREATERTHAN.value, ">")))}
        is_lessthan_conditional = {1: (lambda: self.advance_with_token(init_token(TOKEN.LESSTHAN.value, "<")))}
        is_caret_conditional = {1: (lambda: self.advance_with_token(init_token(TOKEN.CARET.value, "^")))}

        is_hasttag_conditional = {1: (lambda: self.advance_with_token(init_token(TOKEN.HASHTAG.value, "#")))}
        is_tilde_conditional = {1: (lambda: self.advance_with_token(init_token(TOKEN.TILDE.value, "~")))}
        is_question_conditional = {1: (lambda: self.advance_with_token(init_token(TOKEN.QUESTION.value, "?")))}
        is_backtick_conditional = {1: (lambda: self.advance_with_token(init_token(TOKEN.BACKTICK.value, "`")))}

        while not self.char == '\0' and self.index < len(self.contents):
            try: space_conditional[(self.char == " " or self.char == "\n") + 0]()
            except KeyError: pass

            try:
                is_all_num = id_conditional[(self.char.isalnum())]()
                return is_all_num
            except KeyError: pass

            try:
                is_single_quote = is_single_quote_conditional[(self.char == "'") + 0]()
                return is_single_quote
            except KeyError: pass
            try:
                is_double_quote = is_double_quote_conditional[(self.char == '"') + 0]()
                return is_double_quote
            except KeyError: pass


            try:
                _ = is_underscore_conditional[(self.char == "_") + 0]()
                return _
            except KeyError: pass
            try:
                _ = is_lparen_conditional[(self.char == "(") + 0]()
                return _
            except KeyError: pass
            try:
                _ = is_rparen_conditional[(self.char == ")") + 0]()
                return _
            except KeyError: pass
            try:
                _ = is_lbracket_conditional[(self.char == "[") + 0]()
                return _
            except KeyError: pass
            try:
                _ = is_rbracket_conditional[(self.char == "]") + 0]()
                return _
            except KeyError: pass
            try:
                _ = is_lcurly_conditional[(self.char == "{") + 0]()
                return _
            except KeyError: pass
            try:
                _ = is_rcurly_conditional[(self.char == "}") + 0]()
                return _
            except KeyError: pass
            try:
                _ = is_exlam_conditional[(self.char == "!") + 0]()
                return _
            except KeyError: pass
            try:
                _ = is_comma_conditional[(self.char == ",") + 0]()
                return _
            except KeyError: pass
            try:
                _ = is_period_conditional[(self.char == ".") + 0]()
                return _
            except KeyError: pass
            try:
                _ = is_dollar_conditional[(self.char == "$") + 0]()
                return _
            except KeyError: pass
            try:
                _ = is_colon_conditional[(self.char == ":") + 0]()
                return _
            except KeyError: pass
            try:
                _ = is_semi_conditional[(self.char == ";") + 0]()
                return _
            except KeyError: pass
            try:
                _ = is_andsign_conditional[(self.char == "&") + 0]()
                return _
            except KeyError: pass
            try:
                _ = is_equals_conditional[(self.char == "=") + 0]()
                return _
            except KeyError: pass
            try:
                _ = is_atsign_conditional[(self.char == "@") + 0]()
                return _
            except KeyError: pass

            try:
                _ = is_star_conditional[(self.char == "*") + 0]()
                return _
            except KeyError: pass
            try:
                _ = is_slash_conditional[(self.char == "/") + 0]()
                return _
            except KeyError: pass
            try:
                _ = is_plus_conditional[(self.char == "+") + 0]()
                return _
            except KeyError: pass
            try:
                _ = is_minus_conditional[(self.char == "-") + 0]()
                return _
            except KeyError: pass
            try:
                _ = is_percent_conditional[(self.char == "%") + 0]()
                return _
            except KeyError: pass
            try:
                _ = is_geaterthan_conditional[(self.char == ">") + 0]()
                return _
            except KeyError: pass
            try:
                _ = is_lessthan_conditional[(self.char == "<") + 0]()
                return _
            except KeyError: pass
            try:
                _ = is_caret_conditional[(self.char == "^") + 0]()
                return _
            except KeyError: pass

            try:
                _ = is_hasttag_conditional[(self.char == "#") + 0]()
                return _
            except KeyError: pass
            try:
                _ = is_tilde_conditional[(self.char == "~") + 0]()
                return _
            except KeyError: pass
            try:
                _ = is_question_conditional[(self.char == "?") + 0]()
                return _
            except KeyError: pass
            try:
                _ = is_backtick_conditional[(self.char == "`") + 0]()
                return _
            except KeyError: pass

        return None

    def collect_tokens(self):
        tokens = []
        current_token = self.get_next_token()

        while current_token is not None:
            tokens.append(current_token)
            current_token = self.get_next_token()
        return tokens


def __print_tokens(tokens):
    for token in tokens:
        print(f"TOKEN({token['type']}, {token['value']})")


def __save_tokens(tokens, file, new_line=False):
    is_null_conditional = {1: (lambda: print("[ERROR]: There is no specified file to save the tokens to."))}
    does_file_exists_conditional = {1: (lambda file_name: print(f"[ERROR]: \"{file_name}\" does not exist!"))}
    new_line_conditional = {0: (lambda _: _), 1: (lambda _: f"{_}\n")}

    try:
        is_null_conditional[(file is None)]()
        sys.exit(1)
    except KeyError: pass

    try:
        does_file_exists_conditional[(os.path.exists(os.path.join(os.getcwd(), file.split(".")[0]))) + 0](file)
        sys.exit(1)
    except KeyError: pass

    with open(file, "w") as f:
        for token in tokens: f.write(new_line_conditional[bool(new_line) + 0](token))


def get_tokens(file):
    does_file_exists_conditional = {1: (lambda file_name: print(f"[ERROR]: \"{file_name}\" does not exist!"))}

    try:
        does_file_exists_conditional[(os.path.exists(os.path.join(os.getcwd(), file.split(".")[0]))) + 0](file)
        sys.exit(1)
    except KeyError: pass

    with open(file, "r") as f:
        tokenizer = Tokenizer(f.read())

    return tokenizer.collect_tokens()


def main():
    print_conditional = {1: __print_tokens}
    save_conditional = {1: __save_tokens}

    file_name = sys.argv[1]
    command = sys.argv[2]
    try: save_file = sys.argv[3]
    except IndexError: save_file = None
    try: new_lines = sys.argv[4]
    except IndexError: new_lines = False

    with open(file_name, "r") as FILE:
        tokenizer = Tokenizer(FILE.read())

    try: print_conditional[(command == "print") + 0](tokenizer.collect_tokens())
    except KeyError: pass

    try: save_conditional[(command == "save") + 0](tokenizer.collect_tokens(), save_file, new_lines)
    except KeyError: pass


if __name__ == "__main__":
    main()
