from pathlib import Path

from PIL import GifImagePlugin, Image
import pytest

from project import ascii

@pytest.fixture
def gif_instance():
    filename = 'gifs/nyan-cat.gif'
    instance = ascii.GifAsciiArt(filename)
    return instance


@pytest.fixture
def ascii_art_animation():
    filename = 'veritas.png'
    image = Image.open(Path(__file__).parent / filename)
    instance = ascii.AsciiArt(image)
    return instance


def test_gif_instance_not_exist():
    filename = 'unknown_file.gif'
    with pytest.raises(FileNotFoundError):
        ascii.GifAsciiArt(filename)


def test_instance_class(gif_instance):
    assert isinstance(gif_instance, GifImagePlugin.GifImageFile)
    assert isinstance(gif_instance, ascii.GifAsciiArt)


def test_ascii_frames(gif_instance):
    assert isinstance(gif_instance.ascii_frames, list)
    assert gif_instance.ascii_frames is not None


def test_ascii_art_animation_1(gif_instance):
    for frame in gif_instance.ascii_frames:
        assert isinstance(frame, ascii.AsciiArt)


def test_ascii_art_animation_2(ascii_art_animation):
    assert ascii_art_animation._image



def test_wrongly_formatted_file():
    with pytest.raises(SystemExit):
        filename = 'veritas.png'
        with open(Path(__file__).parent / filename, "rb") as f:
            ascii.get_ascii_gif(f)


def test_valid_file():
    with open("gifs/nyan-cat.gif", 'rb') as f:
        ascii.get_ascii_gif(f)


def test_filename():
    ascii.get_ascii_gif("gifs/nyan-cat.gif")
