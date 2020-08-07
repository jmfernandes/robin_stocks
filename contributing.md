# Contributing

Anyone and everyone is encouraged to contribute to this project. The most helpful changes are pull requests that fix one of the open issues in the Issues tab.
Adding functionality that is available on the app/website but not through this interface is also very helpful. Grammar changes and changes to business logic
that do not have a noticable effect on performance are generally not accepted.

## Pull Request Process

1. Make sure that if you make any grammar or documentation changes, that they are in a seperate commit from
   any code changes.
2. Make sure you update __init__.py to import new functions that are created.
3. Make sure to update the version number in setup.py. The version number is in the format XX.YY.ZZ, where the
   XX is only changed when there is a fundamental and major change, YY is changed for features added, and ZZ is changed
   for bug fixes. When updating a number, all the numbers to the right get changed to zero. i.e. 1.23.50 => 1.24.0. Numbers
   are also allowed to go as high as you want, so 1.65289.0 is a valid version number.
4. Write tests to cover the functionality of code you added.
5. After submitting a pull request, please be on the lookout for any messages from me about things that need to be fixed before I merge the branch.

## Testing

Make sure to install pytest and pytest-dotenv from PyPi and run every test in test_github_actions.py. Add new tests to cover the changes you have made, but not if you need to test placing orders. Currently there is no way to submit fake orders, so any tests for orders would submit a real order.

## Code of Conduct

### Our Pledge

In the interest of fostering an open and welcoming environment, we as
contributors and maintainers pledge to making participation in our project and
our community a harassment-free experience for everyone, regardless of age, body
size, disability, ethnicity, gender identity and expression, level of experience,
nationality, personal appearance, race, religion, or sexual identity and
orientation.

### Our Standards

Examples of behavior that contributes to creating a positive environment
include:

* Using welcoming and inclusive language
* Being respectful of differing viewpoints and experiences
* Gracefully accepting constructive criticism
* Focusing on what is best for the community
* Showing empathy towards other community members

Examples of unacceptable behavior by participants include:

* The use of sexualized language or imagery and unwelcome sexual attention or
advances
* Trolling, insulting/derogatory comments, and personal or political attacks
* Public or private harassment
* Publishing others' private information, such as a physical or electronic
  address, without explicit permission
* Other conduct which could reasonably be considered inappropriate in a
  professional setting

### Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable
behavior and are expected to take appropriate and fair corrective action in
response to any instances of unacceptable behavior.

Project maintainers have the right and responsibility to remove, edit, or
reject comments, commits, code, wiki edits, issues, and other contributions
that are not aligned to this Code of Conduct, or to ban temporarily or
permanently any contributor for other behaviors that they deem inappropriate,
threatening, offensive, or harmful.

### Scope

This Code of Conduct applies both within project spaces and in public spaces
when an individual is representing the project or its community. Examples of
representing a project or community include using an official project e-mail
address, posting via an official social media account, or acting as an appointed
representative at an online or offline event. Representation of a project may be
further defined and clarified by project maintainers.
