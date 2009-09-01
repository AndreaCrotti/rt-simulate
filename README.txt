                            *RT SIMULATE*
                            =============

Author: andrea crotti <andrea.crotti.0@gmail.com>
Date: 2009-09-01 12:07:08 CEST


Table of Contents
=================
1 implement the worst case response time algorithm 
2 write the graphical interface with wxWidget 
3 test deeply all the possible error conditions 
4 General concepts 
5 GUI 
    5.1 FIG format 
    5.2 Matplotlib 
    5.3 wxPython 
        5.3.1 Functions 
        5.3.2 Implementation 
        5.3.3 Hints 
        5.3.4 Debugging 
6 Languages used 
7 Frameworks 
8 Language table 
9 Theory summary 
    9.1 STATIC scheduling algorithm 
    9.2 Fixed priority scheduling 
    9.3 Dynamic priority scheduling algorithms: 
        9.3.1 Deadline monotonic 
        9.3.2 Rate monotonic 
    9.4 Analysis 


1 DONE implement the worst case response time algorithm 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  CLOSED: [2009-08-31 Mon 09:31]
  - CLOSING NOTE [2009-08-31 Mon 09:31] 
    Algorithm working on simple cases

2 TODO write the graphical interface with wxWidget 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

3 TODO test deeply all the possible error conditions 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


4 General concepts 
~~~~~~~~~~~~~~~~~~~

This program will show interactively how some real time algorithms work.
It works as:
1. task a set of tasks as input
2. choose a scheduling algorithm
3. check if is schedulable or not
4. return the scheduled hyperperiod if possible

Tasks are taken from the command line or from a configuration file.

In plus there will be an interactive modality (cli or GUI) where those operations should be possible:
- add a new task
- remove a task
- see the timeline

[This] is the official site, more information on laboratories [here].

Using a MVC pattern to design the application, which must be easily adapt to new algorithms and data types.


[This]: http://dit.unitn.it/~abeni/RTOS/index.html
[here]: http://dit.unitn.it/~abeni/RTOS/lab.html

5 GUI 
~~~~~~
  

5.1 FIG format 
===============

5.2 Matplotlib 
===============
   [matplotlib tutorial]


   [matplotlib tutorial]: http://matplotlib.sourceforge.net/users/artists.html

5.3 wxPython 
=============

5.3.1 Functions 
----------------
    One simple menubar where you can:
    - load a configuration file
    - run the scheduling
    - check if everything is working
    - add a new task to the current task set (this enable automatic redrawing)
      
    The main window must contain the hyperperiod scheduling, made of blocks of different colors and lines for the deadlines.

5.3.2 Implementation 
---------------------
      
    We'll use a *wxSizer* object, allows to place objects which will be automatically resized or replaced.
    Important to remember that sizer != parent object.
    
    After the layout is ready (box/grid or other) we set up everything with:
    1. window.SetSizer(sizer)
    2. window.SetAutoLayout(true)
    3. sizer.Fit(window)

5.3.3 Hints 
------------

    When taking input from user *wxValidator* is needed to check if the input is correct
    (Note: Your wxValidator sub-class must implement the wxValidator.Clone() method.)

5.3.4 Debugging 
----------------
    A nice way to debug is using pycrust

6 Languages used 
~~~~~~~~~~~~~~~~~
  - python (for the gui and control interface)
  - C/pyrex extension (for the algorithm engine)

7 Frameworks 
~~~~~~~~~~~~~
  - wxgtk/gtk/dialog?
  - [How to learn wxpython]
    

  [How to learn wxpython]: http://wiki.wxpython.org/How%20to%20Learn%20wxPython

8 Language table 
~~~~~~~~~~~~~~~~~

    Task         Schedulable entity            
    Preemptive   OS can regain control of cpu  
    WCET         Worst Case Execution Time     

9 Theory summary 
~~~~~~~~~~~~~~~~~
  OS kernel creates the illusion of multiple CPUs, concurrency is implemented by multiplexing tasks.
  Tasks are associated to temporal constraints (*deadlines*)
  
  Scheduler is responsible for selecting the tasks to execute.
  
Algorithms:

9.1 STATIC scheduling algorithm 
================================
   - Time axis divided in time slots
   - Slots statically allocated to the tasks
   - $\tau$ = *gcd*, $T$ = *lcm*
   - Very simple implementation, no operating system needed

     *NOT VERY CLEAR HOW TO IMPLEMENT THIS, only frequencies and timings in the slides.*
     What's the deadline in this case?
     In general enough to fire a timer every *minor cycle*.

9.2 Fixed priority scheduling 
==============================
   Very simple /preemptive/ scheduling algorithm.
   - every task has a fixed priority p_i
   - active task with highest priority are scheduled

     To have a better response of the system the priority must be chosen dynamically.
     So the problem becomes, how to assign priorities to manage to have a schedulable set of tasks?

9.3 Dynamic priority scheduling algorithms: 
============================================
   Given a set, how to assign priorities?
   Two possible objectives:
   - schedulability
   - response time
      
   - Given a set of tasks where all periods are equal to deadlines and offsets equal to 0.
      ($\forall i, D_i = T_i
     \forall i, r_i0 = 0$)
     [rate monotonic] is the best choice

   - Given a set of tasks where all periods are different from deadlines
     [deadline monotonic] is the best choice
     
     If we consider periodic tasks with offsets, then /there is no optimal priority assignment possible/


     [rate monotonic]: sec-9.3.2
     [deadline monotonic]: sec-9.3.1

9.3.1 Deadline monotonic 
-------------------------
    Shorter period $\rightarrow$ higher priority.

9.3.2 Rate monotonic 
---------------------
    Shorter relative deadline $\rightarrow$ higher priority.

9.4 Analysis 
=============
   Given a set of tasks, how can we make sure that is possible to schedule them?
   
   1. simulate the system to check if deadlines missed:
      /hyperperiod/ ($H = lcm\{Ti\}$)
      *The number can be very large*

   2. *Utilisation analysis for RM*:
      
      Based on the utilisation bound, only works for deadline monotonic case (deadline = period)

      Each task uses the processor:
      $Ui = Ci/Ti$
      
      Total processor utilisation is:
      $U = \sum_i Ci/Ti$
      
      So we get:
      $U > 1 \rightarrow$ not schedulable
      $U < Ulub \rightarrow$ schedulable
      $U < 1 \rightarrow$ don't know, other checks needed

      $Ulub = 1$ would be optimal

   3. *Utilisation analysis for DM*:
      In this case we consider
      $U' = \sum_i Ci/Di$
      $\tau = (C,D,D)$ is the worst possible case of $\tau = (C,D,T)$
      So if one is satisfied the other is also satisfied
      
      This bound is very pessimistic.

   4. *Response time analysis*:
      Compute the /worst case response time/ for every task.
      Valid for an arbitrary assignment.
      Assumes periodic tasks with no offsets.
      
      *Critical instant*: job $Ji,j$ is released at the same time with a job in every high priority task
      
