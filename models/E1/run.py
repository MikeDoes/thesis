# Attempt 1 with GPT-2 simple
#https://github.com/minimaxir/gpt-2-simple


import gpt_2_simple as gpt2
from datetime import datetime
from google.colab import files

gpt2.download_gpt2(model_name="124M")

gpt2.mount_gdrive()
file_name = "training.txt"
gpt2.copy_file_from_gdrive(file_name)

print("Training the model:")
sess = gpt2.start_tf_sess()

gpt2.finetune(sess,
              dataset=file_name,
              model_name='124M',
              steps=1000,
              restore_from='fresh',
              run_name='run1',
              print_every=100,
              sample_every=200,
              save_every=500
              )