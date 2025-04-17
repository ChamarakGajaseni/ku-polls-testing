[![Unit Tests](https://github.com/ChamarakGajaseni/ku-polls/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/ChamarakGajaseni/ku-polls/actions/workflows/python-app.yml)

## KU Polls: Online Survey Questions 

An application to conduct online polls and surveys based
on the [Django Tutorial project](https://docs.djangoproject.com/en/4.1/intro), with
additional features.

This app was created as part of the [Individual Software Process](
https://cpske.github.io/ISP) course at [Kasetsart University](https://www.ku.ac.th).

## Installation
Installation steps: [Installation](installation.md)

To be added. If the procedure is long, put it in the wiki or a separate file.

## Running the Application
Running: run this code in your terminal to run the webserver

```
python manage.py runserver
```

## Testing
The project includes comprehensive test coverage for all major functionality. To run the tests:

1. Run all tests with verbose output:
```bash
python manage.py test polls.tests --verbosity=2
```

2. Run specific test classes:
```bash
python manage.py test polls.tests.QuestionModelTests
```

3. Run specific test methods:
```bash
python manage.py test polls.tests.QuestionModelTests.test_can_vote_published_now
```

4. Run tests with coverage report:
```bash
coverage run -m pytest polls/tests.py
coverage report
```

The tests cover:
- Question visibility and access control
- Voting period management
- Question publication timing
- Index page functionality
- Detail view behavior

## Demo Users
| Username  | Password        |
|-----------|-----------------|
|   demo1   | hackme11 |
|   demo2   | hackme22 |
|   demo3   | hackme33 |

## Project Documents

All project documents are in the [Project Wiki](../../wiki/Home).

- [Vision and Scope](../../wiki/Vision%20and%20Scope)
- [Requirements](../../wiki/Requirements)
- [Project Plan](../../wiki/Project%20Plan)
- [Iteration 1 Plan](../../wiki/Iteration%201%20Plan) and [Task Board](https://github.com/users/ChamarakGajaseniH/projects/4/views/1)
- [Iteration 2 Plan](../../wiki/Iteration%202%20Plan) and [Task Board](https://github.com/users/ChamarakGajaseni/projects/4/views/12)
- [Iteration 3 Plan](../../wiki/Iteration%203%20Plan) and [Task Board](https://github.com/users/ChamarakGajaseni/projects/4/views/13)
- [Iteration 4 Plan](../../wiki/Iteration%204%20Plan) and [Task Board](https://github.com/users/ChamarakGajaseni/projects/4/views/14)
- [Domain Model](../../wiki/Domain%20Model)