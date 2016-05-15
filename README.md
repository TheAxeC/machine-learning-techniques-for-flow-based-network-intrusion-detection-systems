# Bachelor-thesis-ML-IPS
My Bachelor thesis for Bachelor Computer Science at UHasselt: An Intrusion detection (and prevention) system using machine learning approaches.

## Installation
The IDS requires the packets listed in the pip_requirements file and it requires:
- Python 2.7+
- tshark
- sklearn

# Program
## Flow data
Flow data has a very specific structure. To be able to use the flow data for machine learning the data is processed as follows:
- ports (src + dest)
    * Defined Ports as 1
    * random ports as 0
    * Heeft continue minder effect
- IP Data: (src + dest)
    * IPv6 as seperate continu feature
    * IPv4 as seperate continu feature
    * MAC address as seperate continu feature
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

# Development

## TODO:
- Visualisation
    * Logging
    * Graphing
- Writing thesis
    * Kernels
    * Neuralnet
    * Tree
    * Bayesian
    * Bagging
    * Recall
    * Learning curve
    * Samenvatting
    * Evaluation
    * Conclusion
    * Abstract
    * Acknowledgement
- Data Cegeka
- Poster
- Vulgariserende tekst

## Tips
- algemene tip: figuurtjes toevoegen ( ook bij poster) : interessante manier visueel voorstellen.
- probeer achter de ‘diepere’ vraag te komen: een dieper inzicht dat ze proberen te pollen a d h v een simpele vraag.
- alles HEEL SIMPEL kunnen uitleggen. (hopelijk zijn het informatici, dus leg het heel simpel en heel to the point uit).
- wat is het nut van de BP
- hoe valideren

- http://scikit-learn.org/0.15/auto_examples/plot_classification_probability.html
- http://scikit-learn.org/stable/tutorial/machine_learning_map/index.html
- http://scikit-learn.org/stable/auto_examples/svm/plot_iris.html
