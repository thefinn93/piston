class ConfigurationException(Exception):
    """A given configuration file is invalid."""

    def __str__(self):
        return self.args[0]


class ConfigurationMissingKeysException(ConfigurationException):
    """The provided config is missing required keys."""

    pass


class InsecureRedirectException(ConfigurationException):
    """The provided redirect URL is not over https."""

    pass
