# bbref

Looks up Blood Bowl rules quickly from the command line.

## Usage

`bbref` can search skills, inducements, star players and team rosters for rules
to display.

Invoke with a searchterm:

~~~
$ bbref hail

Hail Mary Pass (Passing)
------------------------
The player may throw the ball to any square on the playing pitch, no
matter what the range: the range ruler is not used. Roll a D6. On a
roll of 1 the player fumbles the throw, and the ball will bounce once
from the thrower’s square. On a roll of 2-6, the player may make the
pass. The Hail Mary pass may not be intercepted, but it is never
accurate – the ball automatically misses and scatters three squares.
Note that if you are lucky, the ball will scatter back into the target
square! This skill may not be used in a Blizzard or with the Throw
Team-Mate skill.
~~~

or tell it to limit the search to skills/inducements, rosters or star players only:

~~~
$ bbref -r dark

   Race        #       Position     MV   ST   AG   AV   Cost       Skills        Norm    Dbles
==============================================================================================
Chaos Pact    0-1    Dark Elf       6    3    4    8    70k    Animosity         GAM     PS
                     Renegade
Dark Elf      0-16   Linemen        6    3    4    8    70k    None              GA      SP
Dark Elf      0-2    Runners        7    3    4    7    80k    Dump-Off          GAP     S
...
~~~

`bbref --help`

will show the following:

~~~
Usage: bbref [OPTIONS] SEARCHTERM

  Quickly checks a Blood Bowl rule. Searches all rule types by default.

Options:
  -s, --skill       Search skills and inducements
  -r, --roster      Search rosters
  -p, --star        Search star players
  -d, --deepsearch  Include rules text in search
  --help            Show this message and exit.
~~~

## Installation

`python setup.py install`

is all that's required.

