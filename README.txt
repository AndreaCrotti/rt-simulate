                            *RT SIMULATE*
                            =============

Author: andrea crotti <andrea.crotti.0@gmail.com>
Date: 2009-08-18 17:04:34 CEST


This program will show interactively how some real time algorithms work.
It works as:
1. insert a set of tasks
2. choose a scheduling algorithm
3. check if is schedulable or not

Tasks are taken from the command line or from a configuration file.

[This] is the official site, more information on laboratories [here].

Using a MVC pattern to design the application, which must be easily adapt to new algorithms and data types.


[This]: http://dit.unitn.it/~abeni/RTOS/index.html
[here]: http://dit.unitn.it/~abeni/RTOS/lab.html

Table of Contents
=================
1 Languages used 
2 Frameworks 
3 Language table 
4 Theory summary 
    4.1 STATIC scheduling algorithm 
    4.2 Fixed priority scheduling 
    4.3 Dynamic priority scheduling algorithms: 
        4.3.1 Deadline monotonic 
        4.3.2 Rate monotonic 
    4.4 Analysis 


1 Languages used 
~~~~~~~~~~~~~~~~~
  - python (for the gui and control interface)
  - C/pyrex extension (for the algorithm engine)

2 Frameworks 
~~~~~~~~~~~~~
  - wxgtk/gtk/dialog?
  - [How to learn wxpython]
    

  [How to learn wxpython]: http://wiki.wxpython.org/How%20to%20Learn%20wxPython

3 Language table 
~~~~~~~~~~~~~~~~~

    Task         Schedulable entity            
    Preemptive   OS can regain control of cpu  
    WCET         Worst Case Execution Time     

4 Theory summary 
~~~~~~~~~~~~~~~~~
  OS kernel creates the illusion of multiple CPUs, concurrency is implemented by multiplexing tasks.
  Tasks are associated to temporal constraints (*deadlines*)
  
  Scheduler is responsible for selecting the tasks to execute.
  
Algorithms:

4.1 STATIC scheduling algorithm 
================================
   - Time axis divided in time slots
   - Slots statically allocated to the tasks
   - $\tau$ = *gcd*, $T$ = *lcm*
   - Very simple implementation, no operating system needed

     *NOT VERY CLEAR HOW TO IMPLEMENT THIS, only frequencies and timings in the slides.*
     What's the deadline in this case?
     In general enough to fire a timer every *minor cycle*.

4.2 Fixed priority scheduling 
==============================
   Very simple /preemptive/ scheduling algorithm.
   - every task has a fixed priority p_i
   - active task with highest priority are scheduled

     To have a better response of the system the priority must be chosen dynamically.
     So the problem becomes, how to assign priorities to manage to have a schedulable set of tasks?

4.3 Dynamic priority scheduling algorithms: 
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


     [rate monotonic]: sec-4.3.2
     [deadline monotonic]: sec-4.3.1

4.3.1 Deadline monotonic 
-------------------------
    Shorter period $\rightarrow$ higher priority.

4.3.2 Rate monotonic 
---------------------
    Shorter relative deadline $\rightarrow$ higher priority.

4.4 Analysis 
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
