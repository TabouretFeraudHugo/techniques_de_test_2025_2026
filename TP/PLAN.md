# Description of the required tests for the API

Using the test library of python pytest, we will be conducting tests for the 4 parts of the workflow that the triangulation API interact with.

### 1) The PointSetID API call

For this part not much needed:
-One test to check for the well communication between the two services (which should trigger a 503 error), sending "good" and "bad" endpoints for the test.
-One test to verify that the format of the API answer (which should trigger a 400 error) sending "good" and "bad".
-One to check if the PointSetID does not exist (which should trigger a 404 error).

### 2) The calculus function

This is the big part, around 20 tests:
-We need a big bunch of tests with values and what is expected, to ensure the algorithm runs well (about 10 different values checks) (all should return the right value and a 200 response).
-Then, a bunch of tests to try to trick the algorithm, with values that won't have any results (they all should be triggering a 500 error).

### 3) The output of the API

In this part we only need one test:
-Test if a correct reponse from the triangle will be in the right format.

### 4) Perf tests

For the final part we will be testing the perf of the product, using our own benchmark (procedures for creating the benchmark will be detailed in the regarding file):
-Time performance tests: first we need a "benchmark" of other similar apps, getting their time to process similar data (will be done before the test, to get an best/average/worst value), then compare the time for our product to process the datas.
-Another performance test will be about the accuracy of the algorithm, again benchmarking other tools to compare to them.
