simple Generator
{
    parameters:
        volatile double generationInterval; // sec
        volatile int packetByteSize;
        @display("i=old/laptop3");
    gates:
        output out;
}

simple Queue
{
    parameters:
        volatile int bufferSize;
        @display("i=block/queue;q=buffer");
    gates:
        input in;
        output out;
}

simple Sink
{
    parameters:
        @display("i=old/laptop3");
    gates:
        input in;
}

simple TransportTx
{
    parameters:
        volatile int bufferSize;
        @display("i=block/buffer;q=buffer");
    gates:
        input toApp;
        inout toOut;
}

simple TransportRx
{
    parameters:
        volatile int bufferSize;
        @display("i=block/buffer;q=buffer");
    gates:
        output toApp;
        inout toOut;
}

module NodeTx 
{
    parameters:
        @display("i=block/routing");
    gates:
        input in;
        output out;
    submodules:
        gen: Generator {
            parameters:
                @display("p=75,50");
        }
        traTx: TransportTx {
            parameters:
                @display("p=75,190");
        }
    connections:
        gen.out --> traTx.toOut$i;
        traTx.toOut$o --> out;
        in --> traTx.toApp; 
}

module NodeRx 
{
    parameters:
        @display("i=block/routing");
    gates:
        input in;
        output out;
    submodules:
        sink: Sink {
            parameters:
                @display("p=75,50");
        }
        traRx: TransportRx {
            parameters:
                @display("p=75,190");
        }
    connections:
        in --> traRx.toOut$i;
        traRx.toApp --> out;

        // caso estudio 1:
        traRx.toOut$o --> { datarate = 0.5Mbps; } --> sink.in;
        // caso estudio 2:
        // traRx.toOut$o --> { datarate = 1Mbps; } --> sink.in; 
}

network Network
{
    @display("bgl=2");
    submodules:
        nodeTx: NodeTx {
            @display("p=30,30");
        }
        queue0: Queue {
            @display("p=130,30");
        }
        nodeRx: NodeRx {
            @display("p=230,30");
        }
        queue1: Queue {
            @display("p=130,130");
        }
    connections:
        nodeTx.out --> { datarate = 1Mbps; delay = 100us; } --> queue0.in;
        
        // caso estudio 1
        queue0.out --> { datarate = 1Mbps; delay = 100us; } --> nodeRx.in;
        // caso estudio 2
        // queue0.out --> { datarate = 0.5Mbps; delay = 100us; } --> nodeRx.in;
        
        nodeRx.out --> queue1.in;
        queue1.out --> nodeTx.in;  
}
