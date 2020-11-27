# Contributing guidelines

## Pull Request Checklist

Before sending your pull requests, make sure you followed this list.

- Read [contributing guidelines](CONTRIBUTING.md).
- Read [Code of Conduct](CODE_OF_CONDUCT.md).
- Document your functions directly in the code with the Sphinx framework.
- Ensure you have the copyrights for your contribution and you are allowed to submit your code.

## How to become a contributor and submit your own code

### Contributing code

If you have improvements to aio, send us your pull requests!
Contributions can be anything from fixing typos, suggesting new functions, writing tests, etc.
For those just getting started, Github has a
[how to](https://help.github.com/articles/using-pull-requests/).

aioneers team members will be assigned to review your pull requests. Once the
pull requests are approved and pass continuous integration checks, an aioneers
team member will apply `ready to pull` label to your change. This means we are
working on getting your pull request submitted to our internal repository. After
the change has been submitted internally, your pull request will be merged
automatically on GitHub.

If you want to contribute, start working through the aio codebase,
navigate to the [Github "issues" tab](https://github.com/aioneers/aio/issues) and start
looking through interesting issues. If you
decide to start on an issue, leave a comment so that other people know that
you're working on it. If you want to help out, but not alone, use the issue
comment thread to coordinate.

### Contribution guidelines and standards

Before sending your pull request for
[review](https://github.com/aioneers/aio/pulls),
make sure your changes are consistent with the guidelines.

All functions need to be imported in the "./aio/\***\*init\*\***.py" file with a statement like

```bash
from .<your_module> import <your_function>
```

where "<your_module>" needs to be replaced by the name of the module and "<your_function>" by the name the function.

#### General guidelines and philosophy for contribution

- Include pytests when you contribute new features, as they help to a)
  prove that your code works correctly, and b) guard against future breaking
  changes to lower the maintenance cost.
- Bug fixes also generally require pytests, because the presence of bugs
  usually indicates insufficient test coverage.
- When you contribute a new feature to aio, the maintenance burden is
(by default) transferred to the aioneers team. This means that the benefit
of the contribution must be compared against the cost of maintaining the
feature.
<!-- - Full new features typically will live in
  [aio/addons](https://github.com/aioneers/addons) to get some
  airtime before a decision is made regarding whether they are to be migrated
  to the core. -->
- As every PR requires some CI testing, we discourage
  submitting PRs to fix one typo, one warning, etc. We recommend fixing the
  same issue at the file level at least (e.g.: fix all typos in a file, fix
  all compiler warning in a file, etc.)

#### License

Include a license at the top of new files.

[License](LICENSE)

#### Running pytests

We encourage all contributors to write tests for their functions with pytest. Please make sure that the tests do not rely on local data nor should the data be included in the repository.

In the folder "tests", all tests for one module should be included in one file with the same name as the module, prefixed with "test\_".

The names of the test functions should be as expressive as possible.

We recommended to assess the correctness of the output of the function with an "assert" statement.

### Documenting your code

We kindly ask contributors to document their code with the [Sphinx framework](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#inline-markup). Just make sure the documentation is included in the right format and we will take care that it gets published.

The documentation should be put directly in the function like this.

```bash
"""
A general description of the function.

Parameters
----------
first_input_parameter : Object type of the parameter (e.g. str)
    Describe what this parameter does and what the expected inputs are.

second_input_parameter : int
    Describe what this parameter does and what the expected inputs are.

Returns
-------
return object : Object type of the return (e.g. int)
    Describe what the return is and how it can be used..

Examples
--------
>>> import aio
>>> result = aio.your_function(first_input_parameter,second_input_parameter)
>>> result
"""
```

Additionally the reference files which create the table of contents and include the functions in the documentation need to be edited:

Add new functions in this file: ./aio/doc/source/reference/index.rst in the ".. toctree::" list.
Every module needs to have a rst file, named like the module, in the folder ./aio/doc/source/reference/.
This file should have the form like

```bash
==========================================
AIO Documentation
==========================================

.. currentmodule:: aio

List of Functions
~~~~~~~~~~~~~~~~~
.. autosummary::
   <your_function>

Definition of Functions
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: <your_function>
```

where "<your_function>" needs to be replaced by the name of the module.

#### Python coding style

“One of [Guido van Rossum](https://gvanrossum.github.io)'s key insights is that code is read much more often than it is written.” It is our intention to develop artefacts in a readable & robust manner, so others can find, use, read, understand, improve, reuse and build on our developments.

Changes to AIO Python code should conform to the following principles:

Please follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) and [PEP 257](https://www.python.org/dev/peps/pep-0257/) style guide whenever possible.

Use `pylint` to check your Python changes. To install `pylint` and check a file
with `pylint` against the `black` style definition:

```bash
$ pip install pylint
$ pip install black
```

To enable the Black formatter, go into File > User Preferences > Settings, and put the following setting in your User Settings (for settings for all workspaces) or Workspace settings (for the current workspace/folder).

```bash
"python.formatting.provider": "black"
```
