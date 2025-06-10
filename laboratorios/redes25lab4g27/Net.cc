#ifndef NET
#define NET

#include <omnetpp.h>
#include "packet_m.h"
#include "feedbackPacket_m.h"

#define INPUT_FEEDBACK 2
#define DISTANCEARR_SIZE 300 // Replace with spected nodes. Let some margin.
#define LINK0 0 
#define LINK1 1

using namespace omnetpp;

class Net: public cSimpleModule {
private:
    cOutVector hopCountVector;
    int distanciasDerecha[DISTANCEARR_SIZE];
    int distanciasIzquierda[DISTANCEARR_SIZE];
    int preferedDoor[DISTANCEARR_SIZE];
    int feedCounter;
    int nodeNumber;

public:
    Net();
    virtual ~Net();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};

Define_Module(Net);

#endif /* NET */

Net::Net() {
}

Net::~Net() {
}

void Net::initialize() {
    hopCountVector.setName("HopCount");

	// Since we will be using this a lot, save it into a variable.
	nodeNumber = this->getParentModule()->getIndex(); 

    // Crear feedback packets
    FeedbackPkt *fbp0 = new FeedbackPkt();
    FeedbackPkt *fbp1 = new FeedbackPkt();
    
    // no es del todo necesario pero da risa (Estas medio loquito che)
    // for (int i = 0; i < (int)fbp0->getDistancesArraySize();i++) {
    //     distanciasDerecha[i] = 69420;
    //     distanciasIzquierda[i] = 69420;
    //     fbp0->setDistances(i, 69420);
    //     fbp1->setDistances(i, 69420);
    // }
    
    // Inicializar feedback packets
    fbp0->setName("Link 0");
    fbp0->setKind(INPUT_FEEDBACK);
    fbp0->setSource(nodeNumber);
    fbp0->setHopCount(0);
    fbp0->setDistances(nodeNumber, fbp0->getHopCount());
    fbp0->setSide(LINK0);

    fbp1->setName("Link 1");
    fbp1->setKind(INPUT_FEEDBACK);
    fbp1->setSource(nodeNumber);
    fbp1->setHopCount(0);
    fbp1->setDistances(nodeNumber, fbp1->getHopCount());
    fbp1->setSide(LINK1);

    // Enviar a sus respectivos links
    send(fbp0, "toLnk$o", LINK0);
    send(fbp1, "toLnk$o", LINK1);

    feedCounter = 0; // This will count how many feedbackpackets came back.a
}

void Net::finish() {
}

void Net::handleMessage(cMessage *msg) {

    FeedbackPkt *fbpkt = (FeedbackPkt *) msg;

    if (fbpkt->getKind() == INPUT_FEEDBACK) {

        this->bubble("FEEDBACK PKT RECIVED");

        // Si es el destino (ya dio toda la vuelta)
        if (fbpkt->getSource() == nodeNumber) {

            feedCounter++;

            // Actualizar matriz de costos
            for (int i = 0 ; i < (int)fbpkt->getDistancesArraySize(); i++) {
                if (fbpkt->getSide() == LINK0) {
                    distanciasDerecha[i] = fbpkt->getDistances(i);
                } else { // if (fbpkt->getSide() == LINK1) no hace falta. Si no es 0, es 1
                    distanciasIzquierda[i] = fbpkt->getDistances(i);
                }
            }

            // Set preferedDoor array when feedCounter equals 2.
            if (feedCounter == 2) {
        		this->bubble("setting preferedDoor...");
                for (int i = 0; i < (int)fbpkt->getDistancesArraySize(); i++) {
                    preferedDoor[i] = (int) (distanciasDerecha[i] > distanciasIzquierda[i]);
                    // preferedDoor[i] will save 0 or 1 depending on the value returned by this.
                    // Cast bool to int
                }
            }

            delete(fbpkt);

        } else {
            // Aumentar la cantidad de saltos que hizo
            fbpkt->setHopCount(fbpkt->getHopCount() + 1);

            // Guardar en su matriz interna cuantos saltos le llevó hacer hasta el nodo actual
            fbpkt->setDistances(nodeNumber, fbpkt->getHopCount());
            send(fbpkt, "toLnk$o", fbpkt->getSide());
        }
    } else {
        Packet *pkt = (Packet *) msg;
        this->bubble("PKT RECIVED");

        // If this node is the final destination, send to App
        if (pkt->getDestination() == nodeNumber) {
            send(msg, "toApp$o");
            // registramos los saltos que realizo el paquete
            hopCountVector.record(pkt->getHopCount());
        }
        // if not, forward the packet to some else... to who?
        else {
            // enviamos al link #0 o #1 dependiendo si el 
            // costo de saltos es menor por izq o der.
            // if (preferedDoor[pkt->getDestination()]) {
            //     send(msg, "toLnk$o", LINK0);
            // } else {
            //     send(msg, "toLnk$o", LINK1);
            // }
            send(msg, "toLnk$o", preferedDoor[pkt->getDestination()]);
            // aumentamos el hopCount
            pkt->setHopCount(pkt->getHopCount() + 1);
        }
    }
}

