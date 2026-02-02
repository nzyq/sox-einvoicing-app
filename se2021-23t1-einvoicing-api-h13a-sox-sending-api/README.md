# README.md

This is a repository for invoice sending. The repository contains the following:

- src directory which includes the source code for the project.
- tests directory which includes the test files for the project.
- .pylintrc which checks the linting of the project.
- .coverage which checks the coverage of the project.
- requirements.txt file which includes the dependencies required to run the project.

## Running the Server
To run the server locally, execute the following command in a terminal from the root directory of the repository:

```
python3 -m src.server
```

The server will start running on the port specified in the src/config.py file.

## Running Tests
To run tests, open two terminals. In the first terminal, start the server by executing:

```
python3 -m src.server
```

In the second terminal, run the command:

```
python3 -m pytest (specific test file)
```

## Checking Coverage
To check the coverage of the code, open two terminals. In the first terminal, run:

```
coverage run -m src.server
```

In the second terminal, run:

```
python3 -m pytest *specific test file*
```

After the tests have completed running, terminate the server in the first terminal by pressing control-C. Next, generate the coverage report in the second terminal by running:

```
coverage report
```

To generate a coverage report in HTML format, run:

```
coverage html
```

## Linting
To perform linting on the code, execute the following command from the root directory of the repository:

```
pylint *path-of-directory or file to lint*
```