import os


cmds = '''
git pull
git add -A
git commit -am "cool"
git push
'''
cmds = [cmd for cmd in cmds.split('\n') if cmd != '']

for cmd in cmds:
  print(cmd)
  os.system(cmd)