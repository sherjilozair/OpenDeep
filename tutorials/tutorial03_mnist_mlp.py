"""
Please refer to the following tutorial in the documentation at www.opendeep.org

Tutorial: Classifying Handwritten MNIST Images
"""
# standard libraries
import logging
# third party libraries
from opendeep.log import config_root_logger
from opendeep.models import Prototype, Dense, SoftmaxLayer
from opendeep.optimization import SGD
from opendeep.data import MNIST

# grab a log to output useful info
config_root_logger()
log = logging.getLogger(__name__)

def sequential_add_layers():
    # This method is to demonstrate adding layers one-by-one to a Prototype container.
    # As you can see, inputs_hook are created automatically by Prototype so we don't need to specify!
    mlp = Prototype()
    mlp.add(Dense(input_size=28*28, output_size=1000, activation='rectifier', noise='dropout', noise_level=0.5))
    mlp.add(Dense(output_size=512, activation='rectifier', noise='dropout', noise_level=0.5))
    mlp.add(SoftmaxLayer(output_size=10))

    return mlp

def add_list_layers():
    # You can also add lists of layers at a time (or as initialization) to a Prototype! This lets you specify
    # more complex interactions between layers!
    hidden1 = Dense(input_size=28*28,
                         output_size=512,
                         activation='rectifier',
                         noise='dropout')

    hidden2 = Dense(inputs_hook=(512, hidden1.get_outputs()),
                         output_size=512,
                         activation='rectifier',
                         noise='dropout')

    class_layer = SoftmaxLayer(inputs_hook=(512, hidden2.get_outputs()),
                               output_size=10)

    mlp = Prototype([hidden1, hidden2, class_layer])
    return mlp


if __name__ == '__main__':
    mlp = sequential_add_layers()
    data = MNIST(concat_train_valid=True)
    print data.train_inputs.shape
    print data.valid_inputs.shape
    print data.test_inputs.shape
    optimizer = SGD(model=mlp,
                    dataset=data,
                    epochs=500,
                    batch_size=600,
                    learning_rate=.01,
                    momentum=.9,
                    nesterov_momentum=True)
    optimizer.train()
