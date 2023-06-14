# author:    Vijay Yadav
# website:   http://www.bklynhlth.com

# import the required packages
import os
import json
import logging
from openwillis.measures.audio.util import transcribe_util as tutil

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger()

def get_config():
    """
    ------------------------------------------------------------------------------------------------------

    Load the configuration settings for the speech transcription.

    Parameters:
    ...........
    None

    Returns:
    ...........
    measures : dict
        A dictionary containing the configuration settings.

    ------------------------------------------------------------------------------------------------------
    """
    #Loading json config
    dir_name = os.path.dirname(os.path.abspath(__file__))
    measure_path = os.path.abspath(os.path.join(dir_name, 'config/speech.json'))

    file = open(measure_path)
    measures = json.load(file)
    return measures

def read_kwargs(kwargs):
    """
    ------------------------------------------------------------------------------------------------------

    Reads keyword arguments and returns a dictionary containing input parameters.

    Parameters:
    ...........
    kwargs : dict
        Keyword arguments to be processed.

    Returns:
    ...........
    input_param: dict A dictionary containing input parameters with their corresponding values.

    ------------------------------------------------------------------------------------------------------
    """
    input_param = {}
    input_param['model'] = kwargs.get('model', 'pyannote')
    input_param['language'] = kwargs.get('language', 'en-US')
    input_param['region'] = kwargs.get('region', 'us-east-1')

    input_param['job_name'] = kwargs.get('job_name', 'transcribe_job_01')
    input_param['ShowSpeakerLabels'] = kwargs.get('ShowSpeakerLabels', True)
    input_param['MaxSpeakerLabels'] = kwargs.get('MaxSpeakerLabels', 2)

    input_param['c_scale'] = kwargs.get('c_scale', '')
    input_param['access_key'] = kwargs.get('access_key', '')
    input_param['secret_key'] = kwargs.get('secret_key', '')
    return input_param

def speech_transcription_cloud(filepath, **kwargs):
    """
    ------------------------------------------------------------------------------------------------------

    Speech transcription function that transcribes an audio file using Amazon Transcribe.

    Parameters:
    ...........
    filepath : str
        The S3 uri for the recording to be transcribed.
    kwargs: Object
        model : str, optional
            The transcription model to use ('aws'). Default is 'aws'.
        language : str, optional
            The language of the audio file (e.g. 'en-US', 'en-IN'). Default is 'en-US'.
        region : str, optional
            The AWS region to use (e.g. 'us-east-1'). Only applicable if model is 'aws'. Default is 'us-east-1'.
        job_name : str, optional
            The name of the transcription job. Only applicable if model is 'aws'. Default is 'transcribe_job_01'.
        ShowSpeakerLabels : boolean, optional
            Show speaker labels
        MaxSpeakerLabels : int, optional
            Max number of speakers
        c_scale : str, optional
            Clinical scale to use for slicing the separated audio files, if any.
        access_key : str, optional
            AWS access key
        secret_key : str, optional
            AWS secret key


    Returns:
    ...........
    json_response : JSON Object
        A transcription response object in JSON format
    transcript : str
        The transcript of the recording.

    ------------------------------------------------------------------------------------------------------
    """
    input_param = read_kwargs(kwargs)
    measures = get_config()
    json_response, transcript = tutil.transcribe_audio(filepath, input_param)

    if input_param['ShowSpeakerLabels'] == True and input_param['c_scale']:
        content_dict = tutil.extract_content(json_response)
        json_response = tutil.get_clinical_labels(input_param['c_scale'], measures, content_dict, json_response)

    return json_response, transcript
