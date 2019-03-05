import os
import sys
import getpass
import datetime

class Tplates(object):
    _projs_dir = ''
    _my_path = ''

    _def_logb_template = ''
    _def_meta_yaml = ''

    _def_proj_template = ''
    _def_proj_yaml = ''

    _def_subj_template = ''
    # the yaml content is already inside the subject file as a header

    def __init__(self,config):
        self._my_path = os.path.dirname(__file__)
        self._projs_dir = config.projsDir()

    # def logb_template(self,path):
    #     return self._try_file_after_default(path,self._my_path+'/logbuch.template.tex')
    def logb_template(self):
        return self._try_path(self._projs_dir+'/.logbuch.template',
            self._my_path+'/logbuch.template.tex')

    # def meta_yaml(self,path):
    #     return self._try_file_after_default(path,self._my_path+'/meta.yaml')
    def meta_yaml(self):
        path = self._projs_dir+'/.meta.yaml'
        pathdef = self._my_path+'/meta.yaml'
        if path == self._try_path(path,pathdef):
            return path
        else:
            cnt = self._read_file(pathdef)%(SafeDict(
                title='Logbuch',
                subtitle='Research/Academy life notes',
                author='['+getpass.getuser()+']',
                date=datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
            ))
            self._write_file(path,cnt)
            return path

    # def proj_template(self,path):
    #     return self._try_file_after_default(path,self._my_path+'/proj.template.tex')
    def proj_template(self):
        return self._try_path(self._projs_dir+'/.proj.template',
            self._my_path+'/proj.template.tex')

    # def proj_yaml(self,path):
    #     return self._try_file_after_default(path,self._my_path+'/proj.yaml')
    def proj_yaml(self,proj):
        path = self._projs_dir+'/'+proj+'/.proj.yaml'
        pathdef = self._my_path+'/proj.yaml'
        if path == self._try_path(path,pathdef):
            return path
        else:
            cnt = self._read_file(pathdef)%(SafeDict(
                title=self._headarise(proj),
                subtitle='',
                authors='['+getpass.getuser()+']',
                date=''
            ))
            self._write_file(path,cnt)
            return path

    # def subj_template(self,path):
    #     return self._try_file_after_default(path,self._my_path+'/subj.template.tex')
    def subj_template(self):
        return self._try_path(self._projs_dir+'/.subj.template',
            self._my_path+'/subj.template.tex')

    def _try_file_after_default(self,path,pathdef):
        try:
            if os.path.exists(path):
                return self._read_file(path)
            elif os.path.exists(pathdef):
                return self._read_file(pathdef)
            else:
                raise Exception('No default template found!')
        except Exception as e:
            print(repr(e))
            return None

    def _read_file(self,path):
        with open(path,'r') as f:
            return f.read()
        return None

    def _write_file(self,path,s):
        with open(path,'w') as f:
            f.write(s)

    def _try_path(self,path,pathdef):
        try:
            if os.path.exists(path):
                return path
            elif os.path.exists(pathdef):
                return pathdef
            else:
                raise Exception('No default template found!')
        except Exception as e:
            print(repr(e))
            return None

    def _headarise(self,s):
        return ' '.join(s.capitalize().split('_'))

class SafeDict(dict):
    def __missing__(self, key):
        return '%(' + key + ')s'
