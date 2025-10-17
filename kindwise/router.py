'''
This module provides the Router class and related utilities for local image classification using Kindwise models.

The Router class loads a pre-trained image classification model from the Hugging Face Hub and provides methodsto
to classify images into predefined classes. It supports multiple model sizes and can run on CPU or CUDA devices.
The module also defines result and configuration structures for classification results.
'''

import enum
import json
from dataclasses import dataclass
from functools import cached_property
from pathlib import PurePath
from typing import BinaryIO

from PIL import Image

from kindwise.core import KindwiseApi
from kindwise.models import Classification

try:
    import numpy as np
    import torch
    import torchvision
    from huggingface_hub import hf_hub_download
except ImportError:
    np = None
    torch = None
    hf_hub_download = None


@dataclass
class RouterResult:
    '''
    Represents the result of a classification performed by the Router.

    Attributes:
        classification (Classification): The classification result containing suggestions.
    '''

    classification: Classification

    @classmethod
    def from_dict(cls, data: dict):
        '''
        Create a RouterResult instance from a dictionary.

        Args:
            data (dict): Dictionary containing classification data.
        Returns:
            RouterResult: The created RouterResult instance.
        '''
        return cls(
            classification=Classification.from_dict(data['classification']),
        )

    @cached_property
    def simple(self) -> dict[str, float]:
        '''
        Returns a simplified dictionary mapping class names to probabilities.

        Returns:
            dict[str, float]: Mapping from class name to probability.
        '''
        return {suggestion.name: suggestion.probability for suggestion in self.classification.suggestions}


class RouterSize(str, enum.Enum):
    '''
    Enum representing available model sizes for the Router.
    '''

    TINY = 'tiny'
    SMALL = 'small'
    BASE = 'base'


class Router:
    '''
    Router for local image classification using Kindwise models.

    Loads a pre-trained model from the Hugging Face Hub and provides methods to classify images into predefined classes.
    Supports multiple model sizes and device selection (CPU or CUDA).
    '''

    def __init__(self, size: RouterSize = RouterSize.BASE, device: str = 'cuda'):
        '''
        Initialize the Router.

        Args:
            size (RouterSize): The model size to use (tiny, small, base).
            device (str): The device to use for inference ('cuda' or 'cpu').
        '''
        assert np is not None, 'Please install numpy to use the kindwise.router.Router.'
        assert torch is not None, 'Please install torch to use the kindwise.router.Router.'
        assert torchvision is not None, 'Please install torchvision to use the kindwise.router.Router.'
        assert hf_hub_download is not None, 'Please install huggingface_hub to use the kindwise.router.Router.'
        self.size = size
        self._device = device

    @cached_property
    def device(self) -> str:
        '''
        Returns the torch device to use for inference.

        Returns:
            str: The device ('cuda' or 'cpu').
        '''
        if self._device == 'cuda':
            return torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        return self._device

    @cached_property
    def config(self) -> dict:
        '''
        Loads and returns the model configuration from the Hugging Face Hub.

        Returns:
            dict: The model configuration.
        '''
        config_path = hf_hub_download(
            repo_id=f'kindwise/router.{self.size.value}',
            filename='config.json',
        )
        with open(config_path, 'r') as f:
            return json.load(f)

    @cached_property
    def classes(self) -> list[str]:
        '''
        Loads and returns the list of class names from the Hugging Face Hub.

        Returns:
            list[str]: List of class names.
        '''
        classes_path = hf_hub_download(
            repo_id=f'kindwise/router.{self.size.value}',
            filename='classes.txt',
        )
        with open(classes_path, 'r') as f:
            return [line.strip() for line in f.readlines()]

    @cached_property
    def model(self):
        '''
        Loads and returns the pre-trained model from the Hugging Face Hub.

        Returns:
            torch.jit.ScriptModule: The loaded model.
        '''
        model_path = hf_hub_download(
            repo_id=f'kindwise/router.{self.size.value}',
            filename='model.traced.pt',
        )
        return torch.jit.load(model_path).eval().to(self.device)

    def identify(
        self,
        image: PurePath | str | bytes | BinaryIO | Image.Image | list[str | PurePath | bytes | BinaryIO | Image.Image],
        as_dict: bool = False,
    ) -> RouterResult | dict:
        '''
        Classify one or more images and return the classification result.

        Args:
            image: The image(s) to classify. Can be a path, bytes, file-like, PIL Image, or a list of these.
            as_dict (bool): If True, return the result as a dictionary. Otherwise, return a RouterResult.
        Returns:
            RouterResult or dict: The classification result.
        '''
        if not isinstance(image, list):
            image = [image]
        image_buffers = [KindwiseApi._load_image_buffer(img) for img in image]
        images = [Image.open(buf) for buf in image_buffers]
        image_arrays = [self.preprocess_image(im) for im in images]
        image_tensors = [torchvision.transforms.functional.to_tensor(i) for i in image_arrays]
        image_tensors = torch.stack(image_tensors).to(self.device)

        result = {'classification': {'suggestions': []}}
        with torch.no_grad():
            predictions = self.model(image_tensors).detach().cpu().numpy().mean(axis=0)
            del image_tensors
            for i in (-predictions).argsort():
                result['classification']['suggestions'].append(
                    {
                        'id': f'manual:{self.classes[i]}',
                        'name': self.classes[i],
                        'probability': float(predictions[i]),
                    }
                )
        if as_dict:
            return result
        return RouterResult.from_dict(result)

    def preprocess_image(self, image: Image.Image):
        '''
        Preprocess an image for model input: convert to RGB, crop to square, resize, and normalize.

        Args:
            image (Image.Image): The input image.
        Returns:
            np.ndarray: The preprocessed image as a float32 numpy array.
        '''
        if image.mode != 'RGB':
            image = image.convert('RGB')
        width, height = image.size
        if width != height:
            new_size = min(width, height)
            left = (width - new_size) / 2
            top = (height - new_size) / 2
            right = (width + new_size) / 2
            bottom = (height + new_size) / 2
            image = image.crop((left, top, right, bottom))
        image = image.resize((self.config['image_size'], self.config['image_size']))
        return np.array(image).astype(np.float32) / 255.0
