# ------------------------------------
#  CallerID.com
#  info@callerid.com
#
#  Written: 2019
#
#  Simple UDP listener which parses CallerID.com records

import socket # Used for bidning to port
import re # Used for parsing parts of CallerID.com records
import sys # Used to terminate program

LISTEN_ON_UDP_PORT = 3520
NON_DETAILED_PATTERN = ".*(\d\d) ([IO]) ([ESB]) (\d{4}) ([GB]) (.)(\d) (\d\d/\d\d \d\d:\d\d [AP]M) (.{14})(.{15})"
DETAILED_PATTERN = ".*(\d\d) ([NFR]) {13}(\d\d/\d\d \d\d:\d\d:\d\d)"

# ---------------------------------------------------------
#                 FUNCTIONS
# ---------------------------------------------------------

# TAKE INPUT DATA AND PARSE PARTS
def parse_packet(packet):

    # Decode packet from bytes to readable text
    packet = packet.decode("utf-8")

    non_detailed_match = re.search(NON_DETAILED_PATTERN, packet)
    detailed_match = re.search(DETAILED_PATTERN, packet)

    # Call type
    detailed_call = False

    # Parsed non_detailed variables for use in program
    pLineNumber = ""
    pInboundOrOutbound = ""
    pStartOrEnd = ""
    pDuration = ""
    pCheckSum = ""
    pRingType = ""
    pRings = ""
    pDateTime = ""
    pNumber = ""
    pName = ""

    # Parsed detailed variables for use in program
    pDetailedStatus = ""
    pDetailedDate = ""

    # If call is a non-deatiled packet
    if non_detailed_match:

        # Set call type
        detailed_call = False

        # Parse variables
        pLineNumber = non_detailed_match.group(1)
        pInboundOrOutbound = non_detailed_match.group(2)
        pStartOrEnd = non_detailed_match.group(3)
        pDuration = non_detailed_match.group(4)
        pCheckSum = non_detailed_match.group(5)
        pRingType = non_detailed_match.group(6)
        pRings = non_detailed_match.group(7)
        pDateTime = non_detailed_match.group(8)
        pNumber = non_detailed_match.group(9)
        pName = non_detailed_match.group(10)

        # For testing purposes - check variables
        print("Call Record ----------\n")
        print("Line: " + pLineNumber + "\n")
        print("IO: " + pInboundOrOutbound + "\n")
        print("SE: " + pStartOrEnd + "\n")
        print("DUR: " + pDuration + "\n")
        print("CHKS: " + pCheckSum + "\n")
        print("Ring: " + pRingType + pRings + "\n")
        print("DateTime: " + pDateTime + "\n")
        print("Number: " + pNumber + "\n")
        print("Name: " + pName + "\n")
        print("----------------------\n")


    # If call is a detailed packet
    if detailed_match:

        # Set call type
        detailed_call = True

        # Parse variables
        pLineNumber = detailed_match.group(1)
        pDetailedStatus = detailed_match.group(2)
        pDetailedDate = detailed_match.group(3)

        # For testing purposes - check variables
        print("Detailed Record ----------\n")
        print("Line: " + pLineNumber + "\n")
        print("Status: " + pDetailedStatus + "\n")
        print("DateTime: " + pDetailedDate + "\n")
        print("--------------------------\n")

    # ---------------------------------------
    # Your code below, using parsed variables
    #
    #   if detailed_call:
    #       - Handle detailed
    #         accordingly
    #
    #   else:
    #       - Handle start or end record
    #         accordingly
    #
    # ---------------------------------------

# ---------------------------------------------------------
#                Listener - main program
# ---------------------------------------------------------

rec_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
rec_sock.bind(("0.0.0.0", LISTEN_ON_UDP_PORT))

print("This code will bind to port " + str(LISTEN_ON_UDP_PORT) + ".\n" +
      "To re-run this code, you will need to kill it's process in the " +
      "task manager.\n\n")

while True:
    data, addr = rec_sock.recvfrom(1500)
    parse_packet(data)
