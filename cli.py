def run(tasksets):
    for name, tset in tasksets.items():
        print "\n\t STARTING TO ANALYZE %s: \n" % name
        print tset
        if tset.schedule():
            print tset.timeline


        
