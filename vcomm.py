from collections import deque

class Node(object):
    """
    the communication agent. every vehicle, RSU, Base station, AP is a node
    """
    
    def __init__(self, nm):
        """
        """
        self.name = nm
        self._pktqueue = list()
        
    def __str__(self):
        """
        
        Arguments:
        - `self`:
        """
        return self.name

    def pick_pkt(self):
        """
        Arguments:
        - `self`:
        """
        try:
            return self._pktqueue.pop(0)
        except IndexError:
            return None
        
    def peek_pkt(self):
        """
        Arguments:
        - `self`:
        """
        try:
            return self._pktqueue[0]
        except:
            return None
        

    def insert_pkt(self, pkt):
        """
        """
        try:
            self._pktqueue.index(pkt)
            return False
        except:
            self._pktqueue.append(pkt)
            return True
        
class Packet(object):
    """
    the packet transmitted between the nodes
    """
    def __init__(self, pktid, src, dst, starttime, content):
        """
        """
        self.pktid = pktid
        self.pktsrc = src
        self.pktdst = dst
        self.pktcontent = content
        self.pktstarttimestamp = starttime
        self.pktreachtimestamp = None

    def has_dst(self, node):
        """
        
        Arguments:
        - `self`:
        - `node`:
        """
        return self.pktdst == node.name

    def has_src(self, node):
        """
        Arguments:
        - `self`:
        - `node`:
        """
        return self.pktsrc == node.name

    def has_arrived(self):
        """
        """
        return self.pktreachtimestamp != None

        
if __name__ == "__main__":
    n = Node('a_vehi')
    n.insert_pkt('pkt1')
    n.insert_pkt('pkt2')
    n.insert_pkt('pkt_fwu')
    n.insert_pkt(2)

    pkt = n.pick_pkt()
    while pkt != None:
        print pkt
        pkt = n.pick_pkt()

