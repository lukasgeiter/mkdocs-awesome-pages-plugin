# Contribution Guidelines

Thank you for considering to contribute to this project. These guidelines will help you get going with development and outline the most important rules to follow when submitting pull requests for this project.

<br/>

## Development

#### Setup

##### Prerequisites

- [Python 3]
- [poetry]

##### Steps

1. Clone the (forked) repository
1. Install dependencies with `poetry install`

#### Running Tests

```bash
poetry run pytest
```

<br/>


## Submitting Changes

To get changes merged, create a pull request. Here are a few things to pay attention to when doing so: 

#### Commit Messages

The summary of a commit should be concise and worded in an imperative mood.  
...a *what* mood? This should clear things up: *[How to Write a Git Commit Message][git-commit-message]*

#### Code Style

This project uses [Black][black] for code formatting. 

#### Tests

If it makes sense, writing tests for your PRs is always appreciated and will help get them merged.

[Python 3]: https://www.python.org/
[poetry]: https://python-poetry.org/
[git-commit-message]: https://chris.beams.io/posts/git-commit/
[black]: https://black.readthedocs.io/
