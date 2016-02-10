# -*- coding: utf-8 -*-

from errcorrect.disassembler import disassemble
import sys


def frames_from_traceback(traceback):
    """
    Get iterable of frames in traceback.

    :param traceback: traceback to extract frames from
    :type traceback: traceback

    :returns: frames
    :rtype: iterable
    """

    frames = []
    curframe = traceback

    while curframe is not None:
        frames.append(curframe.tb_frame)
        curframe = curframe.tb_next

    return reversed(frames)


def extract_exception_info():
    """
    Extract information about exception using ``sys.exc_info()``.

    Extracted informations are:

     - exception type
     - exception value
     - exception traceback
     - traceback frames (with disassembled code)

    :rtype: dict
    """

    errtype, err, traceback = sys.exc_info()

    return {
        'type': errtype,
        'value': err,
        'traceback': traceback,
        'frames': [
            {
                'frame': frame,
                'instructions': disassemble(frame.f_code, frame.f_lasti)
            }
            for frame in frames_from_traceback(traceback)
        ]
    }
