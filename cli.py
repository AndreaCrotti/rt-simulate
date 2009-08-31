def run(tasksets):
    for name, tset in tasksets.items():
        if tset.schedule():
            print name
            print tset.timeline


        
