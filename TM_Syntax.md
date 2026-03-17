
# Turing Machine Simulator Language Specification


## 1. Overview

The simulator operates on a Turing machine object that encapsulates its rules, states, and alphabets, and provides methods to execute and display a computation. To simplify program creation, a parser constructs this object from a textual description written in the syntax defined below.

## 2. Grammar

A machine description file consists of a sequence of **stanzas**. Each stanza begins with a **header line** that starts in the first column. The first word of the header line is a **keyword** identifying the type of stanza.

A stanza may be followed by one or more **continuation lines**, each of which must be indented. These continuation lines provide additional data associated with the stanza.

<pre>
  M -> (Stanza)(\n Stanza)*
  Stanza -> StartStanza | TapesStanza | AcceptStanza | RejectStanza | StateStanza
  StartStanza -> "start:" Ident
  TapesStanza -> "tapes:" number
  AcceptStanza -> "accept:" Ident (\n\t Ident)*
  RejectStanza -> "reject:" Ident (\n\t Ident)*
  StateStanza -> "state:" Ident (\n\t StateTransition)+
  StateTransition -> (Symbol|Special){k} (Symbol|Special){k} Action{k} Ident
  Symbol -> tape symbols are alphanumeric or punctuation ! $ % &amp; ( ) * + , - . or /
  Special -> the : and _
  Action -> the characters l, r and n or uppercase L, R and N.
  Ident -> a nonempty string of alphanumerics
</pre>


## 3. Comments and Lexical Notes

The `#` character introduces a comment. A comment extends from the `#` to the end of the line and is ignored by the parser.

Because `#` is reserved for comments, it cannot be used as a tape symbol. If a program (for example, from a textbook) requires the `#` symbol, it must be replaced with an alternative character. Any permitted punctuation symbol may be used; a common convention is to use the ampersand (`&`) as a substitute.

## 4. Required Stanzas and Ordering

A valid machine description must contain exactly one:

* `start` stanza
* `accept` stanza
* `reject` stanza

The `tapes:` stanza must appear before any `state:` stanza.

## 5. Tape and Symbols

The underscore character (`_`) denotes the blank symbol. It is the default value of all uninitialized tape cells.

The blank symbol may be used when specifying the initial contents of the tape; it is normalized by the parser to the underscore character (`_`).

## 6. States and Identifiers

An **Ident** is the name (label) of a state. Identifiers consist of one or more alphanumeric characters.

A **state stanza** defines a state and its transitions. The header line specifies the state name, and the body consists of one or more **transition lines**, each defining a single transition.

## 7. Transition Syntax

### 7.1 Single-Tape

```
read-symbol write-symbol action new-state
```

### 7.2 Multi-Tape (k tapes)

```
read₁ ... readₖ write₁ ... writeₖ action₁ ... actionₖ new-state
```

Each transition line consists of:

* *k* symbols read from the tapes
* *k* symbols to write to the tapes
* *k* actions (one per tape)
* the next state identifier

All components appear on a single line, separated by whitespace.

## 8. Symbols and Special Characters

### 8.1 Symbols

A **symbol** is any single character from the following set:

* Alphanumeric: `A–Z`, `a–z`, `0–9`
* Punctuation: `! $ % & ( ) * + , - . /`

### 8.2 Special Symbols

The following **special symbols** are permitted:

* `:` — wildcard
* `_` — blank symbol

## 9. Actions

An **action** specifies tape head movement:

* `l` — move left
* `r` — move right
* `n` — no movement

Uppercase variants (`L`, `R`, `N`) have the same effect on the tape head, and additionally cause the simulator to print the machine configuration immediately after performing the transition.

## 10. Accept and Reject States

The `accept` and `reject` stanzas may specify one or more state identifiers:

* The first identifier appears on the header line
* Additional identifiers appear on indented continuation lines

## 11. Wildcard (`:`) Semantics

The colon (`:`) acts as a **wildcard**.

### 11.1 Wildcards in Read Positions

When used in the read symbols of a transition, `:` matches **any symbol** on the corresponding tape.

#### Priority Rules

Transitions are selected in order of **specificity** (most specific to least specific):

1. **No wildcards** — exact match required
2. **One wildcard** — matches if no exact match exists
3. **k−1 wildcards** — matches if exactly one symbol is concrete
4. **All wildcards** — default match, lowest precedence

Within the same specificity level, transitions are evaluated **right to left** (later lines override earlier ones).

### 11.2 Wildcards in Write Positions

When `:` appears as a write symbol, it **copies the corresponding read symbol** to the tape. This allows transitions to preserve tape contents without explicitly naming symbols.

### 11.3 Missing Transitions

If no transition matches the current configuration, the machine halts in the **reject** condition.

(Last update: 17 March 2026)


