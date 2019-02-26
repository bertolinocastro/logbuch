from .md2tex import Md2Tex

def make(conf,proj):

    # TODO: ---v
    # converting each markdown file contents to latex ones
    # and storing it in memory
    # Afterall, create the main latex file to import annd sections and images and
    # then compile it

    texFile = Md2Tex(conf,proj)
    texFile.writeContents()
    # texFile.editContents()
    texFile.compile()
