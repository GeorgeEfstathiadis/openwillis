# author:    Georgios Efstathiadis
# website:   http://www.bklynhlth.com

# import the required packages
from multiprocessing import Pool

from transformers import AutoTokenizer, AutoModelForCausalLM

from openwillis.measures.text.util.diarization_utils import (
    exponential_backoff_decorator, preprocess_str, apply_formatting
)


@exponential_backoff_decorator(max_retries=3, base_delay=90)
def process_chunk_hf(args):
    """
    ------------------------------------------------------------------------------------------------------

    This function processes a diarized text chunk using the HuggingFace model;
     it is used for parallel processing.

    Parameters:
    ...........
    args: tuple
        Tuple of arguments.
        idx: int, chunk index.
        prompt: str, diarized text chunk.
        input_param: dict, additional arguments for the HF model.

    Returns:
    ...........
    tuple: Tuple of chunk index and model output.

    ------------------------------------------------------------------------------------------------------
    """
    idx, prompt, input_param = args

    if input_param['quantized']:
        # load quantized model from HuggingFace
        tokenizer = AutoTokenizer.from_pretrained("bklynhlth/WillisDiarize-GPTQ")
        model = AutoModelForCausalLM.from_pretrained("bklynhlth/WillisDiarize-GPTQ")
    else:
        # load model from HuggingFace
        tokenizer = AutoTokenizer.from_pretrained("bklynhlth/WillisDiarize")
        model = AutoModelForCausalLM.from_pretrained("bklynhlth/WillisDiarize")

    input_data = apply_formatting(preprocess_str(prompt))

    # Tokenize the input data
    inputs = tokenizer(input_data["inputs"], return_tensors="pt")

    # Generate the output
    output = model.generate(
        **inputs,
        max_length=2048,
        top_p=0.5,
        temperature=0.2,
        stop_token="</s>",
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.pad_token_id,
        return_dict_in_generate=True
    )

    # Decode the output
    result = tokenizer.decode(output["sequences"][0], skip_special_tokens=True)

    return idx, result


def call_diarization_hf(prompts, endpoint_name, input_param):
    """
    ------------------------------------------------------------------------------------------------------

    This function calls the speaker diarization model.

    Parameters:
    ...........
    prompts: dict
        Dictionary of diarized text chunks.
        key: chunk index, value: diarized text chunk.
    endpoint_name: str
        Name of the SageMaker endpoint.
    input_param: dict
        Additional arguments for the API call.

    Returns:
    ...........
    results: dict
        Dictionary of model outputs.
        key: chunk index, value: model output.

    ------------------------------------------------------------------------------------------------------
    """

    results = {}
    if input_param['parallel_processing'] == 1:
        with Pool(processes=len(prompts)) as pool:
            args = [(idx, prompts[idx], input_param, endpoint_name) for idx in sorted(prompts.keys())]
            results = pool.map(process_chunk_hf, args)
            results = dict(results)
    else:
        for idx in sorted(prompts.keys()):
            results[idx] = process_chunk_hf((idx, prompts[idx], input_param, endpoint_name))[1]

    return results
