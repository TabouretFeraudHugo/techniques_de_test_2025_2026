# Description of the required tests for the API

### 1) Writting the test first

As the project started with the writting of tests, it was actually really hard to think forward into what will be problematic, considering i didn't even know which algorithm i would implement. So of course i did thought of the basic status checks (200,400,...) but i overshot with the perf tests..

### 2) Making the actual algortihm

What i did was : writting my test -> make the algorithm -> check if it passed the tests.
Spoiler, none passed...
So i used a dummy Delaunay version where i was sure that was working, then verified that my tests were actually working.
Then made my own version (it's not delaunay at all, it's ear clipping, because i was clueless about triangulation at the start and it seemed, after reseaches, that it was easier to implement).

### 3) Improving the tests

I was bothered with the fact that my tests were just the same functions with only one parameter changing.
So what i did was make a function that can use a parametrize with my parameters, and thus, i can have only one function, and greatly increase the "readability" of the code. 

### 4) Perf tests

So, at the begining i thought of making a benchmark with others triangulation tools on internet, gathering datas like time to complete, memory usage, accuracy. Then i realized i had no access to these datas, and i needed to actually measure them (which would be very innacurate without a precise protocol).
After some research i acknoledged that there are actually some common polygon types that i can use to check for the accuracy of the algortihm.
In the end i couldn't come up with a solution for the speed performance, or the benchmark (which would have been nice).

### 5) Possible improvements 

I think i would have done better if :
- I would have start with the algorithm instead of the test
- Made a bit more research before, to know a bit better what i'm doing