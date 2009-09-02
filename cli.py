def run(tasksets):
    for x in tasksets.items():
        analyze(x)

def analyze(taskset):
    name, tset = taskset
    print "\n\t ANALYZING %s \n%s" % (name, str(tset))
    if not(tset.is_schedulable()):
        print "this task set is not schedulable\n"
    else:
        tset.schedule()
        print "TIMELINE:\n %s" % str(tset.timeline)
