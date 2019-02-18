import os
import subprocess
from .topic import Topic

def buch(subject):
    topic = Topic(subject)

    # running the text editor
    editor = os.environ['EDITOR'] if 'EDITOR' in os.environ else 'vi'
    subprocess.run([editor, topic.path()])

    topic.close()
