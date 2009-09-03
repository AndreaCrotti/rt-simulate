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
        print "\nHYPERPERIOD: %d\n" % tset.hyper
        print "\nUSING ALGORITHM: %s\n" % tset.algo
        print "TIMELINE:\n %s" % str(tset.timeline)
