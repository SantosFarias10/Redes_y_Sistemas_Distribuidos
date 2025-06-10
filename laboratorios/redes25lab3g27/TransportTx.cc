#ifndef TRANSPORTTX
#define TRANSPORTTX
#define CHECK_INTERVAL 10
#define INFO_PACKET 2
#define ASK_SLOW 3

#include <string.h>
#include <omnetpp.h>
#include "FeedbackPkt_m.h"
#include "DataPkt_m.h"

using namespace omnetpp;

class TransportTx : public cSimpleModule{
    private:
        cQueue buffer;

        cMessage *endServiceEvent;

        cChannel *RxChannel;

        simtime_t slowDown;
        simtime_t serviceTime;
        simtime_t temp;
        simtime_t sendDelay;

        cOutVector bufferSizeVector;
        cOutVector packetDropVector;
        cOutVector packetIn;
        cOutVector packetOut;

        int pktDropCount;
        int ack;
        int remainingBufferTx;
        int remainingBufferRx;
        unsigned int counter;

        cMessage *reSend = new cMessage("reSend");
        std::map <int,DataPkt *> checkList; // Dictionary-like mapping using ack and pointer

    public:
        TransportTx();
        virtual ~TransportTx();
    protected:
        virtual void initialize();
        virtual void finish();
        virtual void handleMessage(cMessage *msg);
};

Define_Module(TransportTx);

TransportTx::TransportTx() {
    endServiceEvent = NULL;
};

TransportTx::~TransportTx() {
    cancelAndDelete(endServiceEvent);
};

void TransportTx::initialize() {
    buffer.setName("buffer");

    endServiceEvent = new cMessage("endService");

    bufferSizeVector.setName("bufferSize");
    packetDropVector.setName("packetDrop");
    pktDropCount = 0;

    packetIn.setName("pacektsIn");
    packetOut.setName("packetsOut");

    remainingBufferTx = par("bufferSize").intValue();
    remainingBufferRx = 0;

    RxChannel = gate("toOut$o")->getTransmissionChannel();

    ack = 100;
    counter = 0;
};

void TransportTx::finish(){};

void TransportTx::handleMessage(cMessage *msg) {
    // if msg is signaling an endServiceEvent
    if (msg == endServiceEvent) {

        // if packet in buffer, send next one
        if (!buffer.isEmpty()) {
            // Dequeue packet
            DataPkt *pkt = (DataPkt *) buffer.pop();

            // Save DataPkt in case it has to be sent again
            checkList[ack] = pkt;

            // Send packet
            send(pkt, "toOut$o");
            packetOut.record(1);

            // Start new service

            if (simTime() >= temp) slowDown = 0;

            sendDelay = std::max(simTime(), RxChannel->getTransmissionFinishTime());
            simtime_t nextSend = sendDelay + slowDown; 

            if (counter++ <= CHECK_INTERVAL) {
              scheduleAt(nextSend, endServiceEvent);
              this->bubble("endServiceEvent");
            } else {
              scheduleAt(nextSend, reSend);
              this->bubble("reSend!!!");
              counter = 0;
            }
        }

    } else if (msg->getKind() == ASK_SLOW || msg->getKind() == INFO_PACKET) {
        
        int kind = msg->getKind();

        // contamos cuantos paquetes entran en Tx
        packetIn.record(1);

        FeedbackPkt *feedbackPkt = (FeedbackPkt*)msg;
        remainingBufferRx = feedbackPkt->getRemainingBuffer();
        remainingBufferTx = par("bufferSize").intValue() - buffer.getLength();

        /* para imprimir variables en burbujas, (debug con prints)
        char text[32];
        sprintf(text, "%d >= %d", remainingBufferRx, remainingBufferRx);
        this->bubble(text); */ 

        if (kind == ASK_SLOW) {    // Rx is asking for a slowdown
          if (remainingBufferRx <= remainingBufferTx) {
              // caso si la cola Rx esta mas llena que Tx
              if (feedbackPkt->getSlowTx()) {
                  // cola Rx esta al 50%
                  slowDown = 0.5;
                  temp = simTime() + 0.5;
                  this->bubble("RX AL 50%");
              } else if (feedbackPkt->getAlmostFull()) {
                  // cola Rx esta casi llena al 75%
                  slowDown = 1; temp = simTime() + 1;
                  this->bubble("RX AL 75%");
              } else {
                  // cola Rx esta abajo del 50%, en teoria nunca pasa este caso 
                  // pero yo ya no se siquiera si creo en dios
                  slowDown = 0.1;
                  temp = simTime() + 0.2;
                  this->bubble("POCO %");
              }
          } else {
              temp = 0;
              this->bubble("IGNORA");
          }
        }

        int num = feedbackPkt->getAck(); // check ack
          checkList[num] = NULL;
          char text[32];
          sprintf(text, "deleted %d", num);
          this->bubble(text);
          checkList.erase(num);
          if (ack >= 300) ack = 100;

        delete(msg);

    } else if (msg == reSend) {                     // Check for lost packets
        if (!checkList.empty()) {
          for (const auto& pair : checkList) {      // "For in" for "dictionaries"
            if (pair.first >= ack-(CHECK_INTERVAL/2)) break;   // Check only the first sent half

            char text[32];
            sprintf(text, "re-sending pkt %d", pair.first);
            this->bubble(text);

            DataPkt *pkt = pair.second;
            send(pkt->dup(), "toOut$o");
            serviceTime = ((cPacket *)buffer.front())->getDuration();
            sendDelay = std::max(simTime(), RxChannel->getTransmissionFinishTime());
            scheduleAt(sendDelay + slowDown, endServiceEvent);
            slowDown += 0.5;                        // Drastic delay since a resend means cloud is possibly overflowed.
            break;
          }
        }
    } else { // if msg is a data packet
        packetIn.record(1);
        // check buffer limit
        if (buffer.getLength() >= par("bufferSize").intValue()) {
            delete msg;
            this->bubble("packet dropped");
            packetDropVector.record(pktDropCount++);
        } else {
            // enqueue the packet
            cPacket *pkt = (cPacket*) msg; 

            // Add header with identification to package
            DataPkt *headedMsg = new DataPkt(); headedMsg->encapsulate(pkt);
            headedMsg->setAck(ack);
            ack++;

            // Insert it into buffer.
            buffer.insert(headedMsg);
            bufferSizeVector.record(buffer.getLength());
            // if the server is idle 
            if ((!endServiceEvent->isScheduled()) && (!reSend->isScheduled())) {
                // start the service now
                scheduleAt(simTime(), endServiceEvent);
            }
        }
    }
}

#endif /* TRANSPORTTX */
