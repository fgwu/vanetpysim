import vevent
import random
import vcomm
import time


class Simulator(object):
    """
    """
    def __init__(self,cntfile):
        """
        """
        self.nodeDict = ({})
        self.eventQueue = vevent.EventQueue(cntfile, self)
        
        

        self.networkcost = 0 # in hop counts
        self.simclock = self.eventQueue.starttime
        self.eventconsumed = 0

        try:
            rndsrc = random.choice(dict.keys(self.nodeDict))
            rnddst = random.choice(dict.keys(self.nodeDict))
        except:
            raise

        rndsrc = 't17602ai'
        rnddst = 't89515ai'
        print 'rndsrc' + ' ' + rndsrc
        print 'rnddst' + ' ' + rnddst

        self.testpkt = vcomm.Packet(1, rndsrc, rnddst, self.simclock, "this is packet content")
        self.nodeDict[rndsrc].insert_pkt(self.testpkt)

    def run(self):
        """
        """
        tmpevent = self.eventQueue.consume_event()
        while tmpevent:
            self.eventconsumed += 1
            if tmpevent.handler():
#                print 'packet successful delivered!'
                break
            tmpevent = self.eventQueue.consume_event()
        if self.testpkt.has_arrived():
            print 'packet successfully delivered'
#            print 'delay is '+ time.strftime("%H:%M:%S", time.localtime(self.testpkt.pktreachtimestamp - self.testpkt.pktstarttimestamp))
            print 'delay is %.2f hours' % ((self.testpkt.pktreachtimestamp - self.testpkt.pktstarttimestamp)/3600)
            print 'network cost is ' + str(self.networkcost) + ' hops'
            print 'event consumed No. is ' + str(self.eventconsumed) + ' events'
        else:
            print 'packet has not arrive at the destination'
            
if __name__ == "__main__":
    time.clock()
    sim = Simulator('d201/cont.dump')
#    sim = Simulator('dump.cont')

    sim.run()
    print 'the simulation takes %2.f minutes' + (time.clock()/60)

#    for i in sim.nodeDict:
#        print str(i) + ' ' + str(sim.nodeDict[i])
