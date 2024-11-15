# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Train a MixIT separation model on FUSS using tf.estimator."""


import argparse
import os
import sys

import tensorflow.compat.v1 as tf

import model
cur_path = os.path.dirname(os.path.realpath(__file__))
parent_path = os.path.dirname(os.path.dirname(os.path.dirname(cur_path)))
sys.path.append(os.path.join(parent_path))
from train import data_io
from train import train_with_estimator


def main():
  tf.logging.set_verbosity(tf.logging.INFO)
  parser = argparse.ArgumentParser(
      description='Train the MixIT separation model on FUSS.')
  parser.add_argument(
      '-dd', '--data_dir', help='Data directory.',
      required=True)
  parser.add_argument(
      '-md', '--model_dir', help='Directory for checkpoints and summaries.',
      required=True)
  args = parser.parse_args()

  hparams = model.get_model_hparams()
  hparams.sr = 16000.0

  print("SIGNALS: ", len(hparams.signal_names))

  roomsim_params = {
      'num_sources': len(hparams.signal_names),
      'num_receivers': 1,
      'num_samples': int(hparams.sr * 10.0),
  }
  tf.logging.info('Params: %s', roomsim_params.values())

  feature_spec = data_io.get_roomsim_spec(**roomsim_params)
  inference_spec = data_io.get_inference_spec()

  train_list = os.path.join(args.data_dir, 'train_example_list.txt')
  validation_list = os.path.join(args.data_dir, 'validation_example_list.txt')

  params = {
      'feature_spec': feature_spec,
      'inference_spec': inference_spec,
      'hparams': hparams,
      'io_params': {'parallel_readers': 512,
                    'num_samples': int(hparams.sr * 10.0)},
      'input_data_train': train_list,
      'input_data_eval': validation_list,
      'model_dir': args.model_dir,
      # Effective batch size of 3, since batches split in half to create MoMs.
      'train_batch_size': 2 * 3,
      'eval_batch_size': 2 * 3,
      'train_steps': 20000000,
      'eval_suffix': 'validation',
      'eval_examples': 800,
      'save_checkpoints_secs': 600,
      'save_summary_steps': 1000,
      'keep_checkpoint_every_n_hours': 4,
      'write_inference_graph': True,
      'randomize_training': True,
  }
  tf.logging.info(params)
  params['input_data_train'] = data_io.read_lines_from_file(
      params['input_data_train'], skip_fields=1)
  params['input_data_eval'] = data_io.read_lines_from_file(
      params['input_data_eval'], skip_fields=1)
  train_with_estimator.execute(model.model_fn, data_io.input_fn, **params)


if __name__ == '__main__':
  main()
