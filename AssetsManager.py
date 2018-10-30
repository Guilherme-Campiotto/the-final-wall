#coding: utf-8

import os
import pygame

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

class Asset(object):
    def __init__(self, path):
        dname = os.path.dirname(path)
        fname = os.path.basename(path)
        self.path = os.path.join(dname, fname)
        self.data = None

class Manager(object):
    assets = {}

    @classmethod
    def init(cls):
        path = os.path.join(ROOT_PATH, cls.folder)
        os.path.walk(path, cls.__scan, None)

    @classmethod
    def __scan(cls, arg, dirname, fnames):
        for fname in fnames:
            if not fname:
                continue
            path = os.path.join(dirname, fname)
            cls.assets[path] = Asset(path)
            print path

    @classmethod
    def get(cls, name, *args):
        path = os.path.join(cls.folder, name)
        path = os.path.abspath(path)
        asset = cls.assets[path]
        #if asset.data is None:
        asset.data = cls.load(asset.path, *args)
        return asset.data

    @classmethod
    def dispose(cls, name):
        del cls.assets[name].data


class Fonts(Manager):
    folder = 'Fontes'

    @classmethod
    def load(cls, path, *args):
        return pygame.font.Font(path, *args)

class Images(Manager):
    folder = 'Images'

    @classmethod
    def load(cls, path):
        return pygame.image.load(path)
    
class Sounds(Manager):
    folder = 'Sounds'

    @classmethod
    def load(cls, path):
        return pygame.mixer.Sound(path)
