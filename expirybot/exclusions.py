import logging
import re

from .config import config

LOG = logging.getLogger(__name__)

RSA = 1
DSA = 17
ECDSA = 19
ECC = 18


def is_strong_key(key):
    if key.algorithm_number == RSA:
        return key.size_bits >= 2048

    elif key.algorithm_number == DSA:
        return key.size_bits >= 2048

    elif key.algorithm_number == ECDSA:
        LOG.warn("Returning 'strong' for ECDSA key size {}".format(
            key.size_bits
            )
        )
        return True

    elif key.algorithm_number == ECC:
        return key.size_bits >= 256

    else:
        LOG.warn("Unknown key algorithm / size: {} {}".format(
            key.algorithm_number, key.size_bits
            )
        )
        return False


def no_valid_emails(key):
    missing_email = not key.email_lines
    return missing_email


def all_blacklisted_domains(key):
    if no_valid_emails(key):
        return False

    def get_domain(email):
        _, domain = email.split('@', 1)
        return domain

    return all(is_blacklisted(get_domain(e)) for e in key.emails)


def is_blacklisted(domain):
    return domain.lower() in config.blacklisted_domains


def roughly_validate_email(email):
    try:
        (_, hostname) = email.split('@', 1)
    except ValueError:
        return False

    return roughly_validate_hostname(hostname)


def roughly_validate_hostname(hostname):
    if len(hostname) > 255:
        return False

    if hostname[-1] == ".":
        hostname = hostname[:-1]  # strip exactly 0 or 1 dot from the right

    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)

    parts = hostname.split(".")

    if not parts:
        return False

    if parts[-1] == 'onion':
        return False

    return all(allowed.match(x) for x in parts)
