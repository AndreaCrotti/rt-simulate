#define N 2

byte clock = 0;
bool done[N] = false;

proctype T(byte ID, period, exec) {
  byte next = 0;
  do
    :: atomic {
      clock >= next ->
      clock = clock + exec;
      next = next + period;
      done[ID] = true;
    }
  od
}

proctype watchdog(byte ID, period) {
  byte deadline = period;
  do
    :: atomic {
      clock >= deadline ->
      assert done[ID];
      deadline = deadline + period;
      done[ID] = false
    }
  od
}


proctype idle() {
  do
    :: atomic {
      timeout -> clock++
    }
  od
}

init {
  atomic {
    run idle();
    run T(0, 2, 1);
    run watchdog(0, 2);
    run T(1, 5, 2);
    run watchdog(1, 5);
  }
}