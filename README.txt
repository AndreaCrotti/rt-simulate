                            *RT SIMULATE*
                            =============

Author: andrea crotti <andrea.crotti.0@gmail.com>
Date: 2009-09-08 18:55:04 CEST


Table of Contents
=================
1 implement the worst case response time algorithm 
2 write an automatic generator + tester or random task sets 
3 Description and usage 
4 GUI 
    4.1 FIG format
    4.2 SVGfig 
        4.2.1 Doc 
    4.3 wxPython
5 Languages used 
6 Language table 
7 Theory summary 
8 Algorithms 
    8.1 STATIC scheduling algorithm 
    8.2 Fixed priority scheduling 
    8.3 Dynamic priority scheduling algorithms: 
        8.3.1 Deadline monotonic 
        8.3.2 Rate monotonic 
    8.4 Analysis 


1 DONE implement the worst case response time algorithm 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  CLOSED: [2009-08-31 Mon 09:31]
  - CLOSING NOTE [2009-08-31 Mon 09:31] 
    Algorithm working on simple cases

2 TODO write an automatic generator + tester or random task sets 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

3 Description and usage 
~~~~~~~~~~~~~~~~~~~~~~~~

This program will show interactively how some real time algorithms work.
In general it:
1. takes a set of tasks as input
2. chooses a scheduling algorithm
3. check if is schedulable or not
4. return the scheduled hyperperiod if possible

Tasks are taken from a configuration file.

In plus there will is an interactive modality where those operations should be possible:
- add a new task
- remove a task
- see the timeline

To start it simply ./rt_simulate.py -i

[This] is the official site, more information on laboratories [here].


[This]: http://dit.unitn.it/~abeni/RTOS/index.html
[here]: http://dit.unitn.it/~abeni/RTOS/lab.html

4 GUI 
~~~~~~
  

4.1 FIG format :ARCHIVE:
========================

4.2 SVGfig 
===========
   

4.2.1 Doc 
----------
    [svgfig tutorial], one big library composed of only one file.
    Possibility to export in different formats
    Some nice links:
    - [wikipedia SVG page]
    - [learning by coding]
    - [table of colors available]: color are the same used in the CSS style


    [svgfig tutorial]: http://code.google.com/p/svgfig/wiki/Introduction
    [wikipedia SVG page]: http://en.wikipedia.org/wiki/Scalable_Vector_Graphics
    [learning by coding]: http://www.datenverdrahten.de/svglbc/
    [table of colors available]: http://www.december.com/html/spec/colorspottable.html

4.3 wxPython :ARCHIVE:
======================


5 Languages used 
~~~~~~~~~~~~~~~~~
  - python (for the gui and control interface)
    

6 Language table 
~~~~~~~~~~~~~~~~~
  ACRONYM      EXPLANATION                   
 ------------+------------------------------
  Task         Schedulable entity            
  Preemptive   OS can regain control of cpu  
  WCET         Worst Case Execution Time     

7 Theory summary 
~~~~~~~~~~~~~~~~~
  OS kernel creates the illusion of multiple CPUs, concurrency is implemented by multiplexing tasks.
  Tasks are associated to temporal constraints (*deadlines*)
  
  Scheduler is responsible for selecting the tasks to execute.

8 Algorithms 
~~~~~~~~~~~~~

8.1 STATIC scheduling algorithm 
================================
   - Time axis divided in time slots
   - Slots statically allocated to the tasks
   - $\tau$ = *gcd*, $T$ = *lcm*
   - Very simple implementation, no operating system needed

8.2 Fixed priority scheduling 
==============================
   Very simple /preemptive/ scheduling algorithm.
   - every task has a fixed priority p_i
   - active task with highest priority are scheduled

     To have a better response of the system the priority must be chosen dynamically.
     So the problem becomes, how to assign priorities to manage to have a schedulable set of tasks?

8.3 Dynamic priority scheduling algorithms: 
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


     [rate monotonic]: sec-8.3.2
     [deadline monotonic]: sec-8.3.1

8.3.1 Deadline monotonic 
-------------------------
    Shorter period $\rightarrow$ higher priority.

8.3.2 Rate monotonic 
---------------------
    Shorter relative deadline $\rightarrow$ higher priority.

8.4 Analysis 
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
      
