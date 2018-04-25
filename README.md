# Test for a demonstrator

We have 2 clients and 1 server.

How it works ?
  - Client 1 sends a message to the server and receives an ack from it. We measure the latency and send it to ther server;
  - The server send a message to the client 2 when it receives a message from the client 1. It measures the latency between the client 2 and it;
  - Moreover, we have the latency of the process in the server. But in this version is equal to zero.
  
At the end, we want to measure the toal latency of the system and put measure in a csv file.
