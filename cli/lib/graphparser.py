from dataclasses import dataclass
from typing import Callable, ClassVar, Self, Any, IO, List, Dict
from json import loads

reserved_keywords = "sin cos tan csc sec cot mean median min max quertile quantile stdev stdevp var mad cov covp corr spearman stats count total join sort shuffle unique for histogram dotplot boxplot normaldist tdist poissondist binomialdist uniformdist pdf cdf inversecdf random ttest tscore ittest frac sinh cosh tanh csch sech coth polygon distance midpoint rgb hsv lcm gcd mod ceil floor round sign nPr nCr log with cdot to in length left right operatorname"
reserved_keywords = reserved_keywords.split(' ')

def continue_lines(string: str) -> str:
    # if there's a '\' and then a newline, ignore the newline.
    return string.replace('\\\n', '')

def replace_multiplication(string: str) -> str:
    return string.replace('*', '\\cdot ')

def replace_actions(string: str) -> str:
    return string.replace(' ->', '\\to ').replace('->', '\\to ')

def replace_tabs(string: str) -> str:
    return string.replace('\t', '    ')

def merge_multiple_spaces(string: str) -> str:
    return ' '.join(string.split())

def curly_brackets(string: str) -> str:
    return string.replace('{', '\\left\\{').replace('}', '\\right\\}')

def parens(string: str) -> str:
    return string.replace('(', '\\left(').replace(')', '\\right)')

def for_fix(string: str) -> str:
    return string \
        .replace('for\\ ', "\\operatorname{for}") \
        .replace('for', "\\operatorname{for}")    \
        .replace('length\\ ', "\\operatorname{length}") \
        .replace('length', "\\operatorname{length}")

def make_spaces_permanant(string: str) -> str:
    return string.replace(' ', '\ ')

def change_square_brackets(string: str) -> str:
    return string.replace('[', '\\left[').replace(']', '\\right]')

def subscriptize(string: str) -> str:
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

@dataclass
class DesmosGraphOverride:
    """
    Container for Desmos Overrides.

    This is the method by which machine code compiled by assembler or otherwise, is inserted.

    It's sort of like a fancy substitution macro system thing. It's still prone to stupidity.
    """

    # XXX: If you use the Dict[str, str] type annotation, dataclass throws an error:
    # ValueError: mutable default <class 'dict'> for field payload is not allowed: use default_factory
    # Ask a question about this
    payload: Any = None

    @classmethod
    def from_file(cls, filename: str) -> Self:
        """
        Read a Override from the filename filename.
        """
        fd = open(filename, "r")

        return cls.from_file_object(fd)

    @classmethod
    def from_file_object(cls, io_obj: IO) -> Self:
        """
        Read a Override from fileobj fileobj.
        """
        text = io_obj.read()

        return cls.from_text(text)

    @classmethod
    def from_text(cls, text: str) -> Self:
        return cls(loads(text))

@dataclass
class DesmosGraphStatement:
    """
    This class contains one Desmos graph statement -- that is, one line in the editor.

    You probably shouldn't create this class manually; it's used in .DesmosGraph.
    """
    commands: str
    latex: str

    def __getitem__(self, item) -> str:
        try:
            return self.commands[item]
        except KeyError:
            return None

    def __repr__(self) -> str:
        return "{} : {}".format(str(self.commands), self.latex)

    @classmethod
    def from_line(cls, line) -> Self:
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
    def from_lines(cls, lines) -> List[str]:
        output = []
        for line in lines:
            output.append(cls.from_line(line))

        return list(
            filter(
                lambda item: item is not None,
                output
            )
        )

@dataclass
class DesmosGraph:
    """
    This class represents a Desmos Graph. That is, the thing that you interact with when you use Desmos. That thing.

    You want to create one through a series of Desmos statements. This is a cobbled together DSL that uses .replace and .split regularly. Beware!
    """

    text_preprocessors: ClassVar[List[Callable[[str], str]]] = [
        continue_lines,
        replace_multiplication,
        replace_actions,
        replace_tabs
    ]
    line_preprocessors: ClassVar[List[Any]] = [
        DesmosGraphStatement.from_lines
    ]
    latex_preprocessors: ClassVar[List[Callable[[str], str]]] = [
        merge_multiple_spaces,
        curly_brackets,
        parens,
        subscriptize,
        change_square_brackets,
        for_fix,
        make_spaces_permanant
    ]

    text: str

    def __post_init__(self):
        self.ast: List[DesmosGraphStatement] = []
        self._parse()

    def _parse(self) -> None:
        text: str = self.text
        for preprocessor in self.text_preprocessors:
            text = preprocessor(text)

        lines = text.split('\n')
        for preprocessor in self.line_preprocessors:
            lines = preprocessor(lines)

        for index, line in enumerate(lines):
            if not line["comment"]:
                for preprocessor in self.latex_preprocessors:
                    lines[index].latex = preprocessor(line.latex)

        self.ast = lines

    def to_file(self, filename: str) -> None:
        """
        Write the Graph to the filename filename.
        """
        fd = open(filename, "w")
        self.to_fileobj(fd)

    def to_fileobj(self, io_obj: IO) -> None:
        """
        Write the Graph to the fileobj fileobj.
        """
        io_obj.write(self.text)

    @classmethod
    def from_file(cls, filename: str) -> Self:
        """
        Read a Graph from the filename filename.
        """
        fd = open(filename, "r")

        return cls.from_file_object(fd)

    @classmethod
    def from_file_object(cls, io_obj: IO) -> Self:
        """
        Read a Graph from fileobj fileobj.
        """
        text = io_obj.read()

        return cls(text)

    def include_override(self, override: DesmosGraphOverride) -> None:
        """
        Overrides are the way to include changes in a Desmos Graph. This is changes in the instructions and stuff.

        If you're writing an assembler, you can use an override for computer.desmos to include the compiled machine code.
        """
        # XXX: This is O(n^2). Or somewhat inefficient. Not a computer science major.
        for key in override.payload.keys():
            for statement in self.ast:
                try:
                    if statement.commands["id"] == key:
                        statement.latex = override.payload[key]
                except KeyError:
                    pass
