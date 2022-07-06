import tensorflow_hub as hub

# def process_to_IDs_in_sparse_format(sp, sentences):
#   # An utility method that processes sentences with the sentence piece processor
#   # 'sp' and returns the results in tf.SparseTensor-similar format:
#   # (values, indices, dense_shape)
#   ids = [sp.EncodeAsIds(x) for x in sentences]
#   max_len = max(len(x) for x in ids)
#   dense_shape = (len(ids), max_len)
#   values = [item for sublist in ids for item in sublist]
#   indices = [[row, col]
#              for row in range(len(ids)) for col in range(len(ids[row]))]
#   return (values, indices, dense_shape)


def test():
    embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder-large/5")


    embeddings = embed([
    "The quick brown fox jumps over the lazy dog.",
    "I am a sentence for which I would like to get its embedding"])

    print(embeddings)
