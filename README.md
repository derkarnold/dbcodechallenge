# DB code challenge

Implements a simple text analyser that runs as a web service.

For a given JSON request of the format:
```json
{
    "text": "hello 2 times  "
}
```
It will return a response of the format:
```json
{
    "textLength": {
        "withSpaces": 15,
        "withoutSpaces": 11
    },
    "wordCount": 3,
    "characterCount": [
        {"e": 2}, {"h": 1}, {"i": 1}, {"l": 2},
        {"m": 1}, {"o": 1}, {"s": 1}, {"t": 1}
    ]
}
```

The core code is in analyser.py, with unit tests to be found in test_analyser.py.
These unit tests are run automatically via a GitHub workflow when the main branch is pushed to GitHub.

Provided the tests pass, Heroku pulls the latest changes and deploys them automatically.
