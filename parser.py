# desmos reserved keywords. think function names, and other verbs
# like with, etc.
reserved_keywords = "sin cos tan csc sec cot mean median min max quertile quantile stdev stdevp var mad cov covp corr spearman stats count total join sort shuffle unique for histogram dotplot boxplot normaldist tdist poissondist binomialdist uniformdist pdf cdf inversecdf random ttest tscore ittest frac sinh cosh tanh csch sech coth polygon distance midpoint rgb hsv lcm gcd mod ceil floor round sign nPr nCr log with cdot to in length left right"
reserved_keywords = reserved_keywords.split(' ')

def continue_lines(string):
    # if there's a '\' and then a newline, ignore the newline.
    return string.replace('\\\n', '')

def replace_multiplication(string):
    return string.replace('*', '\\cdot ')

def replace_actions(string):
    return string.replace(' ->', '\\to ').replace('->', '\\to ')

def replace_tabs(string):
    return string.replace('\t', '    ')

def split_linewise(string):
    return string.split('\n')

def merge_multiple_spaces(string):
    return ' '.join(string.split())

def make_spaces_permanant(string):
    return string.replace(' ', '\\ ')

def subscriptize(string):
    output = ""
    buffer = ""
    for char in (string + "\n"): # add a newline so there's always a non-alpha char at the end
        if char.isalpha():
            buffer += char

        else:
            if buffer:
                # check if our buffer is a reserved word; if so, do
                # not expand.
                if not buffer in reserved_keywords:
                    if len(buffer) > 1:
                        output += "{}_{{{}}}".format(buffer[0], buffer[1:])
                    else:
                        output += buffer[0]
                else:
                    output += buffer
    
            buffer = ""
            output += char

    return output.rstrip()

class Statement:
    def __init__(self, commands, latex):
        self.commands = commands
        self.latex = latex
    
    def __getitem__(self, item):
        try:
            return self.commands[item]
        except KeyError:
            return None

    def __repr__(self):
        return "{} : {}".format(str(self.commands), self.latex)
    
    @classmethod
    def from_line(cls, line):
        if not line:
            return None

        if line[0] == "#": # ignore comments
            return None
        
        splitted = line.split(':')
        commands = splitted[0]
        latex = ':'.join(splitted[1:])

        commands = commands.split(' ')
        iterator = iter(commands)
        commands = dict(zip(iterator, iterator))

        try:
            del commands['']
        except KeyError:
            pass

        return cls(commands, latex)

    @classmethod
    def from_lines(cls, lines):
        output = []
        for line in lines:
            output.append(cls.from_line(line))
        
        return list(
            filter(
                lambda item: item is not None,
                output
            )
        )


class Parser:
    """
    Implements the parsing of the Desmos local DSL.

    General syntax:
    option1 value1 option2 value2 option3 value3 : latex

    in latex statements, multiplication between variables is *not* implicit.
    this is because
    `testing`
    becomes
    `t_{esting}`.

    In order to multiple two variables together, use
    `a * b`
    instead of
    `ab`.    

    """
    def __init__(self, file):
        self.file = file
        self.ast = []

    def parse(self):
        with open(self.file, "r") as f:
            text = f.read()

        text = continue_lines(text)
        text = replace_multiplication(text)
        text = replace_actions(text)
        text = replace_tabs(text)
        lines = split_linewise(text)
        lines = Statement.from_lines(lines)

        for index, line in enumerate(lines):
            if not line["comment"]:
                # now, remove multiple spaces in lines, replacing them with one.
                lines[index].latex = merge_multiple_spaces(line.latex)
            
                # convert things like testing to t_{esting}
                lines[index].latex = subscriptize(line.latex)

                # make the spaces escaped and 'permanant'
                lines[index].latex = make_spaces_permanant(line.latex)
        
        self.ast = lines