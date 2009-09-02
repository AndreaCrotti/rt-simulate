def run(tasksets):
    for name, tset in tasksets.items():
        print "\n\t ANALYZING %s \n%s" % (name, str(tset))
        if not(tset.is_schedulable()):
            print "this task set is not schedulable\n"
        else:
            tset.schedule()
            print "TIMELINE:\n %s" % str(tset.timeline)
