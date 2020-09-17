import gpt_2_simple as gpt2

TRAIN = True
model = '355M'
run_name = 'master'

#gpt2.download_gpt2(model_name="355M")
file_name = "master.csv"
gen_file = "output.txt"
sess = gpt2.start_tf_sess()
if TRAIN:
    gpt2.finetune(sess,
                 dataset=file_name,
                 model_name=model,
                 steps=500,
                 restore_from='fresh',
                 run_name=run_name,
                 print_every=10,
                 sample_every=100)
else:
    gpt2.load_gpt2(sess, run_name=run_name)

# gpt2.generate(sess, run_name=run_name,
#              length=100,
#              prefix="<|startoftext|>",
#              truncate="<|endoftext|>",
#              include_prefix=False)
gpt2.generate_to_file(sess,
                     destination_path=gen_file,
                     length=100,
                     temperature=1.0,
                     nsamples=100,
                     batch_size=20,
                     prefix="<|startoftext|>",
                     truncate="<|endoftext|>",
                     include_prefix=False,
                     sample_delim='',
                     run_name=run_name
                     )