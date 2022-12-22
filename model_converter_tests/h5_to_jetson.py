# import tensorflow as tf
# from tensorflow.python.framework import graph_io
# from tensorflow.keras.models import load_model
# import tensorflow.python.keras.backend as K
#
#
#
# # Clear any previous session.
# tf.keras.backend.clear_session()
#
# save_pb_dir = 'trained_models'
# model_fname = 'trained_models/own_data_with_none_class.h5'
# def freeze_graph(graph, session, output, save_pb_dir='.', save_pb_name='frozen_model.pb', save_pb_as_text=False):
#     with graph.as_default():
#         # graphdef_inf = tf.graph_util.remove_training_nodes(graph.as_graph_def())
#         graphdef_inf = tf.compat.v1.graph_util.remove_training_nodes(graph.as_graph_def())
#         # graphdef_frozen = tf.graph_util.convert_variables_to_constants(session, graphdef_inf, output)
#         graphdef_frozen = tf.compat.v1.graph_util.convert_variables_to_constants(session, graphdef_inf, output)
#         graph_io.write_graph(graphdef_frozen, save_pb_dir, save_pb_name, as_text=save_pb_as_text)
#         return graphdef_frozen
#
# # This line must be executed before loading Keras model.
# tf.keras.backend.set_learning_phase(0)
#
# model = load_model(model_fname)
#
# session = K.get_session()
#
# input_names = [t.op.name for t in model.inputs]
# output_names = [t.op.name for t in model.outputs]
#
# # input_names = ["input_11"]
# # output_names = ["dense_4/Softmax"]
#
# # input_names = model.input_names
# # output_names = model.output_names
#
# # Prints input and output nodes names, take notes of them.
# print(input_names, output_names)
#
# frozen_graph = freeze_graph(session.graph, session, output_names, save_pb_dir=save_pb_dir)
#
#
#
# import tensorflow.contrib.tensorrt as trt
#
# trt_graph = trt.create_inference_graph(
#     input_graph_def=frozen_graph,
#     outputs=output_names,
#     max_batch_size=1,
#     max_workspace_size_bytes=1 << 25,
#     precision_mode='FP16',
#     minimum_segment_size=50
# )
#
# graph_io.write_graph(trt_graph, "./model/",
#                      "trt_graph.pb", as_text=False)





# import os
# import numpy as np
# import tensorflow as tf
# from google import protobuf
# from tensorflow.python.compiler.tensorrt import trt_convert as trt
#
# print("Tensorflow version: ", tf.version.VERSION)
# print("Protobuf version:", protobuf.__version__)
# print("TensorRT version: ")
# print(os.system("dpkg -l | grep TensorRT"))
#
# gpu_devices = tf.config.experimental.list_physical_devices('GPU')
# tf.config.experimental.set_memory_growth(gpu_devices[0], True)
# tf.config.experimental.set_virtual_device_configuration(
#             gpu_devices[0],
#             [tf.config.experimental.VirtualDeviceConfiguration(
#                memory_limit=1024)]) ## Crucial value, set lower than available GPU memory (note that Jetson shares GPU memory with CPU), should be 2048
#
# conversion_params = trt.DEFAULT_TRT_CONVERSION_PARAMS
# conversion_params = conversion_params._replace(max_workspace_size_bytes=(1<<30))
# conversion_params = conversion_params._replace(precision_mode="FP16")
# conversion_params = conversion_params._replace(maximum_cached_engines=10)
# conversion_params = conversion_params._replace(use_calibration=True)
# converter = trt.TrtGraphConverterV2(
#     input_saved_model_dir="./trained_model/saved_model",
#     conversion_params=conversion_params)
# converter.convert()
#
# batch_size = 1
# def input_fn():
#     # Substitute with your input size
#     Inp1 = np.random.normal(size=(batch_size, 1024, 1024, 3)).astype(np.uint8)
#     yield (Inp1, )
# converter.build(input_fn=input_fn)
#
# converter.save("./trained_model/saved_model_compressed_int8")



# import tensorflow as tf
# from tensorflow.python.framework import graph_io
# from tensorflow.keras.models import load_model
#
#
# # Clear any previous session.
# tf.keras.backend.clear_session()
#
# save_pb_dir = './model'
# model_fname = './model/model.h5'
# def freeze_graph(graph, session, output, save_pb_dir='.', save_pb_name='frozen_model.pb', save_pb_as_text=False):
#     with graph.as_default():
#         graphdef_inf = tf.graph_util.remove_training_nodes(graph.as_graph_def())
#         graphdef_frozen = tf.graph_util.convert_variables_to_constants(session, graphdef_inf, output)
#         graph_io.write_graph(graphdef_frozen, save_pb_dir, save_pb_name, as_text=save_pb_as_text)
#         return graphdef_frozen
#
# # This line must be executed before loading Keras model.
# tf.keras.backend.set_learning_phase(0)
#
# model = load_model(model_fname)
#
# session = tf.keras.backend.get_session()
#
# input_names = [t.op.name for t in model.inputs]
# output_names = [t.op.name for t in model.outputs]
#
# # Prints input and output nodes names, take notes of them.
# print(input_names, output_names)
#
# frozen_graph = freeze_graph(session.graph, session, [out.op.name for out in model.outputs], save_pb_dir=save_pb_dir)
#
# import tensorflow.contrib.tensorrt as trt
#
# trt_graph = trt.create_inference_graph(
#     input_graph_def=frozen_graph,
#     outputs=output_names,
#     max_batch_size=1,
#     max_workspace_size_bytes=1 << 25,
#     precision_mode='FP16',
#     minimum_segment_size=50
# )
#
# graph_io.write_graph(trt_graph, "./model/",
#                      "trt_graph.pb", as_text=False)

from tensorflow.python.compiler.tensorrt import trt_convert as trt

# import tensorflow as tf
#
# input_saved_model_dir = 'trained_models/own_data_with_none_class.h5'
# output_saved_model_dir = "my_model.engine"
#
# converter = tf.experimental.tensorrt.Converter(input_saved_model_dir=input_saved_model_dir)
# converter.convert()
# converter.save(output_saved_model_dir)
#
# # RuntimeError: Tensorflow has not been built with TensorRT support.

#https://forums.developer.nvidia.com/t/keras-pb-model-to-tensorrt-engine-conversion/191242