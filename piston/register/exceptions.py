class ConfigurationException(Exception):
    """A given configuration file is invalid."""

    pass


class InsecureConfigSchemeException(ConfigurationException):
    """The provided config URL is not over https."""

    pass


class ConfigurationMissingKeysException(ConfigurationException):
    """The provided config URL is missing required keys."""

    pass


class InsecureRedirectException(ConfigurationException):
    """The provided redirect URL is not over https."""

    pass


class DomainMismatchException(ConfigurationException):
    """The provided config URL and the redirect URL do not share a domain."""

    pass
