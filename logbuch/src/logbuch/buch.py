import os
import subprocess
from .topic import Topic

def buch(subject,conf):
    topic = Topic(subject,conf)

    # running the text editor
    subprocess.run([conf.editor(), topic.path()])

    topic.close()
