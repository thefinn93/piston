from sh import git
__version__ = git("describe", "--always", "--dirty= (dirty)")
