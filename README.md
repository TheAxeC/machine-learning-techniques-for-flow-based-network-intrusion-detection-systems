# Bachelor-thesis-ML-IPS
My Bachelor thesis for Bachelor Computer Science at UHasselt: An Intrusion detection (and prevention) system using machine learning approaches.

## Installation
The IDS requires the packets listed in the pip_requirements file and it requires:
- Python 2.7+
- tshark

## Running the intrusion detection system
Running the intrusion detection system can be done by:
```
python main.py
```
Different settings can be configured in "config.json"

# Development

## Questions:
- glossary

## TODO:
- chapter ML-IDS has to be merged into ML chapter
- already discuss why using a certain (KNN) algorithm compared to others
- Uitbreiden van aanvallen
- Existing solutions

## Remarks:
- IP by country has low effect
- timestamps --> not enough data, algorithm can work with continuous timestamps
- Extraction labels can be done by hand, depends on dataset

## Flow data
- Ports are split into binary (src + dest)
    * Defined Ports
    * random ports
- IP Data: (src + dest)
    * IPv6
    * IPv4
    * MAC address
- Protocol
    * tcp
    * udp
    * other
- duration
- total amount of packets
- total amount of bytes
- total srcbytes
- Starting time
- Type of service (ToS)

## Labels:
- Malicious
    * categorize
- Normal
    * categorize

## TODO:
- Visualisation
    * Logging
    * Graphing
- Implementing different algorithms
- Writing thesis
- Analysing packets (scapy)?
- Running virus/botnet in VM and automatic labeling
- Creating models (running overnight)
- Data Cegeka
- Machine learning
- Preventie
- Poster
- Vulgariserende tekst

## Thesis table of contents:
- Introduction
    * Explanation of IDS
    * Netflow
    * Why use machine learning
    * Wat zijn de voor/nadelen van netflow
- Attack classification
- Machine learning
    * Hoe passen we machine learning toe op IDE en wat zijn de voor/nadelen
    * Welke machine learning algortimes zijn wel/niet gebruikt
- Hoe flows gebruiken
- Implementatie
    * Welke data sets zijn gebruikt
    * Wat zijn de bevindingen
- Hoe kan visualisatie/feedback gebeuren (richting admin en richting automatische preventie)
- Hoe met combinatie netflow/packets (Als dit gedaan zou worden)
- Preventie
- Conclusie

## Planning:
- Week 5: ML cursus verwerkt
- Week 6: Hoe flow data gebruiken
- Week 7: Implementatie testen
- Week 8: implementation hoofdstuk thesis
- Week 9: Visualisatie
- Week 10: Implementatie (multi-pass + visualisatie)
- Week 11: Attack classification
- Week 12: Afmaken draft
- Week 13-14: Extra: preventie
- Week 15: verwerken feedback draft
- Week 15+: Eventueel kleine experimentjes

## Tips
- algemene tip: figuurtjes toevoegen ( ook bij poster) : interessante manier visueel voorstellen.
- probeer achter de ‘diepere’ vraag te komen: een dieper inzicht dat ze proberen te pollen a d h v een simpele vraag.
- alles HEEL SIMPEL kunnen uitleggen. (hopelijk zijn het informatici, dus leg het heel simpel en heel to the point uit).
- wat is het nut van de BP
- hoe valideren
