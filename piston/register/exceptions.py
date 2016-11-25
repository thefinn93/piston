from piston.exceptions import PistonException


class ConfigurationException(PistonException):
    """A given configuration file is invalid."""
    pass


class ConfigurationMissingKeysException(ConfigurationException):
    """The provided config is missing required keys."""

    pass


class InsecureRedirectException(ConfigurationException):
    """The provided redirect URL is not over https."""

    pass
