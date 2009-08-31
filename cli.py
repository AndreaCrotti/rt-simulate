def run(tasksets):
    for name, tset in tasksets.items():
        print name
        tset.schedule()
        print tset.timeline

        
