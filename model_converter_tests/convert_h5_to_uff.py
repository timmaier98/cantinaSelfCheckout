import tensorflow as tf
import tensorflow.python.keras.backend as K

#from tensorflow.python.framework import graph_io


'''def keras_to_frozen_pb(model_in_path,
                       model_out_path,
                       custom_object_dict=None,
                       tensor_out_name=None,
                       tensorboard_dir=None):
    """
    Converter that transforms keras model to frozen pb model

    Args:
        model_in_path (str): Input model path (.h5)
        model_out_path (str): Output model path (dir)
        tensor_out_name (str, optional): Specified name of output tensor.
                                         If None, it will get default tensor name from keras model.
                                         Defaults to None.
        tensorboard_dir (str, optional): Output tensorboard dir path for inspecting output model graph.
                                         If None, it doesn't generate.
                                         Defaults to None.
    """

    graph = tf.Graph()
    with graph.as_default():
        sess = tf.compat.v1.Session()
        K.set_session(sess)
        K.set_learning_phase(0)

        # load the model to graph and sess
        model = tf.keras.models.load_model(model_in_path, custom_objects=custom_object_dict)

        # get the tensor_out_name
        if tensor_out_name is None:
            if len(model.outputs) > 1:
                raise NameError("the model has multiple output tensor. Need to specify output tensor name.")
            else:
                tensor_out_name = model.outputs[0].name.split(":")[0]

        # freeze the graph
        graphdef = tf.compat.v1.graph_util.convert_variables_to_constants(sess, graph.as_graph_def(), [tensor_out_name])
        graphdef = tf.compat.v1.graph_util.remove_training_nodes(graphdef)
        graph_io.write_graph(graphdef, './', model_out_path, as_text=False)

    # output tensorboard graph
    if not tensorboard_dir is None:
        tf.compat.v1.summary.FileWriter(logdir=tensorboard_dir, graph_def=graphdef)

    return tensor_out_name

input_keras_model = "C:\\Users\\Lars\\PycharmProjects\\cantinaSelfCheckout\\trained_models_archive\\own_data_with_none_class.h5"
output_pb_model = "C:\\Users\\Lars\\PycharmProjects\\cantinaSelfCheckout\\trained_models_archive\\own_model_with_none_class.pb"

import uff
import tensorrt as trt
import tensorflow as tf

def frozen_pb_to_plan(model_path,
                      output_path,
                      tensor_in_name,
                      tensor_out_name,
                      input_size,
                      data_type=trt.float32,
                      max_batch_size=1,
                      max_workspace=1 << 30,
                      tensorboard_dir=None):
    # infer with pb model
    graph_def = tf.GraphDef()
    with tf.io.gfile.GFile(model_path, "rb") as f:
        graph_def.ParseFromString(f.read())

    # convert TF frozen graph to uff model
    uff_model = uff.from_tensorflow_frozen_model(model_path, [tensor_out_name])

    # create uff parser
    parser = trt.UffParser()
    parser.register_input(tensor_in_name, input_size)
    parser.register_output(tensor_out_name)

    # create trt logger and builder
    trt_logger = trt.Logger(trt.Logger.INFO)
    builder = trt.Builder(trt_logger)
    builder.max_batch_size = max_batch_size
    builder.max_workspace_size = max_workspace
    builder.fp16_mode = (data_type == trt.float16)

    # parse the uff model to trt builder
    network = builder.create_network()
    parser.parse_buffer(uff_model, network)

    # build optimized inference engine
    engine = builder.build_cuda_engine(network)

    # save inference engine
    with open(output_path, "wb") as f:
        f.write(engine.serialize())

# step 1: convert keras model to frozen pb model
# if __name__ == "__main__":
#     node_out_name = keras_to_frozen_pb(input_keras_model, output_pb_model)
#     print("the output node name is:", node_out_name)

BATCH_SIZE = 1
H, W, C = 299, 299, 3

# step 2: convert frozen pb model to trt plan
if __name__ == "__main__":
    '''
    generate the inference engine 
    '''
    pb_model_path = "C:\\Users\\Lars\\PycharmProjects\\cantinaSelfCheckout\\trained_models_archive\\own_model_with_none_class.pb"
    plan_model_path = "C:\\Users\\Lars\\PycharmProjects\\cantinaSelfCheckout\\trained_models_archive\\own_model_with_none_class.plan"
    input_node_name = "input_1"
    output_node_name = "predictions/Softmax"

    frozen_pb_to_plan(pb_model_path,
                      plan_model_path,
                      input_node_name,
                      output_node_name,
                      [C, H, W],
                      data_type=trt.float32, # change this for different TRT precision
                      max_batch_size=1,
                      max_workspace=1<<30)