import heapq
import time
import re
import vcomm

"""
http://qlj.sh.cn/python/20100402/python-time/
"""

CONTFILETYPE = 2
ISOTIMEFORMAT = "%Y-%m-%d %H:%M:%S"

class Event(object):
    """
    """
    
    def __init__(self, t, sim):
        """
        """
        self.timestamp = t
        self.sim = sim
#        print self.timestamp

    def handler(self):
        """
        
        Arguments:
        - `self`:
        """
        print "EventHandler called!"

    def __str__(self):
        """
        """
        return time.strftime(ISOTIMEFORMAT,time.localtime(self.timestamp))
 
        
class TaxiContEvent(Event):
    """
    """
    
    def __init__(self, t, vn1, vn2, sim):
        """
        """
        Event.__init__(self, t, sim)
        self.vName1 = vn1
        self.vName2 = vn2

    def handler(self):
        """
        """
#        print "TaxiContEvent:" + str(self)
        node1 = self.sim.nodeDict[self.vName1]
        node2 = self.sim.nodeDict[self.vName2]

        pkt1 = node1.peek_pkt()
        pkt2 = node2.peek_pkt()
        if pkt1 != None:
            if node2.insert_pkt(pkt1):
                self.sim.networkcost += 1
                print self.vName1 + "->" + self.vName2
        if pkt2 != None:
            if node1.insert_pkt(pkt2):
                self.sim.networkcost += 1
                print self.vName2 + "->" + self.vName1

        if pkt1 != None:
            if pkt1.has_dst(node2):
                pkt1.pktreachtimestamp = self.sim.simclock
                return True

        if pkt2 != None:
            if pkt2.has_dst(node1):
                pkt2.pktreachtimestamp = self.sim.simclock
                return True
        
        return False

    def __str__(self):
        """
        """
        return Event.__str__(self) + ' ' + self.vName1 + ' ' + self.vName2
        


class EventQueue(object):
    """
    the priority queue of events, ordered by the timestamp
    the event with the smallest timestamp is consumed first
    """
    _eventHeap= []
    _count = 0
    starttime = None
    def __init__(self, cntfile, sim):
        """
        """
        self.sim = sim
        fcont = open(cntfile,'r')
        if int(fcont.readline())!=CONTFILETYPE:
           raise NameError( 'Invalid file type')
        for line in fcont:
            result =  re.split(",|\n", line)
            vn1 = min(result[0], result[1])
            vn2 = max(result[0], result[1])

            if vn1 not in sim.nodeDict:
                sim.nodeDict[vn1] = vcomm.Node(vn1)
            if vn2 not in sim.nodeDict:
                sim.nodeDict[vn2] = vcomm.Node(vn2)
            newTimeStamp = time.mktime(time.strptime(result[2], '%Y-%m-%d %H:%M:%S'))
            if self.starttime == None:
                self.starttime = newTimeStamp
            else:
                self.starttime = min(self.starttime, newTimeStamp)
                
            newEvent = TaxiContEvent(newTimeStamp, vn1, vn2, sim)
            self.insert_event(newEvent)
        fcont.close()

    def consume_event(self):
        """
        pop the event with the smallest timestamp and return
        """
        if self._count > 0:
            tmpts, tmpevent = heapq.heappop(self._eventHeap)
            self._count -= 1
            self.sim.simclock = tmpts
            return tmpevent
        else:
            return None
        
    def insert_event(self, ev):
        """
        """
        heapq.heappush(self._eventHeap, [ev.timestamp, ev])
        self._count += 1
        
            
        
if __name__ == "__main__":
    tce1 = TaxiContEvent(1,'v1','v2')
    tce2 = TaxiContEvent(35, 'v3','v4')

    print tce1
    print tce2

"""   
    eq = EventQueue('dumpsmall.cont')
    tmpevent = eq.consume_event()
    while tmpevent != 0:
        print tmpevent
        tmpevent = eq.consume_event()
"""        

"""
    b = time.strptime('2007-02-03 00:00:00','%Y-%m-%d %H:%M:%S')
    print b
    print time.mktime(b)
    print time.ctime(time.mktime(b))
    t = time.time()
    print t
    print time.ctime(t)
    print time.ctime()
    print ' 321.3'
    print float(' 321.3')+1

    p=({})
    p[1]='hello'
    p[7]='hi'
    p['idx'] = 9
#    p.add({2:'hi'})
#    p.fromkeys(2:'hi')
    print p




    
"""
