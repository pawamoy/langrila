import base64
import io
from typing import Any, Generator, Iterable

import numpy as np
from PIL import Image


def make_batch(
    iterable: Iterable[Any], batch_size: int = 1, overlap: int = 0
) -> Generator[Iterable[Any], None, None]:
    if overlap >= batch_size:
        raise ValueError("overlap must be less than batch_size")

    length = len(iterable)

    st: int = 0
    while st < length:
        en = min(st + batch_size, length)
        batch = iterable[st:en]
        yield batch

        if en == length:
            break

        st += batch_size - overlap


def pil2bytes(image: Image.Image) -> bytes:
    num_byteio = io.BytesIO()
    image.save(num_byteio, format=image.format.lower())
    image_bytes = num_byteio.getvalue()
    return image_bytes


def image2bytes(image: Image.Image | np.ndarray | bytes) -> bytes:
    if isinstance(image, Image.Image):
        return pil2bytes(image)
    elif isinstance(image, np.ndarray):
        image_pil = Image.fromarray(image)
        return pil2bytes(image_pil)
    elif isinstance(image, bytes):
        return image
    else:
        raise ValueError(f"Type of {type(image)} is not supported for image.")


def base64_encode(data: Any):
    return base64.b64encode(data)


def encode_image(image: Image.Image | np.ndarray | bytes, as_utf8: bool = False) -> str:
    image_bytes = image2bytes(image)
    encoded = base64_encode(image_bytes)

    if as_utf8:
        return encoded.decode("utf-8")
    else:
        return encoded


def decode_image(image_encoded: str, as_utf8: bool = False) -> Image.Image:
    if not as_utf8:
        image_encoded_utf = image_encoded
    else:
        image_encoded_utf = image_encoded.encode("utf-8")

    image_bytes = base64.b64decode(image_encoded_utf)
    byteio = io.BytesIO(image_bytes)
    return Image.open(byteio)
