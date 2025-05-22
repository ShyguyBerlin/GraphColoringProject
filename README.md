# GraphColoringProject
A project where we try to visualize/ work on some graph coloring algorithms

## How to run

To run the webinterface, you have to set up a Webserver to host the webpage contained in this repository. There are many ways to achieve this. For example, if editing in visual studio code, you can use a live server extension. Also the page is available at our [github page](https://shyguyberlin.github.io/GraphColoringProject/).<br>
To run local tests you can use the cli_tests.py script (It contains a solver which is seperated from the webpage, but no real CLI capabilities like arguments or test input).

## About Tests (to be implemented, these are requirements/propositions)
Besides visualizing all the algorithms, it also makes sense to compare them in a few different factors, these include:
- Runtime
- Quality
    - (average/median/min/max Coloring Number)
    - When generating the Graph with a specific upper bound for the optimal Coloring Color, you can also output a ratio to this number

This data should be sampled over large datasets, which need to be formated in a specific way. I propose a CLI which may take a datafile or a test definition file and some formating info as parameters and then print a summary for the tests it runs on the given graphs. This should include all available solvers by default and may include a standard timeout, so inefficient solvers don't block the pipeline.

Example Test definition file, which includes all parameters which the user should also be able to enter manually (thus overwriting the definition file):
```json
// Test definition file
{
    "name": "Test1",
    "timeout": "1500", // miliseconds
    // "solvers": ["greedy_min","greedy_max"]
    "datasets":
    [
        {
            "format": "edge-list",
            "file": "tests/SmallGraphs.txt"
        },
        {
            "format": "adjacency-matrix",
            "file": "tests/LargeGraphs.txt",
        }
        {
            "format": "planar-code",
            "file": "tests/SmallPlanarGraphs.txt"
        }
    ]
}
```