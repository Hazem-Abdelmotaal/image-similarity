from keras.models import Model
from keras.layers import Flatten, Dense, Input, Lambda
from keras.applications.vgg16 import VGG16
from keras import backend as K


def vgg16_features(input_shape):
    """ Extract feature vector from image using pre-trained vgg16
    """
    base_model = VGG16(
        weights='imagenet', include_top=False, input_shape=input_shape)

    x = base_model.output
    x = Flatten(name='flatten')(x)
    x = Dense(512, activation='relu', name='fc1')(x)
    features = Dense(512, activation='relu', name='fc2')(x)

    for layer in base_model.layers:
        layer.trainable = False

    return Model(inputs=base_model.input, outputs=features)


def euclidean_distance(vects):
    """ Compute euclidean distance between two vectors
    """
    x, y = vects
    return K.sqrt(
        K.maximum(K.sum(K.square(x - y), axis=1, keepdims=True), K.epsilon()))


def eucl_dist_output_shape(shapes):
    shape_1, _ = shapes
    return(shape_1[0], 1)


def vgg16_siamese(input_shape):
    """ Compute distance between image pairs
    """
    features_network = vgg16_features(input_shape)

    input_a = Input(shape=input_shape)
    input_b = Input(shape=input_shape)

    features_a = features_network(input_a)
    features_b = features_network(input_b)

    distance = Lambda(euclidean_distance, output_shape=eucl_dist_output_shape)

    return Model([input_a, input_b], distance([features_a, features_b]))


# loss functions
def contrastive_loss(y_true, y_pred):
    margin = 1
    return K.mean(y_true * K.square(y_pred) +
                  (1 - y_true) * K.square(K.maximum(margin - y_pred, 0)))
