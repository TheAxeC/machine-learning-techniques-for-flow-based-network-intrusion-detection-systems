
from config import Config
from train import Trainer
from ml import SupportVectorMachine

config = Config()
config.read_config()

# Load algortihm
algorithm = SupportVectorMachine()

# Start training
trainer = Trainer()
netflow = trainer.train_supervised(algorithm, 'src/capture20110816-2.binetflow')

# Start prediction
i = 0
max_num = 10000 #netflow.get_size()
while i < max_num:
    result = algorithm.predict(netflow.get_sample_data()[i])
    test = result == netflow.get_target_data()[i]
    if not test:
        print "Expected " + netflow.get_target_data()[i] + " Got: " + result
    i = i + 1
