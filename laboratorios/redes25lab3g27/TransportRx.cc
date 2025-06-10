#ifndef TRANSPORTRX
#define TRANSPORTRX
#define ASK_SLOW 3
#define INFO_PACKET 2

#include <string.h>
#include <omnetpp.h>
#include "FeedbackPkt_m.h"
#include "DataPkt_m.h"

using namespace omnetpp;

class TransportRx : public cSimpleModule{
    private:
        cQueue buffer;

        cMessage *endServiceEvent;
        cMessage *sendFeedbackEvent;

        cChannel *RxChannel;

        simtime_t nextFree;
        simtime_t sendFeedbackDelay;
        simtime_t sinkDelay;

        cOutVector bufferSizeVector;
        cOutVector packetDropVector;
        cOutVector packetIn;
        cOutVector packetOut;
        
        int pktDropCount;
        int remainingBuffer;
        int ack;
        int sentPkts[200];
    public:
        TransportRx();
        virtual ~TransportRx();
    protected:
        virtual void initialize();
        virtual void finish();
        virtual void handleMessage(cMessage *msg);
};

Define_Module(TransportRx);

TransportRx::TransportRx() {
    endServiceEvent = NULL;
    sendFeedbackEvent = NULL;
};

TransportRx::~TransportRx() {
    cancelAndDelete(endServiceEvent);
};

void TransportRx::initialize(){
    buffer.setName("buffer");

    endServiceEvent = new cMessage("endService");
    sendFeedbackEvent = new cMessage("sendFeedback");

    bufferSizeVector.setName("bufferSize");
    packetDropVector.setName("packetDrop");
    pktDropCount = 0;

    packetIn.setName("pacektsIn");
    packetOut.setName("packetsOut");

    RxChannel = gate("toOut$o")->getTransmissionChannel();
};

void TransportRx::finish(){};

void TransportRx::handleMessage(cMessage *msg) {

    // if msg is signaling an endServiceEvent
    if (msg == endServiceEvent) {
        // if packet in buffer, send next one
        if (!buffer.isEmpty()) {
            // dequeue packet
            DataPkt *pkt = (DataPkt*) buffer.pop();

            // Save header data and remove it.
            ack = pkt->getAck();
            cPacket *deHeadedPkt= pkt->decapsulate();

            // send packet if wasn't already send
            if (sentPkts[ack-100] != ack) {
              send(deHeadedPkt, "toOut$o");
              sentPkts[ack-100] = ack;
              // contamos cuantos paquetes salen de Rx
              packetOut.record(1);
            }
            else {
              this->bubble("Packet already sent! Ignoring");
            }

            // Schedule next iteration
            scheduleAt(simTime(), sendFeedbackEvent);
        }
    } else if (msg == sendFeedbackEvent) {
        FeedbackPkt* feedbackPkt = new FeedbackPkt();
        feedbackPkt->setAck(ack);
        feedbackPkt->setKind(INFO_PACKET);
        // contamos cuantas veces entran a Rx
        packetIn.record(1);
        // check buffer limit
        if (buffer.getLength() >= par("bufferSize").intValue() - (par("bufferSize").intValue())/2) {
            // cola llena al 50%
            // caso especifico de estudio 1 (Cola de traRx llena)
            // dividido en partes para intentar evitar perder paquetes
            feedbackPkt->setRemainingBuffer(par("bufferSize").intValue() - buffer.getLength());
            feedbackPkt->setKind(ASK_SLOW);

            if (buffer.getLength() >= par("bufferSize").intValue() - (par("bufferSize").intValue())/4) {
                // cola Rx esta casi llena al 75%
                feedbackPkt->setAlmostFull(true);
            } else if (buffer.getLength() >= par("bufferSize").intValue() - (par("bufferSize").intValue())/2) {
                // cola Rx al 50%
                feedbackPkt->setSlowTx(true);
            }
        }
        send(feedbackPkt, "toApp");
        sinkDelay = std::max(simTime(), RxChannel->getTransmissionFinishTime());
        scheduleAt(sinkDelay, endServiceEvent);

    } else if (buffer.getLength() >= par("bufferSize").intValue()) {
        // caso especifico de cola llena
        delete msg;
        this->bubble("packet dropped");
        packetDropVector.record(pktDropCount++);
    } else {
        // enqueue the packet
        buffer.insert(msg);
        bufferSizeVector.record(buffer.getLength());
        // if the server is idle
        if ((!endServiceEvent->isScheduled()) && (!sendFeedbackEvent->isScheduled())) {
            // start the service now
            scheduleAt(simTime() + 0.1, endServiceEvent); // Give some margin in case a packet is still being sent.
        }
    }
}

#endif /* TRANSPORTRX */
