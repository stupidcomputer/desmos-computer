# desmos-computer

available on [Gitea](https://git.beepboop.systems/stupidcomputer/desmos-computer) and [Github](https://github.com/stupidcomputer/desmos-computer)

## What is this?
- a client-server architecture for synchronizing a file containing Desmos expressions to a graph, (`cli/lib/server.py` and `cli/lib/clientside.py`)
- an instruction set architecture for Turing machines whose cells contain IEEE 754 compliant integers in each cell, (`cli/data/computer.py`)
- an assembler for that instruction set architecture, (not yet!)
- and other utilities. (disassembler, etc.)

## How does the ISA work?
The 'CPU', implemented in Desmos, takes in a list (aka an array, Turing tape, etc.) and starts execution at cell 1 (lists have 1-based indexes in Desmos).
The list also serves as the memory, as well. (Think like Befunge's `p` command.)

*Todo: disconnect opcode definitions and opcodes from the actual CPU implementation. Because of this, don't rely on this table! Check the implementation in `data/computer.desmos`.*

| Instruction mnemonic   | Behavior                                                                                                                         | First parameter         | Second parameter | Third parameter |
|-|-|-|-|-|
| `jmp`                  | Modify the instruction pointer and continue execution at the new location.                                                       | New instruction pointer | *n/a*            | *n/a*           |
| `add`                  | Take the values in addresses `a` and `b` and add them; store the result in address `c`.                                          | address `a`             | address `b`      | address `c`     |
| `sub`                  | See `add` instruction.                                                                                                           | *ld.*                   | *ld.*            | *ld.*           |
| `div`                  | See `add` instruction.                                                                                                           | *ld.*                   | *ld.*            | *ld.*           |
| `mul`                  | See `add` instruction.                                                                                                           | *ld.*                   | *ld.*            | *ld.*           |
| `cmp`                  | Compare the numbers in `a` and `b`. If `a` > `b`, set the greater than flag. Ditto for equals and less operators, as well. | address `a`             | address `b`      | *n/a*           |
| `rst`                  | Clear the equals, greater, and less than flags.                                                                                  | *n/a*                   | *n/a*            | *n/a*           |
| `eld`                  | Write the state of the equals flag to address `a`. If it's set, than `1` is written; `0` otherwise.                          | address `a`             | *n/a*            | *n/a*           |
| `gld`                  | Same as `eld`, but for the greater than flag.                                                                                    | *ld.*                   | *n/a*            | *n/a*           |
| `lld`                  | Same as `eld`, but for the less than flag.                                                                                       | *ld.*                   | *n/a*            | *n/a*           |
| `be`                   | Branch to address `a` if the equal flag is set.                                                                                  | address `a`             | *n/a*            | *n/a*           |
| `bne`                  | Same as `be`, but the !equal flag.                                                                                               | *ld.*                   | *n/a*            | *n/a*           |
| `bg`                   | Same as `be`, but the greater than flag.                                                                                         | *ld.*                   | *n/a*            | *n/a*           |
| `bl`                   | Same as `be`, but the less than flag.                                                                                            | *ld.*                   | *n/a*            | *n/a*           |
| `sto`                  | STOre the immediate value `v` into address `a`.                                                                                  | `v`                     | address `a`      | *n/a*           |
| `mov`                  | MOVe the value in the address `a` into address `b`.                                                                              | address `a`             | address `b`      | *n/a*           |

There are some other instructions, like `psto` and similar variants. They're experimental.

## Instruction design in general
Things we're optimizing for:

- *Pack as many things into one instruction as possible.* Execution of stuff in instructions is cheap, but each instruction execution is expensive.
- *No stacks.* Stacks require too much computation on the ISA side itself that isn't provided by the Desmos 'standard library' of instructions.

In general: *embed the intelligence into the machine code, **not** the CPU/ISA!*

## Things to do
- [x] Write a test suite for the various instruction of the ISA executing *in Desmos*
- [ ] Make the test suite reliable.
- [ ] Write an assembler to compile a custom Assembly language to native Desmos list format.
- [ ] Simplify all this into a command line tool.
- [x] Simplify the synchronization stack.
- [ ] Write documentation for all of this.

## Running tests

- Enter the nix-shell, then start a web browser.
- Navigate to `https://desmos.com/calculator`, and open the dev console
- Run `python3 -m cli sync -c` to copy the userscript to your clipboard
- Run the userscript in the console
- Run `main()` in the console
- Run `python3 -m unittest ./cli/tests/isa.py`, or other test groups if needed
- Keep the Desmos tab focused, as it may impede the ISA testing process

A note: the test suite might fail if you run it weirdly.
If it fails, run it again.
It might work, in which case you're good.

(This is cursed and I know it.)

## License

This project is licensed under the AGPLv3. See the `LICENSE` file for more information.
Copyright rndusr, randomuser, stupidcomputer 2024.
