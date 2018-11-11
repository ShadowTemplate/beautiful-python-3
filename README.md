# Beautiful Python 3

A collection of beautiful Python 3 pieces of code. 

This repository contains a wide range of algorithms, data structures, design 
patterns and other interesting or beautiful pieces of code. Its goal is both to 
test new language features and to keep track of reusable software components.

---
## Information

**Status**: `Occasionally developed`

**Type**: `Personal project`

**Development year(s)**: `2018+`

**Author(s)**: [ShadowTemplate](https://github.com/ShadowTemplate)

---
## Getting Started

Each script is usually associated to unit tests or a demo code. It should be
easy for the reader to dive into the project folders and run the scripts of 
interest.

### Prerequisites

Clone the repository and install the required Python dependencies:

```
$ git clone https://github.com/ShadowTemplate/beautiful-python-3.git
$ cd beautiful-python-3.git/
$ pip install --user -r requirements.txt
```

### Testing

To run a set of unit tests just locate and run the script, for example:

```
$ python3 algorithms/algorithms_test.py
```

Some scripts use [type hints](https://docs.python.org/3/library/typing.html).
You can statically check types of a script using 
[mypy](https://github.com/python/mypy), for example:

```
$ mypy design_patterns/behavioural/command_mixer.py 
```

If any error occurs the tool will log it.

---
## Building tools

* [Python 3.X](https://www.python.org/downloads/) - 
Programming language (X may vary according to the features used in each script)
* [mypy](https://github.com/python/mypy) - Static type check

---
## Contributing

Any contribution is welcome. Feel free to open issues or submit pull requests.

---
## License

This project is licensed under the GNU GPLv3 license.
Please refer to the [LICENSE.md](LICENSE.md) file for details.

---
*This README.md complies with [this project template](
https://github.com/ShadowTemplate/project-template). Feel free to adopt it
and reuse it.*
