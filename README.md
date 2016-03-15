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

## Thesis table of contents:
- Introduction
    * Explanation of IDS
    * Netflow
    * Why use machine learning
    * Existing solutions
- Attack classification
    * attack descriptions
    * discovery methods
    * flow discovery methods
- Machine learning
    * What is machine learning
    * How to implement a machine learning algorithm
- How to use flows
- Implementation
    * Which datasets are used
    * What are implementation decisions
    * results from tests
- How to report detections
- Can packet and flow analysis be combined
- Prevention
- Conclusion

# Program
## Flow data
Flow data has a very specific structure. To be able to use the flow data for machine learning the data is processed as follows:
- ports (src + dest)
    * Defined Ports as 1
    * random ports as 0
- IP Data: (src + dest)
    * IPv6 as 0
    * IPv4 as 1
    * MAC address as 2
- Protocol
    * tcp as 0
    * udp as 1
    * other as 2
- duration
- total amount of packets
- total amount of bytes
- total srcbytes
- Starting time
- Type of service (ToS)

Converting port number into binary is too slow. Ability to set severity of feature.

## Labels:
Prediction algorithms predict whether the data is:
- Malicious
    * categorize
- Normal
    * categorize

The algorithm tries to predict a label as specific as possible.

## Logging
Logging:
- Printing all records
- Print predictions
- Print fails (in check)
- Print trained model
- Progression bar training
- Print record training
- Things to check on overfitting etc

Visualisation:
- Keep detected links in database/json
- Find similarities/connections
- Graphing

# Development
## TODO:
- chapter ML-IDS has to be merged into ML chapter
- already discuss why using a certain (KNN) algorithm compared to others
- Uitbreiden van aanvallen
- Existing solutions

## Remarks:
- IP by country has low effect
- timestamps --> not enough data, algorithm can work with continuous timestamps
- Extraction labels can be done by hand, depends on dataset

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

## Planning:
- Week 5: ML cursus verwerkt --> done
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

- meeting 11/03 en 14/03
- http://scikit-learn.org/0.15/auto_examples/plot_classification_probability.html
- http://scikit-learn.org/stable/tutorial/machine_learning_map/index.html
- http://scikit-learn.org/stable/auto_examples/svm/plot_iris.html
