# IIoT Sensor Data Simulation and Visualization

## Project Overview

This project was developed to simulate Industrial Internet of Things (IIoT) sensor data transmission using different protocols, and visualize the collected data in real time. The protocols explored included:

- MQTT - implemented and working
- CoAP - not functional due to network compatibility issues
- OPC UA - not functional due to asynchronous version conflicts on Windows

---

## What Worked

The **MQTT** protocol was successfully implemented using the `paho-mqtt` Python library. A simulation script was created to generate random temperature and humidity values and publish them every second to a local MQTT broker (`mosquitto`).
A **real-time visualization script** was developed using `matplotlib`, which subscribes to the MQTT topic and displays live sensor data in a graph.
A snapshot of the live graph was saved to the `visualizations/` folder.

---

## What Didn’t Work

- **CoAP** simulation (`aiocoap`) failed due to network errors and a missing CoAP server on localhost. Windows compatibility limitations made reliable testing difficult.
- **OPC UA** simulation (`asyncua`) raised runtime errors related to async API changes between library versions. Even after adjusting for the newer 1.x version, consistent execution on Windows remained problematic.
