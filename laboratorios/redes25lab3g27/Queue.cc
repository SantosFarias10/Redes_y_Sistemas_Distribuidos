#ifndef QUEUE
#define QUEUE

#include <string.h>
#include <omnetpp.h>

using namespace omnetpp;

class Queue: public cSimpleModule {
private:
    cQueue buffer;
    cMessage *endServiceEvent;
    simtime_t serviceTime;
    cOutVector bufferSizeVector;
    cOutVector packetDropVector;
public:
    Queue();
    virtual ~Queue();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};

Define_Module(Queue);

Queue::Queue() {
    endServiceEvent = NULL;
}

Queue::~Queue() {
    cancelAndDelete(endServiceEvent);
}

void Queue::initialize() {
    buffer.setName("buffer");
    endServiceEvent = new cMessage("endService");
    bufferSizeVector.setName("bufferSize");
    packetDropVector.setName("packetDrop");
}

void Queue::finish() {}

void Queue::handleMessage(cMessage *msg) {
    // if msg is signaling an endServiceEvent
    if (msg == endServiceEvent) {
        // if packet in buffer, send next one
        if (!buffer.isEmpty()) {
            // dequeue packet
            cPacket *pkt = (cPacket*) buffer.pop();
            // send packet
            send(pkt, "out");
            // start new service
            serviceTime = pkt->getDuration();
            scheduleAt(simTime() + serviceTime, endServiceEvent);
        }
    } else { // if msg is a data packet
        // check buffer limit
        if (buffer.getLength() >= par("bufferSize").intValue()) { // longValue() no nos funciona
            delete msg;
            this->bubble("packet dropped");
            packetDropVector.record(1);
        } else {
            // enqueue the packet
            buffer.insert(msg);
            bufferSizeVector.record(buffer.getLength());
            // if the server is idle 
            if (!endServiceEvent->isScheduled()) {
                // start the service now
                scheduleAt(simTime(), endServiceEvent);
            }
        }
    }
}

#endif /* QUEUE */
