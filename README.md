# CyberRangeIEC61850
This is a SUTD's MSSD thesis on " Cyber Range of Critical Infrastructure for Cybersecurity Experiment" 2024


There are 2 version in this repository
1. One is the linux version (which is fully tested with ubuntu 22.4.3 with lot more options, though some options would rquired to have to input administrative password to execute).
2. The other is the windows version (which required Administrative priviliage to run, though it can be set up in the tasks but it is tedious and cumbersome. Hence most testing is done with Linux version instead).

Concepts of the CyberRange
Both the Linux and Windows version are that intended to allow testers/users to conduct stepwise simulation.
Depending on the setup, the network diagram will provide good indication and connection details of the simulated environment setup.
First, gathered information (for windows -use the IEDExplorer/ObjectInfo), for linux use the ObjectInfo
to find out the Logical Devices and Logical Nodes info for further experimentation later.
Next , progressively move on and click the next "clickable" options.

There are 2 main test domain:
MMS - testing and GOOSE- testing. Testers/users not necessarily need to do the simulation sequentially, you are free to skip and move on to other "clickable" within the domain, or move between MMS and GOOSE.

Lastly, to allow testers/users to do a simple self assessment based on their understanding of their own setup. There is a CCOP-OT (V2 and focuses on OT only), help testers/users to do a self assessment to check if their own/existing OT setup compliance status aligning with CCOP V2-OT.
The total compliance as well individual compliance results will be shown after the testers/users dutifully responded to the clauses indicated.

Thank you and have a good experiential experiment.


