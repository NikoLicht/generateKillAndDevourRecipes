from textgenrnn import textgenrnn
textgen = textgenrnn(weights_path='KillAndDevour_weights.hdf5',
                       vocab_path='KillAndDevour_vocab.json',
                       config_path='KillAndDevour_config.json')
 
textgen.generate_samples(max_gen_length=1)
textgen.generate_to_file('textgenrnn_texts.txt', max_gen_length=1)


