# Usage Vacuum 

Usage Vacuum takes a Python script built to demo some functionality with print output, converts it to markdown.
The markdown contains the demo code interspersed with print output.

This works well with my process:
* As I develop functionality, I write tests, but I also write a demo usage script.
* The demo usage script looks like a walk through of what my new code does.
* So converting it into interesting markdown makes sense to me.

Essentially: input is a demo python script for functionality
output is markdown showing how the code produces output, created from the code itself.

Saves time if you are producing walkthrough markdown and have a script.

Another benefit is that you can test your demo usage script, then convert it to markdown when it works.
This prevents beautiful markdown with scripting in it which does not work or does not produce the advertised output.


## Future plans

List a roadmap or future plans for the repo work.

- [ ] 

## Important disclaimer

If any disclaimer exists, add it here.

## Getting Started

To get started with Usage Vacuum, prepare a Python script that demonstrates the functionality you want to showcase. This script should include print statements to display outputs as you walk through your code. Once your demo script is ready and working as intended, you can use Usage Vacuum to convert it into a markdown file, where the code and its outputs are interleaved for easy sharing and documentation.

## Prerequisites

- Python 3.7 or newer must be installed on your system.
- Ensure you have `pip` (Python package manager) available.
- It is recommended to use a virtual environment (such as `venv` or `virtualenv`) to manage dependencies.
- Your demo script should be a standalone Python file that runs without errors.

## Installing

1. Clone this repository:
   ```sh
   git clone https://github.com/ErikPohl444/usage_vacuum.git
   cd usage_vacuum
   ```
2. (Recommended) Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
   If a `requirements.txt` is not yet provided, install any needed libraries as you encounter ImportErrors, or create one with your environment’s current packages using `pip freeze > requirements.txt`.

## Running the tests

Provide instructions on running the tests here.

## Technologies used

List the technologies used here.

e.g.
* Written in Chicken 2.0

## Minimum system requirements

List the minimum system requirements for the application to run.

e.g.
* Must be run on VALIS.

## Contributing

I invite contributions.  See the [Contribution Guidelines](CONTRIBUTING.md) for any guidelines.

## Authors

See the [Authors doc.](AUTHORS.md)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

* Thanks to everyone who has motivated me to learn more.
* These folks were key to this particular effort: [ACKNOWLEDGEMENTS](ACKNOWLEDGEMENTS.md)
