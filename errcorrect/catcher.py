# -*- coding: utf-8 -*-

from b3j0f.conf import Configurable, Category, Parameter
from b3j0f.utils.path import lookup
from six import string_types

from errcorrect.exception import extract_exception_info


@Configurable(
    paths='pyerrors/catcher.conf',
    conf=Category(
        'CATCHER',
        Parameter('exception_processing', parser=lookup)
    )
)
class ExceptionCatcher(object):
    """
    Catch exception, extract informations from traceback and process it.

    Usage:

        try:
            # code that raise an error

        except Exception:
            with ExceptionCatcher() as catcher:
                catcher.process()
    """

    @property
    def exception_processing(self):
        if not hasattr(self, '_exception_processing'):
            self.exception_processing = None

        return self._exception_processing

    @exception_processing.setter
    def exception_processing(self, value):
        if value is None:
            value = exception_processing

        if isinstance(value, string_types):
            value = lookup(value)

        self._exception_processing = value

    @property
    def exc_info(self):
        return self._exc_info

    def __init__(self, exception_processing=None, *args, **kwargs):
        """
        :param exception_processing: exception processing handler (optional)
        :type exception_processing: callable or str
        """

        super(ExceptionCatcher, self).__init__(*args, **kwargs)

        if exception_processing is not None:
            self.exception_processing = exception_processing

        self._exc_info = extract_exception_info()

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def process(self):
        """
        Extract information from exception, and process it.
        """

        self.exception_processing(
            catcher=self,
            exc_info=self.exc_info
        )


def exception_processing(catcher, exc_info, **_):
    """
    exception_processing prototype.

    :param catcher: caller instance of ExceptionCatcher
    :type catcher: ExceptionCatcher

    :param exc_info: information as returned by ``extract_exception_info``
    :type exc_info: dict
    """

    pass
