packet FeedbackPkt {
    int remainingBuffer;
    int ack;
    bool slowTx = false;
    bool almostFull = false;
};
