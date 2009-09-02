def run(tasksets):
    for name, tset in tasksets.items():
        print "\n\t ANALYZING %s \n%s" % (name, str(tset))
        if not(tset.is_schedulable()):
            print "this task set is not schedulable\n"
        else:
            x = tset.schedule()
            if x:
                print "TIMELINE:\n %s" % str(tset.timeline)
